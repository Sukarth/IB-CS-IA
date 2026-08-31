"""
fix_arrows.py -- replace draw.io's Mermaid-only arrowheads with built-in UML ones.

When draw.io imports Mermaid it uses two custom markers, `mermaidExtension`
(generalisation) and `mermaidDiamond` (composition).  Those stencils are only
registered while the Mermaid module is loaded, so everywhere else -- headless
CLI export, plain SVG/PNG, reopening the file later -- they render as *nothing*
and those edges lose their heads entirely.  `classic` is unaffected.

This swaps them for the standard markers, which render everywhere:

    mermaidExtension -> block       + Fill=0   (hollow triangle, generalisation)
    mermaidDiamond   -> diamondThin + Fill=1   (filled diamond,  composition)

Idempotent; run after any fresh Mermaid import.

    python ~tools/fix_arrows.py Core/CoreUML.drawio ADT/ADTUML.drawio
"""
import re, sys
import xml.etree.ElementTree as ET

MAP = {'mermaidExtension': ('block', '0'), 'mermaidDiamond': ('diamondThin', '1')}


def fix_style(style):
    n = 0
    for end in ('start', 'end'):
        m = re.search(r'\b%sArrow=(\w+)' % end, style)
        if not m or m.group(1) not in MAP:
            continue
        shape, fill = MAP[m.group(1)]
        style = style[:m.start(1)] + shape + style[m.end(1):]
        if re.search(r'\b%sFill=' % end, style):
            style = re.sub(r'\b%sFill=\d' % end, '%sFill=%s' % (end, fill), style)
        else:
            style = style.rstrip(';') + ';%sFill=%s;' % (end, fill)
        n += 1
    return style, n


def main(paths):
    for p in paths:
        s = open(p, encoding='utf-8').read()
        total = [0]

        def sub(m):
            new, n = fix_style(m.group(1))
            total[0] += n
            return 'style="%s"' % new

        # (?<!Base) keeps mermaidBaseStyle untouched so draw.io still knows the original
        s2 = re.sub(r'(?<!Base)style="([^"]*)"', sub, s)
        ET.fromstring(s2)
        open(p, 'w', encoding='utf-8', newline='').write(s2)
        left = len(re.findall(r'(?<!Base)style="[^"]*mermaid(?:Extension|Diamond)', s2))
        print('%-24s markers replaced: %-3d  mermaid-only markers left: %d'
              % (p, total[0], left))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
