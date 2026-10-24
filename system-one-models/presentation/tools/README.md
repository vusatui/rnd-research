# Tools for the Excalidraw deck

```bash
cd system-one-models/presentation/tools
npm install                       # @excalidraw/excalidraw, react, puppeteer-core, esbuild
npx esbuild export_entry.js --bundle --format=iife --outfile=dist/export_bundle.js \
  --define:process.env.NODE_ENV='"production"' --define:process.env.IS_PREACT='"false"' --loader:.woff2=file --log-level=warning
pip install pillow fonttools brotli
python3 build_deck.py             # writes ../presentation.excalidraw (validates the JSON structure)
node export_frames.mjs            # renders every frame with the real Excalidraw renderer -> ../export/*.svg|png (needs google-chrome)
python3 contact_sheet.py          # ../contact-sheet.png
python3 make_pdf.py               # ../presentation.pdf
```

- `excal.py`: tiny scene builder + structural validator (required fields, unique ids, frame ids, image files).
- `build_deck.py`: all 18 slides. Illustration slots (`slot("name", ...)`) become real images when `../images/<name>.png` exists, otherwise dashed placeholders.
- Fonts are Excalidraw's own (Excalifont), so the export looks the same as in the editor.
