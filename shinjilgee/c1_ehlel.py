"""c1. Шахалт ХЭЗЭЭ эхэлсэн бэ — өдөр тоолох цэг.

b6-b9 бүгд «өнөөдөр хэр шахагдсан бэ» гэсэн ТҮВШИН дээр ажилласан.
Арилжаанд илүү ойр нь «шахалт хэдэн дэх өдрөө явж байна» гэсэн
ТООЛОЛТ — тэгвэл хүснэгт хараад хүлээх эсэхээ шийднэ.

Эхлэл: ATR14/ATR100 харьцаа босгыг ДЭЭРЭЭС ДООШ огтлох өдөр.
Тэр өдрөөс эхлэн 1, 2, 3 … гэж тоолно. Шахалт дуусах нь хоёр
замаар:

    задралаар — 10 хоногийн муж эвдэрсэн
    сулралаар — харьцаа босгоос дээш буцаж гарсан (задралгүй)

Шалгах гол итгэл үнэмшил: «удаан шахагдсан нь хүчтэй тэсэрдэг».
Энэ нь тун түгээмэл боловч шалгагдаагүй байдаг. Хэрэв үнэн бол
шахалтын 8 дахь өдөр 2 дахь өдрөөсөө илүү боломж гэсэн үг —
хүлээх нь утгатай болно. Худал бол хүлээх нь зүгээр л цаг алдах.

ХАЗАЙЛТААС сэргийлсэн зүйл: урт шахалтыг сонгож авах нь өөрөө
ирээдүйг харсан хэрэг болж болзошгүй («8 хоног үргэлжилсэн» гэдгийг
8 дахь өдөр л мэднэ). Тиймээс хэмжилт бүрийг ТУХАЙН ӨДӨР мэдэгдэж
байсан мэдээллээр л хийнэ: n дэх өдөр байгаа гэдгийг тэр өдөр мэднэ,
цаашид хэд үргэлжлэхийг мэдэхгүй.

    python3 c1_ehlel.py [--thresh 0.85]
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

RNG = 10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--thresh', type=float, default=.85)
    ap.add_argument('--hold', type=int, default=10)
    a = ap.parse_args()
    T = a.thresh

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d['up'] = d.high.rolling(RNG).max()
    d['dn'] = d.low.rolling(RNG).min()
    d = d.dropna(subset=['sq', 'up', 'atr14'])

    sq = d.sq.to_numpy()
    H, L = d.high.to_numpy(), d.low.to_numpy()
    U, D, A = d.up.to_numpy(), d.dn.to_numpy(), d.atr14.to_numpy()
    n = len(d)

    # ── Шахалтын үеүүдийг ялгана ─────────────────────────────────────
    inside = sq < T
    start = inside & ~np.r_[False, inside[:-1]]      # дээрээс доош огтолсон
    day_no = np.zeros(n, int)
    c = 0
    for i in range(n):
        c = c + 1 if inside[i] else 0
        day_no[i] = c
    d['day_no'] = day_no

    n_ep = int(start.sum())
    lens = []
    i = 0
    while i < n:
        if start[i]:
            j = i
            while j < n and inside[j]:
                j += 1
            lens.append(j - i)
            i = j
        else:
            i += 1
    lens = np.array(lens)
    print(f'Босго {T}   —   {n_ep} шахалтын үе, 2005–2026')
    print(f'Үргэлжлэх хугацаа: медиан {np.median(lens):.0f} хоног, '
          f'дундаж {lens.mean():.1f}, хамгийн урт {lens.max()}')
    print('  хуваарь: ' + '  '.join(
        f'{q:.0%}:{np.quantile(lens, q):.0f}х' for q in (.25, .5, .75, .9)))
    print(f'  нэг жилд дунджаар {n_ep / 21:.1f} удаа\n')

    # ── Шахалтын n дэх өдөр орвол юу болох вэ ────────────────────────
    rows = []
    for i in range(n):
        if day_no[i] == 0:
            continue
        lvl = side = ej = None
        for j in range(i + 1, min(i + 6, n)):
            hu, hd = H[j] >= U[i], L[j] <= D[i]
            if hu and hd:
                break
            if hu:
                lvl, side, ej = U[i], 1, j
                break
            if hd:
                lvl, side, ej = D[i], -1, j
                break
        if lvl is None:
            rows.append((day_no[i], sq[i], 0, np.nan, np.nan))
            continue
        k = min(ej + a.hold, n)
        hh, ll = H[ej:k].max(), L[ej:k].min()
        mfe = (hh - lvl) / A[i] if side > 0 else (lvl - ll) / A[i]
        mae = ((lvl - ll) if side > 0 else (hh - lvl)) / A[i]
        rows.append((day_no[i], sq[i], 1, mfe, max(mae, 0)))

    t = pd.DataFrame(rows, columns=['day', 'sq', 'brk', 'mfe', 'mae'])
    t['grp'] = pd.cut(t.day, [0, 1, 2, 3, 5, 8, 13, 1000],
                      labels=['1', '2', '3', '4-5', '6-8', '9-13', '14+'])

    print(f'{"шахалтын":>9} {"харьцаа":>8} {"задарсан":>9} '
          f'{"үргэлжлэл":>10} {"таталт":>8} {"харьцаа":>8} {"n":>6}')
    print(f'{"өдөр":>9} {"дундаж":>8} {"5 хоногт":>9} '
          f'{"медиан":>10} {"медиан":>8} {"MFE/MAE":>8}')
    print('─' * 70)
    for g, x in t.groupby('grp', observed=True):
        b = x[x.brk == 1]
        if len(b) < 20:
            continue
        r = b.mfe.median() / max(b.mae.median(), .01)
        print(f'{str(g):>9} {x.sq.mean():8.2f} {x.brk.mean():9.0%} '
              f'{b.mfe.median():10.2f} {b.mae.median():8.2f} {r:8.2f} {len(x):6}')

    print('\n  «Удаан шахагдсан нь илүү хол явдаг» — үнэн үү:')
    e = t[(t.day <= 2) & (t.brk == 1)]
    l = t[(t.day >= 6) & (t.brk == 1)]
    print(f'    1-2 дахь өдөр : үргэлжлэл {e.mfe.median():.2f}  '
          f'таталт {e.mae.median():.2f}  (n={len(e)})')
    print(f'    6+ дахь өдөр  : үргэлжлэл {l.mfe.median():.2f}  '
          f'таталт {l.mae.median():.2f}  (n={len(l)})')
    diff = l.mfe.median() - e.mfe.median()
    print(f'    зөрүү {diff:+.2f} ATR  → '
          + ('хүлээх нь УТГАТАЙ' if diff > .15 else
             'хүлээх нь утгагүй — эрт орсон ч ижил'))


if __name__ == '__main__':
    main()
