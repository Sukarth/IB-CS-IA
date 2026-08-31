"""
sync_mmd.py -- push .mmd text edits into a styled .drawio without losing layout.

draw.io stores the Mermaid source a diagram was built from inside the file
(mermaidData), so this compares that stored copy against the .mmd on disk and
rewrites only the affected row cells.  Every coordinate, colour and route is
left untouched -- unlike re-importing the Mermaid, which regenerates the shapes
and throws your arrangement away.

    python tools/sync_mmd.py Core/CoreUML.mmd Core/CoreUML.drawio

Safe by construction: it validates that every row in the diagram still matches
the stored Mermaid before touching anything, and refuses to run if classes or
members were added or removed (that genuinely needs a re-import).

Afterwards, re-export:
    drawio -x -f svg -o Core/CoreUML.svg Core/CoreUML.drawio
"""
import re, sys, json, html
import xml.etree.ElementTree as ET

FONTSTYLE = {'': 0, '$': 4, '*': 2}      # 4 = underline (static), 2 = italic (abstract)


def render(body):
    """mermaid member text -> the text draw.io displays

    Mermaid rewrites ~T~ as <T> and resolves its own #NN; entity codes, so
    "#95;#95;init#95;#95;" is displayed as "__init__".
    """
    body = re.sub(r'~([^~]*)~', r'<\1>', body)
    return re.sub(r'#(\d{1,5});', lambda m: chr(int(m.group(1))), body)


def parse_mmd(txt):
    """-> {class: [(displayed_text, classifier)]}"""
    classes, cur = {}, None
    for line in txt.splitlines():
        s = line.strip()
        m = re.match(r'^class\s+([A-Za-z_]\w*)\s*\{', s)
        if m:
            cur = m.group(1); classes[cur] = []; continue
        if cur is not None and s == '}':
            cur = None; continue
        if cur is None or not s or s.startswith('%%'):
            continue
        if re.match(r'^<<.+>>$', s):
            continue                                  # annotation has its own cell
        cl, b = '', s
        if b.endswith('$'):
            cl, b = '$', b[:-1]
        elif b.endswith('*'):
            cl, b = '*', b[:-1]
        classes[cur].append((render(b.rstrip()), cl))
    return classes


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def discover(mxfile):
    """-> {class: [(cell_id, current_value)]} in stack order, skipping separators/annotations"""
    root = ET.fromstring(mxfile)
    kids, nodes = {}, []
    for el in root.find('.//mxGraphModel/root'):
        c = el.find('mxCell') if el.tag == 'UserObject' else el
        if c is not None:
            kids.setdefault(c.get('parent'), []).append(el)
        if (el.get('mermaidId') or '').startswith('n:'):
            nodes.append(el)

    def style_of(el):
        c = el.find('mxCell') if el.tag == 'UserObject' else el
        return (c.get('style') or '') if c is not None else ''

    def bits_of(el):
        m = re.search(r'fontStyle=(\d+)', style_of(el))
        return int(m.group(1)) if m else 0

    out = {}
    for el in nodes:
        out[el.get('mermaidId')[2:]] = [
            (k.get('id'), k.get('value'), bits_of(k)) for k in kids.get(el.get('id'), [])
            if not style_of(k).startswith('line;') and 'align=center' not in style_of(k)]
    return out


def set_fontstyle(style, bits):
    style = re.sub(r'fontStyle=\d+;?', '', style)
    if bits:
        if style and not style.endswith(';'):
            style += ';'
        style += 'fontStyle=%d;' % bits
    return style


def patch_cell(mxfile, cid, value, bits):
    i = mxfile.find('<mxCell id="%s"' % cid)
    if i < 0:
        raise KeyError('cell %s not found' % cid)
    j = mxfile.index('>', i)
    tag = mxfile[i:j]
    new = re.sub(r'value="[^"]*"', 'value="%s"' % esc(value), tag)
    if new == tag:
        raise KeyError('no value attribute on %s' % cid)
    m = re.search(r'style="([^"]*)"', new)
    new = new[:m.start(1)] + esc(set_fontstyle(html.unescape(m.group(1)), bits)) + new[m.end(1):]
    return mxfile[:i] + new + mxfile[j:]


def main(mmd_path, drawio_path, out_path=None):
    out_path = out_path or drawio_path
    mxfile = open(drawio_path, encoding='utf-8').read()
    new_src = open(mmd_path, encoding='utf-8').read()

    md = re.search(r'mermaidData="([^"]*)"', mxfile)
    if not md:
        sys.exit('FATAL: no mermaidData in %s -- was it made by draw.io\'s Mermaid import?' % drawio_path)
    stored = json.loads(html.unescape(md.group(1)))

    old = parse_mmd(stored['data'])
    new = parse_mmd(new_src)
    struct = discover(mxfile)

    plan = []
    for cls, rows in struct.items():
        if cls not in old:                       # implicit class: an empty box, nothing to sync
            if rows:
                sys.exit('FATAL: %s has rows but is absent from the stored Mermaid' % cls)
            continue
        if cls not in new:
            sys.exit('FATAL: class %s was removed from the .mmd -- needs a re-import' % cls)
        o, n = old[cls], new[cls]
        if not (len(rows) == len(o) == len(n)):
            sys.exit('FATAL: %s member count changed (diagram=%d stored=%d mmd=%d) -- needs a re-import'
                     % (cls, len(rows), len(o), len(n)))
        for (cid, cur, cbits), (otxt, ocl), (ntxt, ncl) in zip(rows, o, n):
            # draw.io strips the $/* classifier from the text and encodes it as fontStyle
            if cur != otxt or cbits != FONTSTYLE[ocl]:
                sys.exit('FATAL: %s cell %s reads %r (fontStyle=%d) but stored Mermaid says %r '
                         '(fontStyle=%d) -- diagram edited by hand; re-sync manually'
                         % (cls, cid, cur, cbits, otxt, FONTSTYLE[ocl]))
            plan.append((cid, cur, cbits, ntxt, FONTSTYLE[ncl]))
    for cls in new:
        if cls not in struct:
            sys.exit('FATAL: new class %s is not in the diagram -- needs a re-import' % cls)

    changed = [p for p in plan if p[1] != p[3] or p[2] != p[4]]
    print('validated %d rows across %d classes; %d need updating'
          % (len(plan), len(struct), len(changed)))
    for cid, cur, cbits, ntxt, bits in changed:
        mxfile = patch_cell(mxfile, cid, ntxt, bits)

    stored['data'] = new_src.replace('\r\n', '\n')
    enc = esc(json.dumps(stored, indent=2)).replace('\n', '&#xa;')
    md = re.search(r'mermaidData="([^"]*)"', mxfile)
    mxfile = mxfile[:md.start(1)] + enc + mxfile[md.end(1):]

    ET.fromstring(mxfile)
    open(out_path, 'w', encoding='utf-8', newline='').write(mxfile)
    print('rows rewritten     : %d' % len(changed))
    print('statics underlined : %d' % sum(1 for p in changed if p[4] == 4))
    print('wrote %s -- now re-export with the drawio CLI' % out_path)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
