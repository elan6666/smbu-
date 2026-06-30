const messages = document.getElementById("messages");
const evidence = document.getElementById("evidence");
const form = document.getElementById("form");
const questionInput = document.getElementById("question");

function value(id) {
  const raw = document.getElementById(id).value.trim();
  if (!raw) return null;
  if (id === "score" || id === "rank") return Number(raw);
  return raw;
}

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = `message ${who}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function renderEvidence(data) {
  const sourceHtml = (data.sources || [])
    .map(
      (s) => `<div class="source"><a href="${s.url}" target="_blank">${s.title}</a><p>${s.snippet}</p></div>`
    )
    .join("");
  const rowHtml = (data.score_rows || [])
    .map(
      (r) =>
        `<div class="row">${r.year || ""} ${r.province || ""} ${r.category || ""} ${r.major || ""}<br>最低分：${r.min_score || "待官方表补全"}，最低位次：${r.min_rank || "待官方表补全"}</div>`
    )
    .join("");
  const programHtml = (data.program_rows || [])
    .map(
      (r) =>
        `<div class="row">${r.level || ""} ${r.program || ""}<br>学籍/证书：${r.degree_mode || ""}；${r.smbu_certificate || "无"} / ${r.msu_certificate || "无"}<br>教学语言：${r.teaching_language || ""}；招生人数：${r.enrollment_count || "以正式计划为准"}</div>`
    )
    .join("");
  const dimensionHtml = (data.dimension_rows || [])
    .map((r) => `<div class="row">${r.level || ""} ${r.dimension || ""}：${r.value || ""}<br>${r.notes || ""}</div>`)
    .join("");
  evidence.innerHTML = programHtml + dimensionHtml + rowHtml + sourceHtml || "没有返回来源。";
}

async function ask(question) {
  addMessage(question, "user");
  questionInput.value = "";
  addMessage("检索资料并生成回答中...", "assistant");
  const payload = {
    question,
    profile: {
      province: value("province"),
      category: value("category"),
      score: value("score"),
      rank: value("rank"),
      preferred_major: value("major"),
    },
    enable_web_search: document.getElementById("webSearch").checked,
  };
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  messages.lastChild.textContent = data.answer;
  renderEvidence(data);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const q = questionInput.value.trim();
  if (q) ask(q);
});

document.querySelectorAll("[data-q]").forEach((button) => {
  button.addEventListener("click", () => ask(button.dataset.q));
});

addMessage("请输入报考问题。我会优先使用官方资料和结构化分数线表回答，并标出资料边界。", "assistant");
