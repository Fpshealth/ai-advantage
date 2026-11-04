# Pictures

Show real output, real values and screenshots of the real object in place of drawings or descriptions. `scripts/lint.py` checks the markup below.

## In the HTML

Put each picture in a `<figure>` with a `<figcaption>` that gives its one takeaway. A section without a picture carries its reason on the heading: `<h2 data-no-picture="a sentence says it as fast">`.

## Screenshots

A screenshot shows a real screen the reader will meet. Take it from the images the person already gave you (in the input area or a connected source). If this session has a browser tool and the screen is a public page, you may capture it yourself. Do not ask the person to take a screenshot. If no image of the screen exists, show the section with a diagram or real output instead, and give the picture plan that kind.

Crop to the part the text talks about, and mark the spot the reader must look at. Open every image before you embed it, and remove passwords, keys and personal data. Save images as files next to the HTML (copy them to the output area with the page), not as `data:` URIs.

## Diagrams

Draw each diagram as inline SVG in the page, top-down, with boxes labelled by the real names from the inventory. Use the `artifact-diagramming` skill if this session has it. Text in a diagram must render at 11 px or more; the `--render` check measures it.

## Animations

Let the reader step through with Back and Next buttons; do not autoplay. Before the first step, show the whole picture. Write each step's label as page text, not inside an image. When the reader's system asks for reduced motion (`prefers-reduced-motion`), show all steps without motion.

To show a real screen that changes (a click, a build log), use a recording from the inputs if one exists, and embed a short `<video controls muted>` with a caption that says what to watch for.
