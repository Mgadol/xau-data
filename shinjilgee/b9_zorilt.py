"""b9. Задарсны ДАРАА — дээш хэр, доош хэр явах вэ?

b8 «хэр шахагдвал хэр хол явдаг» гэдгийг өгсөн. Гэхдээ тэр нь хоёр
талын ХАМГИЙН ХОЛЫГ авсан — арилжаанд орсны дараа юу болохыг хэлэхгүй.

Энд задралыг БАРЬЖ АВСНЫ дараах зургийг гаргана. Лааны бүтэц уншиж
чиглэлээ сонгосон хүнд хэрэгтэй гурван тоо:

    ҮРГЭЛЖЛЭЛ (MFE) — эвдэрсэн түвшнээс цааш хэр явдаг
    ТАТАЛТ    (MAE) — эсрэгээрээ хэр татдаг (стоп энэ доор байх ёстой)
    ЭРГЭЛТ          — эсрэг талыг нь ч эвдчихэж байна уу (хуурамч задрал)

Бүгд ATR-ийн дахинаар — 2005 оны $450, 2026 оны $4 800 зэрэгцүүлэгдэнэ.

ЭРГЭЛТИЙН хувь нь хамгийн чухал нь: хэрэв задралын 40% нь эргээд
эсрэг талыг эвдэж байвал «задрал» гэдэг дохио өөрөө сул гэсэн үг.

Медиан ба дундажийг ХОЁУЛАНГ нь харуулна. Цөөн том хөдөлгөөн
дундажийг татдаг — медиан нь «ердийн тохиолдол» юу болохыг хэлнэ.

    python3 b9_zorilt.py [--hold 10]
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

RNG = 10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hold', type=int, default=10,
                    help='задарсны дараа хэдэн хоног хардаг')
    ap.add_argument('--wait', type=int, default=5)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d['up'] = d.high.rolling(RNG).max()
    d['dn'] = d.low.rolling(RNG).min()
    d = d.dropna(subset=['sq', 'up', 'atr14'])

    H, L = d.high.to_numpy(), d.low.to_numpy()
    U, D, A = d.up.to_numpy(), d.dn.to_numpy(), d.atr14.to_numpy()
    sq = d.sq.to_numpy()
    n = len(d)
    rows = []

    for i in range(n):
        lvl = side = ej = None
        for j in range(i + 1, min(i + 1 + a.wait, n)):
            hu, hd = H[j] >= U[i], L[j] <= D[i]
            if hu and hd:
                break                          # аль нь эхэлснийг мэдэхгүй
            if hu:
                lvl, side, ej = U[i], 1, j
                break
            if hd:
                lvl, side, ej = D[i], -1, j
                break
        if lvl is None:
            continue
        k = min(ej + a.hold, n)
        hh, ll = H[ej:k].max(), L[ej:k].min()
        mfe = (hh - lvl) / A[i] if side > 0 else (lvl - ll) / A[i]
        mae = (lvl - ll) / A[i] if side > 0 else (hh - lvl) / A[i]
        # Эсрэг талын түвшнийг ч эвдсэн үү
        rev = (ll <= D[i]) if side > 0 else (hh >= U[i])
        rows.append((d.index[i], sq[i], side, mfe, max(mae, 0), int(rev)))

    t = pd.DataFrame(rows, columns=['date', 'sq', 'side', 'mfe', 'mae', 'rev'])
    t['bin'] = pd.qcut(t.sq, 5, labels=False)
    names = ['1 хамгийн шахагдсан', '2', '3 хэвийн', '4', '5 хамгийн тэлсэн']

    print(f'{len(t):,} задрал   2005 → 2026   '
          f'{a.wait} хоног хүлээж, {a.hold} хоног хардаг')
    print('Бүх тоо ATR-ийн ДАХИНААР\n')
    print(f'{"бүлэг":22} {"ҮРГЭЛЖЛЭЛ":>19} {"ТАТАЛТ":>17} '
          f'{"эргэсэн":>9} {"n":>6}')
    print(f'{"":22} {"медиан":>9} {"дундаж":>9} {"медиан":>8} {"дундаж":>8}')
    print('─' * 80)
    for b in range(5):
        g = t[t.bin == b]
        print(f'{names[b]:22} {g.mfe.median():9.2f} {g.mfe.mean():9.2f} '
              f'{g.mae.median():8.2f} {g.mae.mean():8.2f} '
              f'{g.rev.mean():9.0%} {len(g):6}')

    lo, hi = t[t.bin == 0], t[t.bin == 4]
    print(f'\n  Шахагдсан vs тэлсэн:')
    print(f'    үргэлжлэл (медиан) {lo.mfe.median():.2f} vs {hi.mfe.median():.2f}'
          f'   → {lo.mfe.median() / hi.mfe.median():.2f} дахин')
    print(f'    таталт    (медиан) {lo.mae.median():.2f} vs {hi.mae.median():.2f}')
    print(f'    үргэлжлэл ÷ таталт {lo.mfe.median() / max(lo.mae.median(), .01):.2f}'
          f' vs {hi.mfe.median() / max(hi.mae.median(), .01):.2f}   ← ГОЛ харьцаа')
    print(f'    хуурамч задрал     {lo.rev.mean():.0%} vs {hi.rev.mean():.0%}')

    print('\n  Шахагдсан бүлэг — үргэлжлэл хэдэн хувьд хүрэх вэ:')
    for x in (1, 2, 3, 4):
        print(f'    {x} ATR+ : {(lo.mfe >= x).mean():5.0%}'
              f'   (тэлсэн: {(hi.mfe >= x).mean():.0%})')

    print('\n  Таталт — стоп хаана байх ёстой вэ (шахагдсан бүлэг):')
    for q in (.5, .7, .8, .9, .95):
        print(f'    {q:.0%} тохиолдолд {lo.mae.quantile(q):.2f} ATR-аас бага татна')

    print('\n  Урт/богино тусад нь (шахагдсан бүлэг):')
    for s, nm in ((1, 'дээш'), (-1, 'доош')):
        g = lo[lo.side == s]
        print(f'    {nm:5} n={len(g):4}  үргэлжлэл {g.mfe.median():.2f}  '
              f'таталт {g.mae.median():.2f}  хуурамч {g.rev.mean():.0%}')


if __name__ == '__main__':
    main()
