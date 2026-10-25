"""Tiny Excalidraw scene builder (no dependencies except Pillow/fontTools for text measuring)."""
import base64, glob, io, json, math, os, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
# node_modules is shared with the first deck (system-one-models/presentation/tools); nothing is installed here
SHARED = os.path.abspath(os.path.join(HERE, "..", "..", "..", "system-one-models", "presentation", "tools"))
FONT_FAMILY = 5  # Excalifont (hand-drawn, default in current Excalidraw)
LINE_H = 1.25
INK = "#1e1e1e"

_font_cache = {}


def _font(size):
    from PIL import ImageFont
    ttf = os.path.join(HERE, ".cache", "Excalifont.ttf")
    if not os.path.exists(ttf):
        from fontTools.ttLib import TTFont
        os.makedirs(os.path.dirname(ttf), exist_ok=True)
        src = sorted(glob.glob(os.path.join(SHARED, "node_modules/@excalidraw/excalidraw/dist/prod/fonts/Excalifont/*.woff2")),
                     key=os.path.getsize)[-1]
        f = TTFont(src); f.flavor = None; f.save(ttf)
    if size not in _font_cache:
        _font_cache[size] = ImageFont.truetype(ttf, size)
    return _font_cache[size]


def measure(text, size):
    """(width, height) of text as Excalidraw lays it out (emoji approximated as 1.15 em)."""
    f = _font(size)
    w = 0
    for line in text.split("\n"):
        lw = 0
        for ch in line:
            lw += size * 1.15 if ord(ch) > 0x2000 else f.getlength(ch)
        w = max(w, lw)
    return math.ceil(w), math.ceil(len(text.split("\n")) * size * LINE_H)


class Scene:
    def __init__(self, seed=7):
        self.elements, self.files, self.frames = [], {}, []
        self.rnd = random.Random(seed)
        self._n = 0
        self.frame_id = None
        self.ox = self.oy = 0

    # ---- ids / base ----
    def _id(self, p):
        self._n += 1
        return f"{p}{self._n:04d}"

    def _base(self, typ, x, y, w, h, **kw):
        e = dict(id=self._id(typ[:3]), type=typ, x=self.ox + x, y=self.oy + y, width=w, height=h, angle=kw.pop("angle", 0),
                 strokeColor=kw.pop("stroke", INK), backgroundColor=kw.pop("fill", "transparent"),
                 fillStyle=kw.pop("fillStyle", "solid"), strokeWidth=kw.pop("sw", 3), strokeStyle=kw.pop("style", "solid"),
                 roughness=kw.pop("rough", 1), opacity=kw.pop("opacity", 100), groupIds=[], frameId=self.frame_id,
                 roundness=kw.pop("roundness", None), seed=self.rnd.randint(1, 2**31 - 1), version=1,
                 versionNonce=self.rnd.randint(1, 2**31 - 1), isDeleted=False, boundElements=None,
                 updated=int(time.time() * 1000), link=None, locked=False)
        e.update(kw)
        self.elements.append(e)
        return e

    # ---- frames ----
    def frame(self, name, x, y, w=1600, h=900, bg="#ffffff"):
        self.frame_id = None
        self.ox = self.oy = 0
        fr = self._base("frame", x, y, w, h, name=name, stroke="#bbbbbb", sw=2, rough=0)
        self.frames.append(fr)
        self.frame_id = fr["id"]
        self.ox, self.oy = x, y
        self.rect(0, 0, w, h, fill=bg, stroke=bg, sw=1, rough=0, roundness=None)  # background
        return fr

    # ---- shapes (coordinates are relative to the current frame) ----
    def rect(self, x, y, w, h, fill="transparent", stroke=INK, round_=True, **kw):
        kw.setdefault("roundness", {"type": 3} if round_ else None)
        return self._base("rectangle", x, y, w, h, fill=fill, stroke=stroke, **kw)

    def ellipse(self, x, y, w, h, fill="transparent", stroke=INK, **kw):
        return self._base("ellipse", x, y, w, h, fill=fill, stroke=stroke, roundness={"type": 2}, **kw)

    def diamond(self, x, y, w, h, fill="transparent", stroke=INK, **kw):
        return self._base("diamond", x, y, w, h, fill=fill, stroke=stroke, roundness={"type": 2}, **kw)

    def line(self, pts, stroke=INK, fill="transparent", closed=False, **kw):
        pts = [list(p) for p in pts]
        if closed and pts[0] != pts[-1]:
            pts.append(pts[0])
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, y0 = min(xs), min(ys)
        rel = [[p[0] - xs[0], p[1] - ys[0]] for p in pts]
        e = self._base("line", xs[0], ys[0], max(xs) - x0, max(ys) - y0, stroke=stroke, fill=fill,
                       points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
                       startArrowhead=None, endArrowhead=None, roundness=kw.pop("roundness", {"type": 2}), **kw)
        return e

    def arrow(self, pts, stroke=INK, head="arrow", tail=None, **kw):
        pts = [list(p) for p in pts]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        rel = [[p[0] - xs[0], p[1] - ys[0]] for p in pts]
        return self._base("arrow", xs[0], ys[0], max(xs) - min(xs), max(ys) - min(ys), stroke=stroke, points=rel,
                          lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=tail,
                          endArrowhead=head, elbowed=False, roundness=kw.pop("roundness", {"type": 2}), **kw)

    def text(self, x, y, s, size=48, color=INK, align="left", **kw):
        """x is the left edge (align=left), the centre (align=center) or the right edge (align=right)."""
        w, h = measure(s, size)
        left = x if align == "left" else x - w / 2 if align == "center" else x - w
        return self._base("text", left, y, w, h, stroke=color, text=s, originalText=s, fontSize=size,
                          fontFamily=FONT_FAMILY, textAlign=align, verticalAlign="top", containerId=None,
                          autoResize=True, lineHeight=LINE_H, **kw)

    def label(self, cx, cy, s, size=48, color=INK, **kw):
        """text centred on a point"""
        w, h = measure(s, size)
        return self.text(cx, cy - h / 2, s, size, color, "center", **kw)

    def box(self, x, y, w, h, s, size=44, fill="#ffffff", stroke=INK, color=INK, **kw):
        r = self.rect(x, y, w, h, fill=fill, stroke=stroke, **kw)
        self.label(x + w / 2, y + h / 2, s, size, color)
        return r

    # ---- images ----
    def image(self, path, x, y, w, h):
        """Embed an image (PNG/JPG) contained in the box x,y,w,h, centred."""
        from PIL import Image
        im = Image.open(path).convert("RGBA")
        im.thumbnail((1200, 1200))
        iw, ih = im.size
        k = min(w / iw, h / ih)
        dw, dh = iw * k, ih * k
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        fid = base64.b32encode(os.urandom(10)).decode().lower()
        self.files[fid] = {"mimeType": "image/png", "id": fid, "created": int(time.time() * 1000),
                           "dataURL": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}
        return self._base("image", x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, fileId=fid, status="saved",
                          scale=[1, 1], crop=None)

    # ---- output ----
    def to_json(self):
        return {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
                "elements": self.elements,
                "appState": {"viewBackgroundColor": "#f1f3f5", "gridSize": None},
                "files": self.files}


def validate(scene_json):
    """Structural checks for a .excalidraw scene; returns list of problems."""
    probs, ids = [], set()
    need = {"id", "type", "x", "y", "width", "height", "angle", "strokeColor", "backgroundColor", "fillStyle", "strokeWidth",
            "strokeStyle", "roughness", "opacity", "groupIds", "seed", "version", "versionNonce", "isDeleted"}
    if scene_json.get("type") != "excalidraw":
        probs.append("type != excalidraw")
    frames = {e["id"] for e in scene_json["elements"] if e["type"] == "frame"}
    for e in scene_json["elements"]:
        if e["id"] in ids: probs.append(f"duplicate id {e['id']}")
        ids.add(e["id"])
        miss = need - set(e)
        if miss: probs.append(f"{e['id']} missing {miss}")
        if e["type"] in ("line", "arrow") and len(e.get("points", [])) < 2: probs.append(f"{e['id']} <2 points")
        if e["type"] == "text" and not e.get("text"): probs.append(f"{e['id']} empty text")
        if e.get("frameId") and e["frameId"] not in frames: probs.append(f"{e['id']} bad frameId")
        if e["type"] == "image" and e["fileId"] not in scene_json["files"]: probs.append(f"{e['id']} missing file")
        for k in ("x", "y", "width", "height"):
            if not isinstance(e[k], (int, float)) or e[k] != e[k]: probs.append(f"{e['id']} bad {k}")
    return probs
