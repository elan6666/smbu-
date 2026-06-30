#!/usr/bin/env python3
from __future__ import annotations

import argparse
import inspect
import json
import sys
from pathlib import Path
from typing import Dict, List

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, Trainer, TrainingArguments

ROOT = Path(__file__).resolve().parents[1]


class ChatSFTDataset(Dataset):
    def __init__(self, rows: List[Dict[str, object]], tokenizer, max_length: int) -> None:
        self.rows = rows
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> Dict[str, torch.Tensor]:
        messages = self.rows[index]["messages"]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        encoded = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        input_ids = encoded["input_ids"][0]
        attention_mask = encoded["attention_mask"][0]
        labels = input_ids.clone()
        labels[attention_mask == 0] = -100
        return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}


def load_rows(path: Path) -> List[Dict[str, object]]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def save_loss_artifacts(log_history: List[Dict[str, float]], output_dir: Path, model_name: str, method: str) -> None:
    artifacts = ROOT / "artifacts" / "finetune"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "qwen7b_lora_log_history.json").write_text(
        json.dumps(log_history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    train_losses = [item for item in log_history if "loss" in item]
    eval_losses = [item for item in log_history if "eval_loss" in item]
    final_train = train_losses[-1]["loss"] if train_losses else float("nan")
    final_eval = eval_losses[-1]["eval_loss"] if eval_losses else float("nan")
    metrics = {
        "model": model_name,
        "method": method,
        "final_train_loss": final_train,
        "final_eval_loss": final_eval,
        "train_loss_points": len(train_losses),
        "eval_loss_points": len(eval_losses),
        "adapter_dir": str(output_dir),
    }
    (artifacts / "qwen7b_lora_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    report = ROOT / "report"
    report.mkdir(exist_ok=True)
    (report / "qwen_finetune_metrics.tex").write_text(
        "\\newcommand{\\QwenFineTuneModel}{Qwen2.5-7B-Instruct}\n"
        "\\newcommand{\\QwenFineTuneMethod}{%s}\n"
        "\\newcommand{\\QwenFineTuneTrainLoss}{%.3f}\n"
        "\\newcommand{\\QwenFineTuneEvalLoss}{%.3f}\n"
        % (method, final_train, final_eval),
        encoding="utf-8",
    )
    try:
        import matplotlib.pyplot as plt

        figure_dir = report / "figures"
        figure_dir.mkdir(parents=True, exist_ok=True)
        plt.figure(figsize=(6.2, 3.4))
        if train_losses:
            plt.plot([item.get("step", i + 1) for i, item in enumerate(train_losses)], [item["loss"] for item in train_losses], label="train loss")
        if eval_losses:
            plt.plot([item.get("step", i + 1) for i, item in enumerate(eval_losses)], [item["eval_loss"] for item in eval_losses], label="eval loss")
        plt.xlabel("step")
        plt.ylabel("loss")
        plt.title("Qwen2.5-7B QLoRA fine-tuning loss")
        plt.grid(alpha=0.25)
        plt.legend()
        plt.tight_layout()
        plt.savefig(figure_dir / "qwen7b-lora-loss.png", dpi=180)
        plt.close()
    except Exception as exc:
        (artifacts / "plot_error.txt").write_text(type(exc).__name__, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--dataset", default=str(ROOT / "data" / "finetune" / "sft_examples.jsonl"))
    parser.add_argument("--output-dir", default=str(ROOT / "models" / "qwen7b_lora"))
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--eval-steps", type=int, default=50)
    parser.add_argument("--save-steps", type=int, default=100)
    parser.add_argument("--max-steps", type=int, default=-1)
    parser.add_argument("--no-qlora", action="store_true", help="Use bf16 LoRA without 4-bit quantization when bitsandbytes is unavailable.")
    args = parser.parse_args()

    rows = load_rows(Path(args.dataset))
    train_rows = [row for row in rows if row.get("split") == "train"]
    eval_rows = [row for row in rows if row.get("split") == "eval"]
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quant_config = None
    if torch.cuda.is_available() and not args.no_qlora:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        quantization_config=quant_config,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() and args.no_qlora else None,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
    )
    if quant_config is not None:
        model = prepare_model_for_kbit_training(model)
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    output_dir = Path(args.output_dir)
    training_kwargs = {
        "output_dir": str(output_dir),
        "num_train_epochs": args.epochs,
        "learning_rate": args.lr,
        "per_device_train_batch_size": args.batch_size,
        "per_device_eval_batch_size": args.batch_size,
        "gradient_accumulation_steps": args.grad_accum,
        "logging_steps": 10,
        "eval_steps": args.eval_steps,
        "save_steps": args.save_steps,
        "save_strategy": "steps",
        "bf16": torch.cuda.is_available(),
        "fp16": False,
        "report_to": [],
        "remove_unused_columns": False,
        "gradient_checkpointing": True,
        "max_steps": args.max_steps,
    }
    if "eval_strategy" in inspect.signature(TrainingArguments).parameters:
        training_kwargs["eval_strategy"] = "steps"
    else:
        training_kwargs["evaluation_strategy"] = "steps"
    training_args = TrainingArguments(**training_kwargs)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ChatSFTDataset(train_rows, tokenizer, args.max_length),
        eval_dataset=ChatSFTDataset(eval_rows, tokenizer, args.max_length),
    )
    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    method = "QLoRA" if quant_config is not None else "LoRA bf16"
    save_loss_artifacts(trainer.state.log_history, output_dir, args.model, method)


if __name__ == "__main__":
    main()
