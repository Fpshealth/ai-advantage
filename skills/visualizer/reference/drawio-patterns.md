# draw.io construction patterns

Every cell the Visualizer writes follows these rules. Adapted from
`github/awesome-copilot` (draw-io-diagram-generator) and `sparklabx/drawio-ai-kit`
(drawio-bpmn stencil catalog), both MIT-licensed.

## A. File skeleton

```xml
<mxfile host="Electron" modified="2026-08-25T00:00:00.000Z" version="26.0.0" type="device">
  <diagram id="main" name="Page-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
        tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1"
        pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- content cells -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- `id="0"` / `id="1"` are reserved and must be the first two children of `<root>`, with no
  attributes beyond those shown.
- Write **uncompressed** XML — plain readable `mxGraphModel`, never base64/deflate.
- Vertex: `vertex="1"` + `<mxGeometry x y width height as="geometry"/>`.
- Edge: `edge="1" source=".." target=".."` + `<mxGeometry relative="1" as="geometry"/>`.
- Ids are readable and stable: `lane-warehouse`, `step-check-receipt`, `gw-refund-over-200`,
  `edge-07`, `note-01`. An id, once written, never changes.

## B. Map forms

**B1. Plain flow (single acting role).** Steps, gateways, and events parent directly to `"1"` with
absolute coordinates — no pool, no lanes. Process name + role in a title text cell at the top.
Same shapes, grid, and edge rules as below.

**B2. Pool + swimlanes (multi-role handoffs).**

```xml
<mxCell id="pool" value="Returns Processing" style="shape=pool;startSize=30;horizontal=1;"
    vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="1400" height="600" as="geometry"/></mxCell>
<mxCell id="lane-customer" value="Customer" style="swimlane;startSize=30;horizontal=0;"
    vertex="1" parent="pool">
  <mxGeometry x="0" y="30" width="1400" height="140" as="geometry"/></mxCell>
<mxCell id="step-check-receipt" value="Verify 30-day window"
    style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="lane-customer">
  <mxGeometry x="80" y="40" width="120" height="60" as="geometry"/></mxCell>
```

- Lanes stack vertically inside the pool, each the pool's full width; lane label on the left
  (`horizontal=0` on the lane style rotates it).
- Coordinates inside a lane are **relative to that lane's origin** — repositioning a lane never
  requires touching its children.
- Every step parents to its lane id, never to `"1"`. Edges (including cross-lane) parent to `"1"`.
- A lane whose children overflow gets a bigger `height`; children keep their coordinates.

## C. Shape styles

Common wrapper for event/gateway shapes:
`outlineConnect=0;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;fontSize=11;`
Keep the map monochrome (black on white). Accent `#1A73E8` fills start and normal end events;
red (`#D90000`) is reserved for blocker/error ends only.

```
Start event (40×40):  shape=mxgraph.bpmn.event;outline=standard;symbol=general;perimeter=ellipsePerimeter;
End event (40×40):    shape=mxgraph.bpmn.event;outline=end;symbol=general;
Step / task (120×60): rounded=1;whiteSpace=wrap;html=1;
Decision (50×50):     shape=mxgraph.bpmn.gateway2;perimeter=rhombusPerimeter;gwType=exclusive;
Sequence flow:        edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;
Sticky note:          shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#FFF2CC;strokeColor=#D6B656;
Amber [OPEN] tag:     text;html=1;fontColor=#B45309;fontStyle=1;   (place beside the affected step)
```

- One start event (no incoming edge); end events at the right edge (no outgoing edge).
- A gateway splits (≥2 outgoing) or merges (≥2 incoming) — never neither. Label outgoing branch
  edges (`value="Yes — inside window"`), and offset the label from the arrow so it never sits on
  a node border. Give branch labels room: the box after a gateway starts a full column later, the
  gateway's own label sits below the shape, branch labels sit above/below their edge — three
  distinct label positions that never stack.

## D. Layout grid

- Snap every coordinate to the 10px grid.
- Columns: steps advance left→right in 170px columns (120px box + 50px gap); one shared column
  grid across all lanes so simultaneous/handed-off steps line up vertically.
- 40px minimum gap between boxes, 20px lane inner padding, 40px page margin.
- `orthogonalEdgeStyle` routes edges at right angles; a cross-lane handoff drops straight down or
  up in the shared column, then continues.

## E. Inline validation checklist (run before every save)

1. XML well-formed; `mxGraphModel` uncompressed; `id="0"`/`id="1"` present and first.
2. All ids unique. Every `parent` resolves; in lane form steps parent to lanes and edges to `"1"`;
   in plain-flow form everything parents to `"1"`.
3. Every vertex has exactly one `mxGeometry` with sane bounds inside its lane.
4. Every edge's `source` and `target` resolve to existing vertices.
5. Exactly one start event; every path reaches an end event; every gateway splits or merges.
6. `<`, `>`, `&` in `value` attributes are XML-escaped.
7. Box count equals `.md` step count (+ events, gateways, branch-action boxes, notes) — nothing dropped, nothing invented.

Where a shell is available, `xmllint --noout <file>` (or `python3 -c "import xml.etree.ElementTree as
ET; ET.parse('<file>')"`) confirms point 1; the rest is read-and-check.

## F. Surgical edit protocol

1. Read the whole file first; inventory ids, positions, parentage, edges, notes.
2. New cells get new, non-colliding ids in the house naming scheme.
3. Rewire only the edges the change touches (an insert between A and B: retarget A→new, add
   new→B — two edges, no more).
4. Shift only downstream boxes in the touched lane, whole grid columns at a time.
5. Cells the change does not require stay byte-identical — position, id, style, label.
6. Re-run checklist E.
