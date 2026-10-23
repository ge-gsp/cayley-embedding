"""The repo's index.html is the canonical file.  The Claude artifact harness
supplies its own document skeleton, so strip ours when republishing there."""
import io, os, re
root = os.path.join(os.path.dirname(__file__), '..')
s = io.open(os.path.join(root, 'index.html'), encoding='utf-8').read()
s = re.sub(r'^<!doctype html>\n<html lang="en">\n<head>\n'
           r'<meta charset="utf-8">\n<meta name="viewport"[^\n]*\n', '', s)
s = s.replace('</style>\n</head>\n<body>\n', '</style>\n', 1)
s = re.sub(r'\n</body>\n</html>\n$', '\n', s)
s = s.replace('<title>Cayley Embedding Workbench — GE-GSP</title>',
              '<title>Cayley Embedding Workbench</title>\n'
              '<meta name="claude:viewport-fit-sides" content="cover">', 1)
out = '/home/claude/app/index.html'
io.open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, len(s), 'bytes')
