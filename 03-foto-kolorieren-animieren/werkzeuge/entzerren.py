"""Abzug auf dem Tisch finden (weißer Rand), Perspektive entzerren und auf das Bild ohne Rand zuschneiden.

Aufruf: python entzerren.py <eingabe> <ausgabe> [rand_px]
"""
import sys

import numpy as np
from PIL import Image


def randlinie(maske, achse, von_vorn):
    """Für jede Zeile bzw. Spalte die erste weiße Stelle von außen; Gerade per Median-Fit."""
    m = maske if achse == 0 else maske.T
    if not von_vorn:
        m = m[::-1]
    treffer = m.argmax(axis=0).astype(float)
    gueltig = m.any(axis=0)
    idx = np.arange(m.shape[1])[gueltig]
    pos = treffer[gueltig]
    if not von_vorn:
        pos = m.shape[0] - 1 - pos
    rand = len(idx) // 10
    idx, pos = idx[rand:-rand], pos[rand:-rand]
    a, b = np.polyfit(idx, pos, 1)
    rest = np.abs(pos - (a * idx + b))
    gut = rest < np.percentile(rest, 70)
    return np.polyfit(idx[gut], pos[gut], 1)


def schnitt(waag, senk):
    # waag: y = a*x + b, senk: x = c*y + d
    a, b = waag
    c, d = senk
    y = (a * d + b) / (1 - a * c)
    return c * y + d, y


def koeffizienten(ziel, quelle):
    zeilen = []
    for (x, y), (u, v) in zip(ziel, quelle):
        zeilen.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        zeilen.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(zeilen, float), np.array(quelle, float).reshape(8))


def main():
    ein, aus = sys.argv[1], sys.argv[2]
    rand_px = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    bild = Image.open(ein).convert('RGB')
    a = np.asarray(bild).astype(int)
    hell = a.min(axis=2)
    bunt = a.max(axis=2) - a.min(axis=2)
    weiss = (hell > 185) & (bunt < 30)
    oben = randlinie(weiss, 0, True)
    unten = randlinie(weiss, 0, False)
    links = randlinie(weiss, 1, True)
    rechts = randlinie(weiss, 1, False)
    ecken = [schnitt(oben, links), schnitt(oben, rechts), schnitt(unten, rechts), schnitt(unten, links)]
    print('Ecken', [(round(x), round(y)) for x, y in ecken])
    breite = int(np.hypot(*np.subtract(ecken[1], ecken[0])))
    hoehe = int(np.hypot(*np.subtract(ecken[3], ecken[0])))
    k = koeffizienten([(0, 0), (breite, 0), (breite, hoehe), (0, hoehe)], ecken)
    gerade = bild.transform((breite, hoehe), Image.PERSPECTIVE, tuple(k), Image.BICUBIC)
    r = int(rand_px)
    if r:
        gerade = gerade.crop((r, r, breite - r, hoehe - r))
    gerade.save(aus, quality=95)
    print('Größe', gerade.size)


if __name__ == '__main__':
    main()
