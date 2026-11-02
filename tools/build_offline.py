"""Build periodic-table.html: a single file that runs with no internet connection.

Inlines Three.js r128, OrbitControls and the three web fonts (as base64 woff2) into index.html.

Usage:
  python3 tools/build_offline.py <three-package-dir> <fonts-dir> [output]
    three-package-dir: unpacked `npm pack three@0.128.0` (the folder containing build/ and examples/)
    fonts-dir: folder holding the @fontsource latin woff2 files listed in FONTS below
"""
import base64, os, re, sys

three_dir, fonts_dir = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else "periodic-table.html"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(root, "index.html"), encoding="utf-8").read()

FONTS = [  # (family, weight, file)
    ("Unbounded", 500, "unbounded-latin-500-normal.woff2"),
    ("Unbounded", 700, "unbounded-latin-700-normal.woff2"),
    ("Unbounded", 800, "unbounded-latin-800-normal.woff2"),
    ("Atkinson Hyperlegible", 400, "atkinson-hyperlegible-latin-400-normal.woff2"),
    ("Atkinson Hyperlegible", 700, "atkinson-hyperlegible-latin-700-normal.woff2"),
    ("JetBrains Mono", 500, "jetbrains-mono-latin-500-normal.woff2"),
    ("JetBrains Mono", 700, "jetbrains-mono-latin-700-normal.woff2"),
]
faces = []
for fam, w, f in FONTS:
    data = base64.b64encode(open(os.path.join(fonts_dir, f), "rb").read()).decode()
    faces.append(f'@font-face {{ font-family: "{fam}"; font-style: normal; font-weight: {w}; font-display: block; '
                 f'src: url(data:font/woff2;base64,{data}) format("woff2"); }}')

# 1) drop the Google Fonts links, add embedded @font-face rules
html, n = re.subn(r'<link rel="(?:preconnect|stylesheet)" href="https://fonts\.g[^"]*"(?: crossorigin)?>\n', "", html)
assert n == 3, n
html = html.replace("<style>\n", "<style>\n/* Embedded fonts (offline) */\n" + "\n".join(faces) + "\n", 1)

# 2) inline the two scripts
def inline(tag, path):
    global html
    code = open(path, encoding="utf-8").read()
    assert "</script" not in code.lower()
    assert tag in html, tag
    html = html.replace(tag, "<script>\n" + code + "\n</script>", 1)

inline('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
       os.path.join(three_dir, "build", "three.min.js"))
inline('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>',
       os.path.join(three_dir, "examples", "js", "controls", "OrbitControls.js"))

# 3) offline message wording + build markers
html = html.replace("The 3D library couldn't load. Check your internet connection and reload the page.",
                    "The 3D library couldn't start. Try opening this file in Chrome or Edge.")
html = html.replace("<!--@FRAGMENT-START@-->\n", "").replace("<!--@FRAGMENT-END@-->\n", "")
assert "https://" not in re.sub(r"<script>.*?</script>", "", html, flags=re.S).replace('href="https://', ''), "external URL left"
open(os.path.join(root, out), "w", encoding="utf-8").write(html)
print(f"wrote {out}: {len(html.encode()) / 1024:.0f} KB")
