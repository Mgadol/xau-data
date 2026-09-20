"""b7. Шахалтын дараах ЭВДРЭЛ — жинхэнэ арилжаа болгож шалгана.

b6 «шахалтын дараа ATR-ийн дахинаар илүү хол явдаг» гэж олов. Гэхдээ
MFE бол онолын дээд хязгаар — барьж авах боломжгүй. Энд орох дүрэм,
стоп, зорилт, зардалтай жинхэнэ арилжаа болгоно.

Дүрэм:

  Дохио   — ATR14/ATR100 доод 20% (шахагдсан)
  Орох    — сүүлийн N хоногийн дээд/доод эвдэрвэл тэр ЧИГЛЭЛД, яг
            эвдэрсэн түвшинд (stop order)
  Стоп    — орсон цэгээс k × ATR14
  Зорилт  — m × ATR14  (буюу m/k R)
  Хугацаа — H хоногийн дараа хаалтаар гарна

ХАМГИЙН ЧУХАЛ ХЭСЭГ — ХЯНАЛТЫН БҮЛЭГ. Ижил дүрмийг ШАХААГҮЙ өдрүүдэд
бас ажиллуулна. Учир нь эвдрэлийн дүрэм өөрөө ашигтай байж магадгүй,
эсвэл хоёулаа алдагдалтай байж магадгүй. Шахалтын үнэ цэнэ нь зөвхөн
ХОЁРЫН ЗӨРҮҮ.

Хоёр шударга бус байдлаас зайлсхийв:

  1. Нэг барт стоп ба зорилт ХОЁУЛАА хүрвэл СТОП хүрсэн гэж тооцно.
     Өдрийн өгөгдлөөс аль нь эхэлснийг мэдэх боломжгүй тул хамгийн
     МУУ таамаглалыг авна. Эсрэгээр тооцвол үр дүн хуурамчаар сайхан
     харагдана.
  2. Нэг өдөр дээш, доош ХОЁУЛАА эвдэрвэл тэр арилжааг АЛГАСНА —
     аль нь эхэлснийг мэдэхгүй тул сонгох нь өөрөө хууран мэхлэлт.

    python3 b7_evdrel.py [--stop 1.0 --target 2.0 --range 10]
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def simulate(d, mask, rng_len, k, m, wait, hold, cost_pct):
    """mask=True өдрүүдээс эвдрэл хайж, арилжаануудыг буцаана."""
    hi_n = d.high.rolling(rng_len).max()
    lo_n = d.low.rolling(rng_len).min()
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    atr = d.atr14.to_numpy()
    up, dn = hi_n.to_numpy(), lo_n.to_numpy()
    idx = np.where(mask.to_numpy())[0]
    n = len(d)
    trades = []

    for i in idx:
        if not np.isfinite(atr[i]) or not np.isfinite(up[i]):
            continue
        risk = k * atr[i]
        if risk <= 0:
            continue
        entry = side = ent_j = None
        for j in range(i + 1, min(i + 1 + wait, n)):
            hit_u, hit_d = H[j] >= up[i], L[j] <= dn[i]
            if hit_u and hit_d:
                break                      # аль нь эхэлснийг мэдэхгүй → алгасна
            if hit_u:
                entry, side, ent_j = up[i], 1, j
                break
            if hit_d:
                entry, side, ent_j = dn[i], -1, j
                break
        if entry is None:
            continue

        stop = entry - side * risk
        targ = entry + side * m * atr[i]
        out = None
        for j in range(ent_j, min(ent_j + hold, n)):
            s_hit = (L[j] <= stop) if side > 0 else (H[j] >= stop)
            t_hit = (H[j] >= targ) if side > 0 else (L[j] <= targ)
            if s_hit:                       # стоп ба зорилт хоёулаа бол СТОП
                out = stop
                break
            if t_hit:
                out = targ
                break
        if out is None:
            out = C[min(ent_j + hold - 1, n - 1)]

        r = side * (out - entry) / risk
        r -= cost_pct / 100 * entry / risk   # спред → R болгон хөрвүүлнэ
        trades.append((d.index[ent_j], side, r))
    return pd.DataFrame(trades, columns=['date', 'side', 'R'])


def report(name, t):
    if len(t) == 0:
        print(f'  {name:22} арилжаа алга')
        return None
    print(f'  {name:22} n={len(t):5}  дундаж {t.R.mean():+.3f}R  '
          f'нийт {t.R.sum():+8.1f}R  ялсан {(t.R > 0).mean():5.1%}')
    return t.R.mean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--range', type=int, default=10, dest='rng_len')
    ap.add_argument('--stop', type=float, default=1.0)
    ap.add_argument('--target', type=float, default=2.0)
    ap.add_argument('--wait', type=int, default=5)
    ap.add_argument('--hold', type=int, default=10)
    ap.add_argument('--cost', type=float, default=.03)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d = d.dropna(subset=['sq'])

    q20, q80 = d.sq.quantile(.2), d.sq.quantile(.8)
    print(f'{len(d):,} өдөр  {d.index.min().date()} → {d.index.max().date()}')
    print(f'Дүрэм: {a.rng_len} хоногийн муж эвдрэх, стоп {a.stop}×ATR, '
          f'зорилт {a.target}×ATR ({a.target / a.stop:.1f}R),')
    print(f'       {a.wait} хоног хүлээнэ, {a.hold} хоног барина, '
          f'зардал {a.cost}%\n')

    groups = {
        'ШАХАГДСАН (доод 20%)': d.sq <= q20,
        'хэвийн (дунд 60%)': (d.sq > q20) & (d.sq < q80),
        'тэлсэн (дээд 20%)': d.sq >= q80,
    }
    res = {}
    for nm, mask in groups.items():
        t = simulate(d, mask, a.rng_len, a.stop, a.target,
                     a.wait, a.hold, a.cost)
        res[nm] = t
        report(nm, t)

    sq, ex = res['ШАХАГДСАН (доод 20%)'], res['тэлсэн (дээд 20%)']
    if len(sq) and len(ex):
        print(f'\n  Шахагдсан − тэлсэн: {sq.R.mean() - ex.R.mean():+.3f}R '
              f'нэг арилжаанд')

    # Жилээр — нэг хоёр жилийн аз мөн эсэхийг харна
    if len(sq):
        print('\n  ШАХАГДСАН бүлгийн жилийн дундаж R:')
        g = sq.set_index('date').R.groupby(lambda x: x.year)
        line = '  '.join(f'{y}:{v:+.2f}' for y, v in g.mean().items()
                         if g.size()[y] >= 3)
        print('    ' + line)
        pos = (g.mean() > 0).sum()
        print(f'    эерэг жил: {pos}/{g.ngroups}')


if __name__ == '__main__':
    main()
