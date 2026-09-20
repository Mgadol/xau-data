"""b8. Шахалтын ЭРЭМБЭ — хэр шахагдвал хэдэн хувьд нь задардаг вэ?

b6, b7 шахалт ажилладгийг харуулав. Энд түүнийг ХЭРЭГЛЭХЭД бэлэн
хүснэгт болгоно: шахалтын гүн бүрд —

    · хэдэн хувьд нь 5/10 хоногийн дотор муж эвдэрдэг
    · эвдэрсэн бол хэр хол явдаг (ATR-ийн дахинаар)
    · 2 ATR, 3 ATR хүрэх нь хэдэн хувь
    · эвдрэх хүртэл дунджаар хэдэн хоног

«Задарсан» гэдгийн тодорхойлолт: сүүлийн 10 хоногийн дээд эсвэл доод
цэгийг давах. Чиглэл нь хамаагүй — b3 чиглэл таамаглагдахгүйг
харуулсан тул зөвхөн ХЭДЭН ХУВЬД, ХЭР ХОЛ гэдгийг хэмжинэ.

ГОЛ АНХААРУУЛГА: «90% нь задардаг» гэсэн тоо дангаараа утгагүй.
Ямар ч өдрөөс 10 хоног хүлээвэл үнэ хаа нэгтээ явна — 10 хоногийн
муж эвдрэх нь бараг л баталгаатай. Тиймээс шахагдсан бүлгийг
ТЭЛСЭН бүлэгтэй ЗЭРЭГЦҮҮЛЖ харах ёстой. Зөрүү нь л мэдээлэл.

    python3 b8_erembe.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

RNG = 10          # хэдэн хоногийн мужийг эвдэх вэ
WAIT = (5, 10)    # хэдэн хоног хүлээх вэ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bins', type=int, default=10)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d['up'] = d.high.rolling(RNG).max()
    d['dn'] = d.low.rolling(RNG).min()
    d = d.dropna(subset=['sq', 'up', 'atr14'])

    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    U, D, A = d.up.to_numpy(), d.dn.to_numpy(), d.atr14.to_numpy()
    n = len(d)

    rec = {w: {'brk': [], 'days': [], 'mfe': []} for w in WAIT}
    for i in range(n):
        for w in WAIT:
            broke, day = 0, np.nan
            for j in range(i + 1, min(i + 1 + w, n)):
                if H[j] >= U[i] or L[j] <= D[i]:
                    broke, day = 1, j - i
                    break
            rec[w]['brk'].append(broke)
            rec[w]['days'].append(day)
            # Эвдэрсэн эсэхээс үл хамааран хэр хол явсан
            k = min(i + 1 + w, n)
            if k > i + 1:
                mx = (H[i + 1:k].max() - C[i]) / C[i]
                mn = (C[i] - L[i + 1:k].min()) / C[i]
                rec[w]['mfe'].append(max(mx, mn) * 100 / (A[i] / C[i] * 100))
            else:
                rec[w]['mfe'].append(np.nan)

    for w in WAIT:
        for key in ('brk', 'days', 'mfe'):
            d[f'{key}{w}'] = rec[w][key]

    d['bin'] = pd.qcut(d.sq, a.bins, labels=False)
    print(f'{len(d):,} өдөр   2005 → 2026   мужийн урт {RNG} хоног\n')
    print(f'{"бүлэг":>6} {"ATR14/ATR100":>13} {"5 хоногт":>9} {"10 хоногт":>10} '
          f'{"эвдрэх":>8} | {"10 хоногт явсан":>16} {"2 ATR+":>8} {"3 ATR+":>8}')
    print(f'{"":>6} {"":>13} {"эвдэрсэн":>9} {"эвдэрсэн":>10} '
          f'{"хоног":>8} | {"ATR-ийн дахин":>16} {"":>8} {"":>8}')
    print('─' * 92)
    for b in range(a.bins):
        g = d[d.bin == b]
        print(f'{b + 1:>6} {g.sq.mean():13.2f} {g.brk5.mean():8.0%} '
              f'{g.brk10.mean():9.0%} {np.nanmean(g.days10):8.1f} | '
              f'{g.mfe10.mean():16.2f} {(g.mfe10 > 2).mean():8.0%} '
              f'{(g.mfe10 > 3).mean():8.0%}')

    lo, hi = d[d.bin == 0], d[d.bin == a.bins - 1]
    print(f'\n  Хамгийн шахагдсан 10% vs хамгийн тэлсэн 10%:')
    print(f'    10 хоногт эвдэрсэн : {lo.brk10.mean():.0%} vs {hi.brk10.mean():.0%}'
          f'   ← ялгаа БАГА, энэ нь мэдээлэл БИШ')
    print(f'    ATR-ийн дахинаар   : {lo.mfe10.mean():.2f} vs {hi.mfe10.mean():.2f}'
          f'   ← ЭНЭ нь мэдээлэл')
    print(f'    3 ATR-ээс давсан   : {(lo.mfe10 > 3).mean():.0%} vs '
          f'{(hi.mfe10 > 3).mean():.0%}')

    print('\n  Жилээр тогтвортой юу (хамгийн шахагдсан 10%-ийн 3 ATR+ хувь):')
    out = []
    for y in sorted(d.index.year.unique()):
        g = d[(d.index.year == y) & (d.bin == 0)]
        if len(g) >= 10:
            out.append(f'{y}:{(g.mfe10 > 3).mean():.0%}')
    print('    ' + '  '.join(out))


if __name__ == '__main__':
    main()
