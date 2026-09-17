async function readJson(path) {
  const res = await fetch(path);
  if (!res.ok) {
    return [];
  }
  return res.json();
}

function escapeHtml(str) {
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

function renderTable(containerId, headers, rows) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!rows.length) {
    container.innerHTML = "<p>No entries yet.</p>";
    return;
  }

  const head = headers.map((h) => `<th>${escapeHtml(h)}</th>`).join("");
  const body = rows.map((row) => `<tr>${row.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("");

  container.innerHTML = `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

function safeLink(url, text) {
  var safeUrl = escapeHtml(url);
  if (!/^https?:\/\//i.test(safeUrl)) return escapeHtml(text);
  return `<a href="${safeUrl}" target="_blank" rel="noopener">${escapeHtml(text)}</a>`;
}

async function init() {
  const contributors = await readJson("data/contributors.json");
  const security = await readJson("data/security_hof.json");

  const contributorRows = contributors.map((c) => [
    safeLink(c.profile, c.login),
    escapeHtml(String(c.contributions)),
  ]);

  const securityRows = security.map((s) => [
    escapeHtml(s.name),
    escapeHtml(s.issue),
    escapeHtml(s.reported),
  ]);

  renderTable("contributors", ["Contributor", "Commits"], contributorRows);
  renderTable("security-hof", ["Researcher", "Issue", "Reported"], securityRows);
}

init();
