"""
force_light.py -- pin a .drawio to fixed light-mode colours.

draw.io writes theme-adaptive colours as light-dark(<light>,<dark>) and, when
exported with the default --theme auto, wraps *every* colour that way and adds
`color-scheme: light dark` to the SVG.  The result changes appearance depending
on the viewer's OS/browser theme -- fine on screen, bad for a document.

This collapses every light-dark() pair in the *live* styles down to its light
value and pins the canvas background to white, so the file itself is
unambiguous.  mermaidBaseStyle is deliberately left alone: it records what
draw.io's Mermaid import originally produced.

Pair this with `--theme light` on export, which is what actually stops draw.io
re-deriving dark variants:

    python ~tools/force_light.py Core/CoreUML.drawio
    drawio -x -f svg --theme light -o Core/CoreUML.svg Core/CoreUML.drawio
"""
import re, sys
import xml.etree.ElementTree as ET

LD = re.compile(r'light-dark\(\s*([^,)]+?)\s*,\s*[^)]*\)')


def main(paths):
    for p in paths:
        s = open(p, encoding='utf-8').read()
        n = [0]

        def sub(m):
            style, k = LD.subn(lambda x: x.group(1), m.group(1))
            n[0] += k
            return 'style="%s"' % style

        s2 = re.sub(r'(?<!Base)style="([^"]*)"', sub, s)

        # pin the canvas background (Core had light-dark, ADT had none at all)
        if re.search(r'<mxGraphModel[^>]*\sbackground="[^"]*"', s2):
            s2 = re.sub(r'(<mxGraphModel[^>]*\sbackground=")[^"]*(")', r'\1#FFFFFF\2', s2)
            bg = 'replaced'
        else:
            s2 = re.sub(r'<mxGraphModel', '<mxGraphModel background="#FFFFFF"', s2, count=1)
            bg = 'added'

        ET.fromstring(s2)
        open(p, 'w', encoding='utf-8', newline='').write(s2)
        live = len(re.findall(r'(?<!Base)style="[^"]*light-dark', s2))
        print('%-22s light-dark collapsed: %-4d background: %-9s live styles still adaptive: %d'
              % (p, n[0], bg, live))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
