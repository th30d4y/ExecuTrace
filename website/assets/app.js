async function readJson(path) {
  const res = await fetch(path);
  if (!res.ok) {
    return [];
  }
  return res.json();
}

function renderTable(containerId, headers, rows) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!rows.length) {
    container.innerHTML = "<p>No entries yet.</p>";
    return;
  }

  const head = headers.map((h) => `<th>${h}</th>`).join("");
  const body = rows.map((row) => `<tr>${row.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("");

  container.innerHTML = `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

async function init() {
  const contributors = await readJson("data/contributors.json");
  const security = await readJson("data/security_hof.json");

  const contributorRows = contributors.map((c) => [
    `<a href="${c.profile}" target="_blank" rel="noopener">${c.login}</a>`,
    String(c.contributions),
  ]);

  const securityRows = security.map((s) => [
    s.name,
    s.issue,
    s.reported,
  ]);

  renderTable("contributors", ["Contributor", "Commits"], contributorRows);
  renderTable("security-hof", ["Researcher", "Issue", "Reported"], securityRows);
}

init();
