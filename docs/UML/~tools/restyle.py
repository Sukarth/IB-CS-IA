"""Recolour a fresh drawio-mermaid export into the exact Core theme.

Works on the mxfile XML by rewriting style= attributes only; every coordinate,
route and waypoint drawio computed is left untouched.
"""
import re, sys, html

BASE_FILL   = 'light-dark(#ECECFF,#1f2020)'
BASE_STROKE = 'light-dark(#9370DB,#cccccc)'
BASE_FONT   = 'light-dark(#333333,#cccccc)'
BASE_EDGE   = 'light-dark(#333333,#cccccc)'
BASE_LBLBG  = 'light-dark(#ECECFF,#1f2020)'

TITLE_FILL, STROKE, TEXT, EDGE_STROKE = '#F5AB50', '#909090', '#1A1A1A', '#182E3E'
FAM = 'Trebuchet MS,Verdana,Arial,sans-serif'


def kv(style):
    """style string -> list of (key, value|None) preserving order"""
    out = []
    for part in style.split(';'):
        if not part:
            continue
        if '=' in part:
            k, v = part.split('=', 1)
            out.append([k, v])
        else:
            out.append([part, None])
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
    p = kv(style)
    d = {k: v for k, v in p}
    head = p[0][0]

    if head == 'swimlane':
        setk(p, 'fillColor', TITLE_FILL)
        setk(p, 'strokeColor', STROKE)
        setk(p, 'fontColor', TEXT)
        setk(p, 'labelBackgroundColor', 'none')
        setk(p, 'rounded', '1')
        return dump(p), 'class'

    if head == 'line':
        setk(p, 'strokeColor', STROKE)
        setk(p, 'labelBackgroundColor', 'none')
        setk(p, 'fontColor', TEXT)
        setk(p, 'rounded', '1')
        return dump(p), 'sep'

    if head == 'text':
        setk(p, 'fontColor', TEXT)
        setk(p, 'labelBackgroundColor', 'none')
        setk(p, 'rounded', '1')
        return dump(p), 'row'

    if head == 'edgeLabel':
        setk(p, 'fontColor', TEXT)
        setk(p, 'rounded', '1')
        return dump(p), 'cardinality'

    if head == 'group':
        setk(p, 'labelBackgroundColor', 'none')
        setk(p, 'fontColor', TEXT)
        setk(p, 'rounded', '1')
        return dump(p), 'group'

    # everything else with a stroke is an edge
    if 'strokeColor' in d:
        setk(p, 'strokeColor', EDGE_STROKE)
        setk(p, 'html', '1')
        setk(p, 'fontSize', '19')
        setk(p, 'labelBackgroundColor', '#FFFFFF')
        setk(p, 'fontFamily', FAM)
        setk(p, 'fontColor', 'default')
        setk(p, 'rounded', '1')
        return dump(p), 'edge'
    return style, None


def main(src, out):
    mx = open(src, encoding='utf-8').read()
    counts = {}
    # only touch style="..." that live on <mxCell ...>, never mermaidBaseStyle
    def sub(m):
        raw = html.unescape(m.group(1))
        new, kind = restyle(raw)
        if kind:
            counts[kind] = counts.get(kind, 0) + 1
        return 'style="%s"' % (new.replace('&', '&amp;').replace('<', '&lt;')
                                  .replace('>', '&gt;').replace('"', '&quot;'))
    mx2 = re.sub(r'(?<!Base)style="([^"]*)"', sub, mx)
    open(out, 'w', encoding='utf-8', newline='').write(mx2)
    print('restyled:', counts)
    print('mermaidBaseStyle left intact:', mx2.count('mermaidBaseStyle='))
    for name, col in (('orange title', TITLE_FILL), ('grey stroke', STROKE),
                      ('text', TEXT), ('edge', EDGE_STROKE)):
        print('  %-14s %-8s x%d' % (name, col, mx2.count(col)))
    for b in (BASE_FILL, BASE_STROKE, BASE_EDGE):
        n = len(re.findall(re.escape(b), mx2))
        base_only = len(re.findall(re.escape(b), mx2[:]))
        print('  leftover %-34s x%d  (expected: only inside mermaidBaseStyle)' % (b, n))
    print('wrote', out)


if __name__ == '__main__':
    main(*sys.argv[1:])
