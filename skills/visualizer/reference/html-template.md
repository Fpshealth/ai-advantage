# HTML Template — Visualizer: Team-AI

The canonical **single self-contained HTML file** the Visualizer writes. One file, inline `<style>` **and one
inline `<script>`** — **no external dependencies, no CDN, no Mermaid, no framework, no network calls**. The
person's language throughout (English default per `house-style.md` §1). Warm, professional, system-font,
generous whitespace, no emoji.

The page is **lightly interactive**: the employee can drag-reorder steps, fix step text in place, and flag each
step as *correct / unclear / incorrect*. All interactive chrome is **injected by the inline script on load**, so
with JavaScript disabled the page is a clean read-only render with **no dangling controls** and prints correctly.
The source `.md` stays the single source of truth — see the writeback contract below.

Fill every `{{placeholder}}`. Escape `<`, `>`, `&` from the source content before injecting. Missing sections
render the literal string **— still open —**. The "Does this look right?" footer stays as written; only
`{{SOURCE_FILE}}` is injected.

## Placeholder reference

| Placeholder | Source |
|---|---|
| `{{TITLE}}` | `title` frontmatter / `# H1` heading |
| `{{TYPE_BADGE}}` | `SOP` or `Process Documentation` (detected) |
| `{{DOCTYPE}}` | `sop` or `process-doc` — machine value, injected on `<body data-doctype>` (drives reorder semantics + export shape) |
| `{{VERSION}}` | `version` frontmatter |
| `{{ROLE}}` | `owner_role` / owning role |
| `{{DATE}}` | `created` frontmatter |
| `{{SOURCE_FILE}}` | basename of the source `.md` (e.g. `sop-returns-2026-05-31.md`) |
| `{{PURPOSE}}` | `## Purpose` |
| `{{SCOPE}}` | `## Scope` |
| `{{PREREQUISITES}}` | `## Prerequisites` |
| `{{STEPS}}` | `## Steps` → vertical numbered flow (see below) |
| `{{DECISIONS}}` | `## Decisions & Branches` |
| `{{DOD}}` | `## Definition of Done` |
| `{{EXCEPTIONS}}` | `## Exceptions & Escalation` |
| `{{REFERENCES}}` | `## References & Links` |
| `{{ANNOTATIONS}}` | `## Annotations` if present, else omit the whole card |

**Step blocks** (`{{STEPS}}`): one `<div class="step" data-step>` per step. Each carries a numbered badge
(`.num`), an editable title (`.step-title`), and the labelled lines `Signal / Action / Confirmation / Tool`
as `<div class="field">` rows. Mark each value span with `data-field="Signal"` etc. — the script reads these to
regenerate Markdown. Between consecutive steps insert `<div class="arrow" aria-hidden="true"></div>`.

- **Optional `Why` line:** if the source step supplies a `Why:` value, render one extra row
  `<div class="field why"><span class="k">Why</span><span class="v" data-field="Why">…</span></div>`. Omit the
  row entirely when absent — never render an empty box.
- **Optional screenshot slot:** if the source step supplies an image field whose value is a base64 data URI
  (`data:image/png;base64,…`) or an already-inlined data URI, render `<img class="step-shot" src="{{…}}"
  alt="Screenshot: {{Step Title}}">`. Inline data URIs only — **never** an `http(s)://` URL or a local file
  path (would break the offline single-file rule). If the image value is absent or not a data URI, render no `<img>`.
- For a **Process Documentation**, use the same `.step` block per process stage, add a small
  `<span class="role-tag">{{Role}}</span>` inside the title, and set `data-role="{{Role}}"` on the `.step` so the
  role survives export.

**Open markers:** wrap `[OPEN]` from the source in `<span class="marker">…</span>`.

## The file skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} — {{TYPE_BADGE}}</title>
<style>
  :root{
    --ink:#2b2622; --muted:#6f655c; --line:#e7e0d8; --bg:#faf7f2;
    --card:#ffffff; --accent:#b9742f; --accent-soft:#f3e7d8; --amber:#9a6b12;
    --ok:#3f7d52; --ok-soft:#e7f0e6; --unsure:#9a6b12; --unsure-soft:#fbf3e2;
    --bad:#b3402f; --bad-soft:#f7e6e2;
  }
  *{box-sizing:border-box;}
  html{-webkit-text-size-adjust:100%;}
  body{
    margin:0; background:var(--bg); color:var(--ink); line-height:1.6;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    font-size:17px;
  }
  .wrap{max-width:820px; margin:0 auto; padding:40px 24px 120px;}
  header.doc{border-bottom:1px solid var(--line); padding-bottom:24px; margin-bottom:32px;}
  .badge{
    display:inline-block; font-size:13px; font-weight:600; letter-spacing:.04em;
    text-transform:uppercase; color:var(--accent); background:var(--accent-soft);
    border-radius:999px; padding:4px 12px; margin-bottom:14px;
  }
  h1.title{font-size:30px; line-height:1.25; margin:0 0 12px; font-weight:700;}
  .meta{color:var(--muted); font-size:15px;}
  .meta span{margin-right:18px; white-space:nowrap;}
  h2.section{font-size:14px; text-transform:uppercase; letter-spacing:.05em;
    color:var(--muted); margin:36px 0 12px; font-weight:600;}
  .card{
    background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:20px 22px; margin:0 0 14px;
  }
  .card p:first-child{margin-top:0;} .card p:last-child{margin-bottom:0;}
  ul{margin:0; padding-left:20px;} li{margin:4px 0;}
  /* vertical numbered flow */
  .flow{margin:4px 0;}
  .step{
    background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:18px 22px 18px 60px; position:relative;
    transition:border-color .15s, box-shadow .15s, background .15s;
  }
  .step .num{
    position:absolute; left:16px; top:18px; width:30px; height:30px; border-radius:50%;
    background:var(--accent); color:#fff; font-weight:700; font-size:15px;
    display:flex; align-items:center; justify-content:center;
  }
  .step h3{margin:0 0 10px; font-size:18px; font-weight:650;}
  .role-tag{
    display:inline-block; font-size:12px; font-weight:600; color:var(--muted);
    background:var(--bg); border:1px solid var(--line); border-radius:999px;
    padding:2px 10px; margin-left:8px; vertical-align:middle;
  }
  .field{display:flex; gap:8px; margin:3px 0; font-size:16px;}
  .field .k{flex:0 0 110px; color:var(--muted); font-weight:600;}
  .field .v{flex:1;}
  .field.why .k{color:var(--accent);}
  .field.why .v{font-style:italic;}
  .step-shot{display:block; max-width:100%; height:auto; margin:12px 0 2px;
    border:1px solid var(--line); border-radius:10px;}
  .arrow{width:2px; height:22px; background:var(--line); margin:0 auto; position:relative;}
  .arrow::after{
    content:""; position:absolute; left:50%; bottom:-1px; transform:translateX(-50%);
    border-left:6px solid transparent; border-right:6px solid transparent;
    border-top:8px solid var(--line);
  }
  .marker{
    font-size:13px; font-weight:600; color:var(--amber);
    background:#fbf3e2; border:1px solid #ecd9b0; border-radius:6px; padding:1px 7px;
  }
  .notes{border-left:3px solid var(--accent);}
  footer.check{
    margin-top:48px; background:var(--accent-soft); border:1px solid #ecd9c2;
    border-radius:14px; padding:24px 26px;
  }
  footer.check h2{margin:0 0 10px; font-size:19px; color:var(--ink); text-transform:none; letter-spacing:0;}
  footer.check ol{margin:8px 0 0; padding-left:22px;} footer.check li{margin:6px 0;}
  footer.check code{background:#fff; border:1px solid var(--line); border-radius:5px; padding:1px 6px; font-size:14px;}
  .src{color:var(--muted); font-size:13px; margin-top:24px; text-align:center;}

  /* ---- Interactive layer (all of this is only meaningful once the script injects controls) ---- */
  /* Drag + reorder */
  .step.dragging{opacity:.45;}
  .step.drop-target{border-color:var(--accent); box-shadow:0 0 0 2px var(--accent-soft);}
  .step-tools{position:absolute; right:14px; top:14px; display:flex; gap:4px;}
  .step-tools button{
    width:28px; height:28px; border:1px solid var(--line); background:var(--card);
    border-radius:7px; color:var(--muted); font-size:15px; line-height:1; cursor:pointer;
  }
  .step-tools button:hover{border-color:var(--accent); color:var(--accent);}
  .drag-handle{cursor:grab;}
  .step .v[contenteditable="true"]{
    outline:none; border-bottom:1px dashed var(--line); border-radius:3px;
    padding:0 2px; min-width:2ch;
  }
  .step .v[contenteditable="true"]:focus{border-bottom-color:var(--accent); background:#fffdf9;}
  .step-title[contenteditable="true"]{outline:none;}
  .step-title[contenteditable="true"]:focus{background:#fffdf9; border-radius:4px;}
  /* Verify three-state */
  .verify{display:flex; gap:8px; margin-top:12px; flex-wrap:wrap;}
  .verify button{
    font-size:14px; font-weight:600; border:1px solid var(--line); background:var(--card);
    border-radius:999px; padding:4px 14px; cursor:pointer; color:var(--muted);
  }
  .verify button[aria-pressed="true"][data-vote="correct"]{background:var(--ok-soft); border-color:var(--ok); color:var(--ok);}
  .verify button[aria-pressed="true"][data-vote="unclear"]{background:var(--unsure-soft); border-color:var(--unsure); color:var(--unsure);}
  .verify button[aria-pressed="true"][data-vote="incorrect"]{background:var(--bad-soft); border-color:var(--bad); color:var(--bad);}
  .step-note{margin-top:10px;}
  .step-note textarea{
    width:100%; font:inherit; font-size:15px; color:var(--ink); border:1px solid var(--line);
    border-radius:8px; padding:8px 10px; resize:vertical; min-height:48px; background:#fffdf9;
  }
  /* Live tint of touched steps */
  .step.is-touched{border-color:var(--accent);}
  .step.flag-unclear{background:#fffdf6;}
  .step.flag-incorrect{background:#fdf4f2;}
  /* Floating apply panel */
  .apply-bar{
    position:fixed; right:20px; bottom:20px; z-index:40;
    background:var(--accent); color:#fff; border:none; border-radius:999px;
    padding:12px 20px; font:inherit; font-weight:650; font-size:15px; cursor:pointer;
    box-shadow:0 4px 16px rgba(0,0,0,.18); display:none;
  }
  .apply-bar .dot{display:inline-block; width:8px; height:8px; border-radius:50%; background:#fff; margin-right:8px; vertical-align:middle;}
  .apply-overlay{
    position:fixed; inset:0; z-index:50; background:rgba(43,38,34,.45);
    display:none; align-items:center; justify-content:center; padding:24px;
  }
  .apply-overlay.open{display:flex;}
  .apply-modal{
    background:var(--card); border-radius:16px; max-width:680px; width:100%;
    max-height:86vh; overflow:auto; padding:26px 28px;
  }
  .apply-modal h2{margin:0 0 6px; font-size:21px;}
  .apply-modal p{color:var(--muted); margin:0 0 14px; font-size:15px;}
  .apply-modal ol{margin:0 0 16px; padding-left:22px; font-size:15px;}
  .apply-modal h3{font-size:14px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:18px 0 8px;}
  .apply-modal textarea{
    width:100%; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:13px;
    border:1px solid var(--line); border-radius:10px; padding:12px; min-height:150px; background:var(--bg); color:var(--ink);
  }
  .apply-actions{display:flex; gap:10px; margin-top:8px; flex-wrap:wrap;}
  .apply-actions button{
    font:inherit; font-weight:600; font-size:15px; border-radius:9px; padding:9px 16px; cursor:pointer; border:1px solid var(--line); background:var(--card); color:var(--ink);
  }
  .apply-actions button.primary{background:var(--accent); border-color:var(--accent); color:#fff;}
  .copied{color:var(--ok); font-size:14px; font-weight:600; align-self:center;}

  @media print{
    body{background:#fff;}
    .card,.step,footer.check{break-inside:avoid;}
    .step-tools,.verify,.step-note,.apply-bar,.apply-overlay{display:none !important;}
    .step .v[contenteditable]{border-bottom:none !important;}
    /* Read Aloud & Confirm — print-only two-person confirmation sheet */
    .readaloud{display:block !important;}
  }
  .readaloud{display:none;}
  .readaloud h2{font-size:16px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:28px 0 10px;}
  .readaloud ol{padding-left:0; list-style:none; margin:0;}
  .readaloud li{display:flex; align-items:flex-start; gap:10px; padding:8px 0; border-bottom:1px solid var(--line); break-inside:avoid;}
  .readaloud .chk{flex:0 0 18px; height:18px; border:1.5px solid var(--ink); border-radius:4px; margin-top:3px;}
  .signoff{display:flex; gap:40px; margin-top:24px;}
  .signoff div{flex:1; border-top:1px solid var(--ink); padding-top:6px; font-size:14px; color:var(--muted);}
</style>
</head>
<body data-doctype="{{DOCTYPE}}">
<div class="wrap">

  <header class="doc">
    <span class="badge">{{TYPE_BADGE}}</span>
    <h1 class="title">{{TITLE}}</h1>
    <div class="meta">
      <span>Version {{VERSION}}</span>
      <span>Role: {{ROLE}}</span>
      <span>Date: {{DATE}}</span>
    </div>
  </header>

  <h2 class="section">Purpose</h2>
  <div class="card">{{PURPOSE}}</div>

  <h2 class="section">Scope</h2>
  <div class="card">{{SCOPE}}</div>

  <h2 class="section">Prerequisites</h2>
  <div class="card">{{PREREQUISITES}}</div>

  <h2 class="section">Steps</h2>
  <div class="flow" id="flow">
    {{STEPS}}
    <!-- one per step (Tool + Why + Image are optional; omit when the source doesn't have them):
    <div class="step" data-step data-role="{{Role}}">
      <span class="num">1</span>
      <h3 class="step-title">{{Step Title}}<span class="role-tag">{{Role}}</span></h3>
      <div class="field"><span class="k">Signal</span><span class="v" data-field="Signal">{{…}}</span></div>
      <div class="field"><span class="k">Action</span><span class="v" data-field="Action">{{…}}</span></div>
      <div class="field"><span class="k">Confirmation</span><span class="v" data-field="Confirmation">{{…}}</span></div>
      <div class="field"><span class="k">Tool</span><span class="v" data-field="Tool">{{…}}</span></div>
      <div class="field why"><span class="k">Why</span><span class="v" data-field="Why">{{…}}</span></div>
      <img class="step-shot" src="data:image/png;base64,{{…}}" alt="Screenshot: {{Step Title}}">
    </div>
    <div class="arrow" aria-hidden="true"></div>
    -->
  </div>

  <h2 class="section">Decisions &amp; Branches</h2>
  <div class="card">{{DECISIONS}}</div>

  <h2 class="section">Definition of Done</h2>
  <div class="card">{{DOD}}</div>

  <h2 class="section">Exceptions &amp; Escalation</h2>
  <div class="card">{{EXCEPTIONS}}</div>

  <h2 class="section">References &amp; Links</h2>
  <div class="card">{{REFERENCES}}</div>

  <!-- Only include when the source has an ## Annotations section: -->
  <h2 class="section">Annotations</h2>
  <div class="card notes">{{ANNOTATIONS}}</div>

  <!-- Print-only read-aloud confirmation sheet. Script clones step titles into the list on load. -->
  <section class="readaloud" aria-hidden="true">
    <h2>Read Aloud &amp; Confirm</h2>
    <ol id="readaloud-list"><!-- one <li> per step, filled by the script --></ol>
    <div class="signoff">
      <div>Described by / Date</div>
      <div>Confirmed by / Date</div>
    </div>
  </section>

  <footer class="check">
    <h2>Does this look right?</h2>
    <p>This view shows your work the way it's currently documented. You can check it right here:
    mark each step as <strong>correct / unclear / incorrect</strong>, drag steps into the right
    order, or fix a piece of text. When you're done, click <strong>"Apply changes"</strong> in the
    bottom right — you'll get a finished text to paste into the source file.</p>
    <p>No button working for you (e.g. JavaScript off)? Then correct it this way:</p>
    <ol>
      <li>Open the file <code>{{SOURCE_FILE}}</code>.</li>
      <li>Write your correction at the very bottom under the heading <code>## Annotations</code>
      (in your own words — no jargon needed).</li>
      <li>Save.</li>
      <li>Just tell me <code>visualize</code> again — then I'll rebuild the view.</li>
    </ol>
    <p>This way the source file stays the single truth, and the view is always up to date.</p>
  </footer>

  <p class="src">Generated from {{SOURCE_FILE}} · Cowork: Team-AI</p>

</div>

<!-- Interactive layer: injected on load, degrades to read-only with JS off. No CDN, no framework, no network. -->
<script>
(function(){
  "use strict";
  var SOURCE_FILE = "{{SOURCE_FILE}}";
  var flow = document.getElementById("flow");
  if(!flow) return;
  var steps = Array.prototype.slice.call(flow.querySelectorAll(".step[data-step]"));
  if(!steps.length) return;                 // malformed/empty source → no controls injected
  var doctype = (document.body.getAttribute("data-doctype") || "sop").toLowerCase();
  var touched = false;                       // any reorder/edit happened
  function clean(s){ return (s==null?"":String(s)).replace(/\s+/g," ").trim(); }

  // ---- build the print-only read-aloud list from current step titles ----
  function buildReadAloud(){
    var ol = document.getElementById("readaloud-list");
    if(!ol) return;
    ol.innerHTML = "";
    eachStep(function(step, i){
      var li = document.createElement("li");
      var box = document.createElement("span"); box.className = "chk";
      var txt = document.createElement("span");
      txt.textContent = (i+1) + ". " + stepTitle(step);
      li.appendChild(box); li.appendChild(txt); ol.appendChild(li);
    });
  }
  function eachStep(fn){ flow.querySelectorAll(".step[data-step]").forEach(fn); }
  function stepTitle(step){
    var h = step.querySelector(".step-title");
    if(!h) return "";
    var clone = h.cloneNode(true);
    var tag = clone.querySelector(".role-tag"); if(tag) tag.remove();
    return clean(clone.textContent);
  }
  function markTouched(){ touched = true; bar.style.display = "block"; }

  // ---- renumber badges after a reorder ----
  function renumber(){
    var n = 1;
    eachStep(function(step){ var b = step.querySelector(".num"); if(b) b.textContent = n++; });
    buildReadAloud();
  }

  // ---- make fields editable + add reorder tools ----
  steps.forEach(function(step){
    // editable values + title
    step.querySelectorAll(".v[data-field]").forEach(function(v){
      v.setAttribute("contenteditable","true");
      v.addEventListener("input", function(){ step.classList.add("is-touched"); markTouched(); });
    });
    var title = step.querySelector(".step-title");
    if(title){
      title.setAttribute("contenteditable","true");
      title.addEventListener("input", function(){ step.classList.add("is-touched"); markTouched(); buildReadAloud(); });
    }
    // reorder tools: drag handle + up/down (touch-friendly + accessible)
    var tools = document.createElement("div"); tools.className = "step-tools";
    var up = btn("▲","Move up"), down = btn("▼","Move down"), grip = btn("⠿","Drag to move");
    grip.className = "drag-handle";
    up.addEventListener("click", function(){ move(step,-1); });
    down.addEventListener("click", function(){ move(step,1); });
    tools.appendChild(up); tools.appendChild(down); tools.appendChild(grip);
    step.appendChild(tools);
    // native HTML5 drag via the grip
    step.setAttribute("draggable","false");
    grip.addEventListener("mousedown", function(){ step.setAttribute("draggable","true"); });
    grip.addEventListener("mouseup", function(){ step.setAttribute("draggable","false"); });
    step.addEventListener("dragstart", function(e){ dragged = step; step.classList.add("dragging"); e.dataTransfer.effectAllowed="move"; });
    step.addEventListener("dragend", function(){ step.classList.remove("dragging"); step.setAttribute("draggable","false"); clearTargets(); reflowArrows(); renumber(); markTouched(); });

    // ---- three-state verify + optional note ----
    var verify = document.createElement("div"); verify.className = "verify"; verify.setAttribute("role","group");
    ["correct","unclear","incorrect"].forEach(function(state){
      var b = document.createElement("button"); b.type="button"; b.textContent = state;
      b.setAttribute("data-vote", state); b.setAttribute("aria-pressed","false");
      b.addEventListener("click", function(){ setVote(step, state); });
      verify.appendChild(b);
    });
    step.appendChild(verify);
    var noteWrap = document.createElement("div"); noteWrap.className="step-note"; noteWrap.hidden = true;
    var ta = document.createElement("textarea"); ta.setAttribute("data-note","");
    ta.placeholder = "What exactly is incorrect / unclear? (optional)";
    ta.addEventListener("input", markTouched);
    noteWrap.appendChild(ta); step.appendChild(noteWrap);
  });

  function btn(txt,label){ var b=document.createElement("button"); b.type="button"; b.textContent=txt; b.setAttribute("aria-label",label); b.title=label; return b; }

  function setVote(step, state){
    var current = step.getAttribute("data-vote");
    var next = current === state ? "" : state;            // click again to clear
    step.setAttribute("data-vote", next);
    step.querySelectorAll(".verify button").forEach(function(b){
      b.setAttribute("aria-pressed", b.getAttribute("data-vote") === next ? "true" : "false");
    });
    step.classList.remove("flag-unclear","flag-incorrect");
    if(next === "unclear") step.classList.add("flag-unclear");
    if(next === "incorrect") step.classList.add("flag-incorrect");
    var note = step.querySelector(".step-note");
    if(note) note.hidden = !(next === "unclear" || next === "incorrect");
    if(next) step.classList.add("is-touched");
    markTouched();
  }

  // ---- reorder helpers ----
  var dragged = null;
  function clearTargets(){ eachStep(function(s){ s.classList.remove("drop-target"); }); }
  function move(step, dir){
    var sibs = Array.prototype.slice.call(flow.querySelectorAll(".step[data-step]"));
    var i = sibs.indexOf(step), j = i + dir;
    if(j < 0 || j >= sibs.length) return;
    if(dir < 0) flow.insertBefore(step, sibs[j]);
    else flow.insertBefore(sibs[j], step);
    reflowArrows(); renumber(); step.classList.add("is-touched"); markTouched();
  }
  flow.addEventListener("dragover", function(e){
    e.preventDefault();
    var after = afterElement(e.clientY);
    clearTargets();
    if(dragged){
      if(after == null) flow.appendChild(dragged);
      else flow.insertBefore(dragged, after);
      if(after) after.classList.add("drop-target");
    }
  });
  function afterElement(y){
    var els = Array.prototype.slice.call(flow.querySelectorAll(".step[data-step]:not(.dragging)"));
    var closest = {dist:-Infinity, el:null};
    els.forEach(function(el){
      var box = el.getBoundingClientRect();
      var offset = y - box.top - box.height/2;
      if(offset < 0 && offset > closest.dist){ closest = {dist:offset, el:el}; }
    });
    return closest.el;
  }
  // keep exactly one .arrow between steps after any reorder
  function reflowArrows(){
    flow.querySelectorAll(".arrow").forEach(function(a){ a.remove(); });
    var sibs = Array.prototype.slice.call(flow.querySelectorAll(".step[data-step]"));
    sibs.forEach(function(step, i){
      if(i < sibs.length - 1){
        var ar = document.createElement("div"); ar.className="arrow"; ar.setAttribute("aria-hidden","true");
        step.after(ar);
      }
    });
  }

  // ---- writeback: regenerate ## Steps body + ## Annotations block ----
  function buildSteps(){
    var out = ["## Steps",""];
    eachStep(function(step, i){
      var title = stepTitle(step) || "Step " + (i+1);
      out.push("### " + (i+1) + ". " + title);
      if(doctype === "process-doc"){
        var tag = step.querySelector(".role-tag");
        var role = clean(tag ? tag.textContent : step.getAttribute("data-role"));
        if(role) out.push("- **Role:** " + role);
      }
      step.querySelectorAll(".field .v[data-field]").forEach(function(v){
        var val = clean(v.textContent);
        if(val) out.push("- **" + v.getAttribute("data-field") + ":** " + val);
      });
      out.push("");
    });
    return out.join("\n").trim() + "\n";
  }
  function buildAnnotations(){
    var lines = [];
    eachStep(function(step, i){
      var state = step.getAttribute("data-vote");
      if(!state || state === "correct") return;
      var label = state === "incorrect" ? "incorrect" : "unclear";
      var ta = step.querySelector(".step-note textarea");
      var note = ta ? clean(ta.value) : "";
      lines.push("- Step " + (i+1) + " (" + stepTitle(step) + ") " + label + (note ? ": " + note : "."));
    });
    if(!lines.length) return "";
    return "## Annotations\n\n" + lines.join("\n") + "\n";
  }
  function hasFlags(){ var f=false; eachStep(function(s){ var v=s.getAttribute("data-vote"); if(v && v!=="correct") f=true; }); return f; }

  // ---- floating apply bar + modal ----
  var bar = document.createElement("button");
  bar.className="apply-bar"; bar.type="button";
  bar.innerHTML = '<span class="dot"></span>Apply changes';
  document.body.appendChild(bar);

  var overlay = document.createElement("div"); overlay.className="apply-overlay";
  overlay.innerHTML =
    '<div class="apply-modal" role="dialog" aria-modal="true" aria-label="Apply changes">' +
      '<h2>Apply changes</h2>' +
      '<p>This page doesn\'t save anything on its own. Copy the relevant block and paste it into your source file <code>'+SOURCE_FILE+'</code> — then tell me "visualize" again.</p>' +
      '<div data-sec="steps"><h3>Updated steps (replaces your ## Steps section)</h3>' +
        '<textarea data-out="steps" readonly></textarea>' +
        '<div class="apply-actions"><button class="primary" data-copy="steps">Copy steps</button><span class="copied" data-copied="steps" hidden>Copied ✓</span></div></div>' +
      '<div data-sec="annotations"><h3>Annotations (append to the bottom of the source file)</h3>' +
        '<textarea data-out="annotations" readonly></textarea>' +
        '<div class="apply-actions"><button class="primary" data-copy="annotations">Copy annotations</button><span class="copied" data-copied="annotations" hidden>Copied ✓</span></div></div>' +
      '<div class="apply-actions" style="margin-top:18px;"><button data-close>Close</button></div>' +
    '</div>';
  document.body.appendChild(overlay);

  function openModal(){
    // Show the Steps block whenever steps were reordered/edited; show Annotations only when flags exist.
    var secS = overlay.querySelector('[data-sec="steps"]');
    var secA = overlay.querySelector('[data-sec="annotations"]');
    overlay.querySelector('[data-out="steps"]').value = buildSteps();
    var ann = buildAnnotations();
    secA.style.display = ann ? "" : "none";
    overlay.querySelector('[data-out="annotations"]').value = ann;
    secS.style.display = ""; // always available — the regenerated body is the safe source of truth
    overlay.classList.add("open");
  }
  function closeModal(){ overlay.classList.remove("open"); }
  bar.addEventListener("click", openModal);
  overlay.addEventListener("click", function(e){ if(e.target === overlay) closeModal(); });
  overlay.querySelector("[data-close]").addEventListener("click", closeModal);
  overlay.querySelectorAll("[data-copy]").forEach(function(b){
    b.addEventListener("click", function(){
      var key = b.getAttribute("data-copy");
      var ta = overlay.querySelector('[data-out="'+key+'"]');
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch(e){}
      if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(ta.value).catch(function(){}); ok = true; }
      var flag = overlay.querySelector('[data-copied="'+key+'"]');
      if(flag){ flag.hidden = false; setTimeout(function(){ flag.hidden = true; }, 1800); }
    });
  });
  document.addEventListener("keydown", function(e){ if(e.key === "Escape") closeModal(); });

  buildReadAloud();
})();
</script>
</body>
</html>
```

## Notes for filling the template

- **Writeback shape.** The script regenerates `## Steps` as `### N. Title` headings with `- **Field:**
  value` bullets (and a `- **Role:** …` bullet for Process Documentation stages), and assembles `## Annotations` as
  `- Step N (Title) incorrect: …` lines. Re-running `visualize` on that regenerated body MUST reproduce
  the new arrangement — this is the one and only place the writeback shape is defined; keep the parser in
  SKILL.md pointed here, never restate it there.
- **Export safety.** Export reads `textContent`/`value` (never `innerHTML`), so editable content cannot inject markup.
