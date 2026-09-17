var traceConfig = {
  version: "1.0.2",
  engine: "ExecuTrace",
  mode: "replay",
  verbosity: 2,
  traceMeta: "RXgwcmNpc3Rze3c0bm40ZDEzX3RyNGNlXzF9",
  maxDepth: 128,
  bufferSize: 4096,
  outputFormat: "json"
};

var traceEvents = [
  { ts: "2026-04-06T08:00:01.003Z", pid: 1844, event: "exec_init", msg: "Initializing execution context", status: "ok" },
  { ts: "2026-04-06T08:00:01.017Z", pid: 1844, event: "cfg_load", msg: "Loading configuration from .exectrace/config.json", status: "ok" },
  { ts: "2026-04-06T08:00:01.042Z", pid: 1844, event: "env_check", msg: "Verifying runtime environment (Python 3.11.4)", status: "ok" },
  { ts: "2026-04-06T08:00:01.088Z", pid: 1844, event: "hist_read", msg: "Reading shell history (247 entries)", status: "info" },
  { ts: "2026-04-06T08:00:01.130Z", pid: 1844, event: "fs_watch", msg: "Attaching filesystem watcher on /home/dev/project", status: "ok" },
  { ts: "2026-04-06T08:00:01.155Z", pid: 1844, event: "trace_start", msg: "Processing trace events", status: "ok" },
  { ts: "2026-04-06T08:00:03.410Z", pid: 1844, event: "cmd_exec", msg: "Captured: pip install requests", status: "info" },
  { ts: "2026-04-06T08:00:05.892Z", pid: 1844, event: "cmd_exec", msg: "Captured: python main.py --verbose", status: "info" },
  { ts: "2026-04-06T08:00:08.201Z", pid: 1844, event: "fs_change", msg: "File modified: output/results.json (2.4 KB)", status: "info" },
  { ts: "2026-04-06T08:00:08.340Z", pid: 1844, event: "meta_write", msg: "Writing execution metadata to trace buffer", status: "ok" },
  { ts: "2026-04-06T08:00:08.512Z", pid: 1844, event: "trace_end", msg: "Finalizing execution trace", status: "ok" },
  { ts: "2026-04-06T08:00:08.530Z", pid: 1844, event: "cleanup", msg: "Detaching watchers and flushing buffers", status: "ok" }
];

function verifyTraceIntegrity() {
  try {
    var raw = atob(traceConfig.traceMeta);
    var checksum = 0;
    for (var i = 0; i < raw.length; i++) {
      checksum = (checksum + raw.charCodeAt(i)) & 0xffff;
    }
    return checksum > 0;
  } catch (e) {
    return false;
  }
}

function renderTimeline() {
  var container = document.getElementById("trace-timeline");
  if (!container) return;

  traceEvents.forEach(function (entry) {
    var div = document.createElement("div");
    div.className = "trace-entry" + (entry.status === "ok" ? " entry-ok" : " entry-info");

    var ts = document.createElement("div");
    ts.className = "trace-ts";
    ts.textContent = entry.ts;

    var msg = document.createElement("div");
    msg.className = "trace-msg";
    msg.textContent = "[" + entry.event + "] " + entry.msg;

    var pid = document.createElement("div");
    pid.className = "trace-pid";
    pid.textContent = "PID " + entry.pid;

    div.appendChild(ts);
    div.appendChild(msg);
    div.appendChild(pid);
    container.appendChild(div);
  });
}

function renderSummary() {
  var stats = [
    { label: "Events", value: traceEvents.length },
    { label: "Commands", value: traceEvents.filter(function (e) { return e.event === "cmd_exec"; }).length },
    { label: "FS Changes", value: traceEvents.filter(function (e) { return e.event === "fs_change"; }).length },
    { label: "Duration", value: "7.53s" }
  ];

  var container = document.getElementById("trace-summary");
  if (!container) return;

  stats.forEach(function (s) {
    var div = document.createElement("div");
    div.className = "trace-stat";

    var val = document.createElement("div");
    val.className = "stat-value";
    val.textContent = s.value;

    var lbl = document.createElement("div");
    lbl.className = "stat-label";
    lbl.textContent = s.label;

    div.appendChild(val);
    div.appendChild(lbl);
    container.appendChild(div);
  });
}

function init() {
  verifyTraceIntegrity();
  renderTimeline();
  renderSummary();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
