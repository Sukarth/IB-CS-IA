"""
restyle_erd.py -- put a draw.io ER diagram into the same palette as the UML ones.

draw.io's Mermaid erDiagram import uses shape=table / tableRow /
partialRectangle rather than swimlanes, so the UML restyle.py doesn't touch it.

    header row      #ECECFF lavender -> #F5AB50 orange   (matches UML titles)
    banded rows     #F1F1FF pale     -> #FCEAD3          (#F5AB50 at 25% on white)
    plain rows      #ffffff          -> #FFFFFF
    borders         #9370DB          -> #909090
    text            #333333          -> #1A1A1A
    edges           #333333          -> #182E3E, label background white

Font sizes are left alone: the ER edge labels are 14 and re-sizing them to the
UML's 19 would change how the routed labels sit.  mermaidBaseStyle is untouched.

    python ~tools/restyle_erd.py docs/ERD/ERD.drawio
"""
import re, sys
import xml.etree.ElementTree as ET

ORANGE, TINT, WHITE = '#F5AB50', '#FCEAD3', '#FFFFFF'
STROKE, TEXT, EDGE = '#909090', '#1A1A1A', '#182E3E'
BANDED = '#F1F1FF'          # the pale band draw.io alternates in


def kv(style):
    out = []
    for part in style.split(';'):
        if not part:
            continue
        k, _, v = part.partition('=')
        out.append([k, v if _ else None])
    return out


def dump(pairs):
    return ''.join((k if v is None else '%s=%s' % (k, v)) + ';' for k, v in pairs)


def setk(pairs, key, val):
    for p in pairs:
        if p[0] == key:
            p[1] = val
            return
    pairs.append([key, val])


def restyle(style):
    if not style:
        return style, None
    head = style.split(';')[0]
    p = kv(style)

    if head == 'shape=table':
        setk(p, 'fillColor', ORANGE)
        setk(p, 'strokeColor', STROKE)
        setk(p, 'fontColor', TEXT)
        return dump(p), 'table header'

    if head == 'shape=tableRow':
        setk(p, 'fillColor', TINT if BANDED in style else WHITE)
        return dump(p), 'banded row' if BANDED in style else 'plain row'

    if head == 'shape=partialRectangle':
        setk(p, 'strokeColor', STROKE)
        setk(p, 'fontColor', TEXT)
        return dump(p), 'cell'

    if 'Arrow=ER' in style:
        setk(p, 'strokeColor', EDGE)
        setk(p, 'fontColor', TEXT)
        setk(p, 'labelBackgroundColor', WHITE)
        return dump(p), 'edge'

    return style, None


def main(paths):
    for path in paths:
        s = open(path, encoding='utf-8').read()
        counts = {}

        def sub(m):
            new, kind = restyle(m.group(1))
            if kind:
                counts[kind] = counts.get(kind, 0) + 1
            return 'style="%s"' % new.replace('&', '&amp;').replace('<', '&lt;') \
                                     .replace('>', '&gt;').replace('"', '&quot;')

        s2 = re.sub(r'(?<!Base)style="([^"]*)"', sub, s)
        ET.fromstring(s2)
        open(path, 'w', encoding='utf-8', newline='').write(s2)
        print('%s' % path)
        for k in sorted(counts):
            print('   %-14s x%d' % (k, counts[k]))
        left = len(re.findall(r'(?<!Base)style="[^"]*(?:9370DB|ECECFF|F1F1FF)', s2))
        print('   old palette remaining in live styles: %d' % left)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
