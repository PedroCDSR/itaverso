"""Acha os sprites (componentes conectados) de um sheet de referência. Uso interno das pranchas de estudo."""
from collections import Counter, deque

import numpy as np
from PIL import Image


def componentes(caminho, minimo=150):
    im = Image.open(caminho).convert('RGB')
    a = np.array(im)
    fundo = Counter(map(tuple, a.reshape(-1, 3))).most_common(1)[0][0]
    m = np.abs(a.astype(int) - fundo).sum(2) > 30
    H, W = m.shape
    lab = np.zeros((H, W), int)
    n, out = 0, []
    for y in range(H):
        for x in range(W):
            if m[y, x] and not lab[y, x]:
                n += 1
                q = deque([(y, x)])
                lab[y, x] = n
                pts = []
                while q:
                    cy, cx = q.popleft()
                    pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            yy, xx = cy + dy, cx + dx
                            if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not lab[yy, xx]:
                                lab[yy, xx] = n
                                q.append((yy, xx))
                if len(pts) >= minimo:
                    ys = [p[0] for p in pts]
                    xs = [p[1] for p in pts]
                    out.append({'y': min(ys), 'x': min(xs), 'alt': max(ys) - min(ys) + 1,
                                'larg': max(xs) - min(xs) + 1, 'n': n,
                                'cores': len({tuple(a[p]) for p in pts})})
    return out, lab
