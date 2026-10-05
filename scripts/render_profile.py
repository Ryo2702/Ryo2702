"""Generate the README's 1-bit artwork: python3 scripts/render_profile.py."""

from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]


def panel(height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <style>
    text {{ font-family: 'Courier New', monospace; fill: #fff; }}
    .tile {{ animation: ink 8s steps(1, end) infinite; }}
    .step {{ animation: ink 10s steps(1, end) infinite; }}
    @keyframes ink {{ 0%, 70%, 100% {{ opacity: 1; }} 35%, 55% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .tile, .step {{ animation: none; }} }}
  </style>
  <rect width="960" height="{height}" fill="#000"/>
  <rect x="1" y="1" width="958" height="{height - 2}" fill="none" stroke="#fff" stroke-width="2"/>
  {body}
</svg>
'''


def render():
    # Binary tiles change discretely: no gradients, fades, or intermediate colors.
    tiles = []
    for row in range(8):
        for col in range(8):
            if (row * 3 + col * 5) % 7 < 4:
                tiles.append(
                    f'<rect class="tile" x="{706 + col * 26}" y="{32 + row * 26}" '
                    f'width="22" height="22" fill="#fff" '
                    f'style="animation-delay: -{(row + col) % 8}s"/>'
                )
    hero = panel(300, "Charles Aeron L. Pelayo — freelance web developer", '''
  <text x="32" y="48" font-size="16" letter-spacing="2">FREELANCE WEB DEVELOPER</text>
  <path d="M32 68H668 M686 32V236 M32 254H928" stroke="#fff" fill="none"/>
  <text x="28" y="135" font-size="64" font-weight="700" letter-spacing="-3">CHARLES</text>
  <text x="30" y="190" font-size="46" font-weight="700" letter-spacing="-2">AERON L. PELAYO</text>
  <text x="32" y="231" font-size="16">Practical systems. Responsive interfaces. Maintainable code.</text>
  <text x="32" y="281" font-size="14">WEB DEVELOPER / 2026</text>
  <text x="928" y="281" font-size="14" text-anchor="end">PHILIPPINES</text>
''' + "\n".join(tiles))

    steps = []
    for index, label in enumerate(("UNDERSTAND", "PLAN", "BUILD", "TEST", "IMPROVE")):
        x = index * 192
        steps.append(f'''
  <path d="M{x} 0V128" stroke="#fff"/>
  <text x="{x + 20}" y="37" font-size="14">0{index + 1}</text>
  <rect class="step" x="{x + 150}" y="23" width="20" height="20" fill="#fff" style="animation-delay: -{index * 2}s"/>
  <text x="{x + 20}" y="91" font-size="21" font-weight="700">{label}</text>''')
    workflow = panel(128, "Understand → Plan → Build → Test → Improve", "\n".join(steps))
    return {"profile.svg": hero, "workflow.svg": workflow}


def check(artwork):
    """Small runnable check for valid, monochrome, accessible generated panels."""
    for svg in artwork.values():
        root = ElementTree.fromstring(svg)
        assert root.find("{http://www.w3.org/2000/svg}title").text
        assert "prefers-reduced-motion: reduce" in svg
        for element in root.iter():
            for attribute in ("fill", "stroke"):
                assert element.get(attribute, "none") in ("#000", "#fff", "none")
        assert "animation-delay:" in svg


if __name__ == "__main__":
    artwork = render()
    check(artwork)
    (ROOT / "assets").mkdir(exist_ok=True)
    for name, svg in artwork.items():
        (ROOT / "assets" / name).write_text(svg, encoding="utf-8")
    print("Generated and checked 2 monochrome SVGs.")
