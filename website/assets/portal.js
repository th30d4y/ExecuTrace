var employeeRecords = [];
var restrictedIds = [1003];
var currentId = null;

function escapeText(str) {
  var el = document.createElement("span");
  el.textContent = str;
  return el.innerHTML;
}

async function loadRecords() {
  try {
    var res = await fetch("data/employees.json");
    if (!res.ok) throw new Error("Failed to load employee data");
    employeeRecords = await res.json();
  } catch (e) {
    employeeRecords = [];
  }
}

function renderRoster() {
  var container = document.getElementById("employee-roster");
  if (!container) return;
  container.innerHTML = "";

  employeeRecords.forEach(function (emp) {
    var card = document.createElement("div");
    card.className = "emp-card";
    card.setAttribute("data-id", emp.id);

    var badge = document.createElement("div");
    badge.className = "emp-badge";
    badge.textContent = emp.badge;

    var name = document.createElement("div");
    name.className = "emp-name";
    name.textContent = emp.name;

    var role = document.createElement("div");
    role.className = "emp-role";
    role.textContent = emp.role;

    var clearance = document.createElement("div");
    clearance.className = "emp-clearance" + (emp.clearance === "restricted" ? " restricted" : "");
    clearance.textContent = emp.clearance;

    card.appendChild(badge);
    card.appendChild(name);
    card.appendChild(role);
    card.appendChild(clearance);

    card.addEventListener("click", function () {
      document.getElementById("lookup-input").value = emp.id;
      viewRecord(emp.id);
    });

    container.appendChild(card);
  });
}

function viewRecord(id) {
  var viewer = document.getElementById("record-viewer");
  if (!viewer) return;

  var numId = parseInt(id, 10);
  currentId = numId;

  document.querySelectorAll(".emp-card").forEach(function (card) {
    card.classList.toggle("active", parseInt(card.getAttribute("data-id"), 10) === numId);
  });

  if (restrictedIds.indexOf(numId) !== -1) {
    viewer.innerHTML =
      '<div class="access-denied">' +
      '<div class="denied-icon">ACCESS DENIED</div>' +
      '<div class="denied-msg">Record ' + escapeText(String(numId)) + ' requires elevated clearance.<br>Contact your system administrator.</div>' +
      "</div>";
    return;
  }

  var record = employeeRecords.find(function (e) { return e.id === numId; });

  if (!record) {
    viewer.innerHTML = '<div class="viewer-empty">No record found for ID ' + escapeText(String(numId)) + '</div>';
    return;
  }

  renderRecord(record);
}

function renderRecord(record) {
  var viewer = document.getElementById("record-viewer");
  viewer.innerHTML = "";

  var fields = [
    { key: "ID", val: record.id },
    { key: "Name", val: record.name },
    { key: "Role", val: record.role },
    { key: "Department", val: record.department },
    { key: "Clearance", val: record.clearance },
    { key: "Badge", val: record.badge },
    { key: "Email", val: record.email },
    { key: "Notes", val: record.notes }
  ];

  fields.forEach(function (f) {
    var row = document.createElement("div");
    row.className = "record-field";

    var key = document.createElement("div");
    key.className = "field-key";
    key.textContent = f.key;

    var val = document.createElement("div");
    val.className = "field-val";
    val.textContent = String(f.val);

    row.appendChild(key);
    row.appendChild(val);
    viewer.appendChild(row);
  });
}

function handleLookup() {
  var input = document.getElementById("lookup-input");
  if (!input) return;
  var id = parseInt(input.value, 10);
  if (isNaN(id)) return;
  viewRecord(id);
}

async function init() {
  await loadRecords();
  renderRoster();

  var btn = document.getElementById("lookup-btn");
  if (btn) btn.addEventListener("click", handleLookup);

  var input = document.getElementById("lookup-input");
  if (input) {
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") handleLookup();
    });
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
