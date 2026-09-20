"""d3. Шахалт хилийн АЛЬ ТАЛД тогтсон бэ + 4 цаг дээрх дээш/доош.

Хоёр асуулт:

  1. Шахалт ДООД хилд ойр тогтвол доош задрах нь илүү ЧАНАРТАЙ юу.

     d2-д «хилд ойр байдал» нь АЛЬ ТАЛ задрахыг бараг бүрэн
     тайлбарласан (дээд хилд ойр → 100% дээш). Тэр нь тавтологи.
     Харин ЧАНАР нь өөр асуулт: доод хилд наалдсанаас гарсан доош
     задрал нь бусад доош задралаас дээр үү?

     Энэ нь чухал, учир нь доош задрал одоогоор бүхэлдээ ашиггүй
     (b7, c9, d1). Хэрэв ЗАРИМ доош задрал ажилладаг бол тэр нь
     төслийн хамгийн том нүхийг нөхнө.

  2. 4 ЦАГ дээр дээш/доош тусад нь. c4-д 4 цагийн НИЙТ дүн тэгд ойр
     (+0.018 спредгүй) гарсан. Гэхдээ дээш нь ажиллаад доош нь
     дордуулж байж нийлбэр нь тэг болсон байж магадгүй.

4 цагт цагийн хэмнэлийг ЗААВАЛ цэвэрлэнэ (c3) — эс бөгөөс «шахалт»
нь зүгээр л «Ази байна» гэдгийг олно.

    python3 d3_bairlal.py
"""
import argparse
import numpy as np
import pandas as pd
from core import load
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def prep_daily():
    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr'] = tr.rolling(14).mean()
    d['sq'] = d.atr / tr.rolling(100).mean()
    m = d.close.rolling(20).mean()
    d['up'], d['dn'] = m + 1.5 * d.atr, m - 1.5 * d.atr
    return d.dropna(subset=['sq', 'up', 'atr'])


def prep_tf(tf, slow=60):
    h = load('XAU_5m_data.csv')
    d = h.resample(tf).agg(open=('open', 'first'), high=('high', 'max'),
                           low=('low', 'min'), close=('close', 'last'),
                           volume=('volume', 'sum')).dropna()
    d = d[d.index >= '2010-01-01']
    pc = d.close.shift(1)
    tr = pd.concat([d.high - d.low, (d.high - pc).abs(),
                    (d.low - pc).abs()], axis=1).max(axis=1)
    d['tr'], d['atr'] = tr, tr.rolling(14).mean()
    # Цагийн хэмнэлийг цэвэрлэнэ — зөвхөн ӨНГӨРСӨН өгөгдлөөр
    key = d.index.hour * 60 + d.index.minute
    base = pd.Series(np.nan, index=d.index)
    for k, g in d.groupby(key):
        base.loc[g.index] = (g.tr / g.tr.rolling(60, min_periods=20)
                             .mean().shift(1)).to_numpy()
    d['sq'] = base.rolling(14).mean() / base.rolling(slow).mean()
    m = d.close.rolling(20).mean()
    d['up'], d['dn'] = m + 1.5 * d.atr, m - 1.5 * d.atr
    return d.dropna(subset=['sq', 'up', 'atr'])


def collect(d, spread, wait=5, hold=10):
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = d.atr.to_numpy(), d.up.to_numpy(), d.dn.to_numpy()
    sq = d.sq.to_numpy()
    n = len(d)
    q20 = np.nanquantile(sq, .2)
    rows = []
    for i in np.where(sq <= q20)[0]:
        if not np.isfinite(A[i]) or A[i] <= 0 or U[i] <= DN[i]:
            continue
        # Байрлал: 0 = доод хилд наалдсан, 1 = дээд хилд
        pos = (C[i] - DN[i]) / (U[i] - DN[i])
        lvl = side = ej = None
        for j in range(i + 1, min(i + 1 + wait, n)):
            hu, hd = H[j] >= U[i], L[j] <= DN[i]
            if hu and hd:
                break
            if hu:
                lvl, side, ej = U[i], 1, j
                break
            if hd:
                lvl, side, ej = DN[i], -1, j
                break
        if lvl is None:
            continue
        risk = 2.0 * A[i]
        stop, targ = lvl - side * risk, lvl + side * 4.0 * A[i]
        out = None
        k2 = min(ej + hold, n)
        for j in range(ej, k2):
            s_ = (L[j] <= stop) if side > 0 else (H[j] >= stop)
            t_ = (H[j] >= targ) if side > 0 else (L[j] <= targ)
            if s_:
                out = stop
                break
            if t_:
                out = targ
                break
        if out is None:
            out = C[k2 - 1]
        rows.append((d.index[ej], pos, side,
                     side * (out - lvl) / risk - spread / risk))
    return pd.DataFrame(rows, columns=['date', 'pos', 'side', 'R'])


def by_pos(t, label):
    print(f'\n  {label}')
    t = t.copy()
    t['pb'] = pd.qcut(t.pos, 3, labels=False, duplicates='drop')
    nm = ['доод хилд ойр', 'дунд', 'дээд хилд ойр']
    print(f'    {"байрлал":16}{"ДЭЭШ задрал":>20}{"ДООШ задрал":>20}')
    for b in sorted(t.pb.dropna().unique()):
        g = t[t.pb == b]
        cells = []
        for sd in (1, -1):
            x = g[g.side == sd]
            cells.append(f'{x.R.mean():+.3f} (n={len(x)})' if len(x) >= 12
                         else '—')
        print(f'    {nm[int(b)]:16}' + ''.join(c.rjust(20) for c in cells))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    print('=' * 62)
    print('ӨДРИЙН график')
    print('=' * 62)
    td = collect(prep_daily(), a.spread)
    print(f'  {len(td)} задрал')
    for sd, nm in ((1, 'дээш'), (-1, 'доош')):
        g = td[td.side == sd]
        print(f'    {nm:6} n={len(g):4}  {g.R.mean():+.3f}R  '
              f'ялсан {(g.R > 0).mean():.0%}')
    by_pos(td, 'Байрлалаар:')

    for tf in ('4h', '8h'):
        print('\n' + '=' * 62)
        print(f'{tf.upper()} график  (цагийн хэмнэл цэвэрлэгдсэн)')
        print('=' * 62)
        t = collect(prep_tf(tf), a.spread, wait=8, hold=16)
        print(f'  {len(t)} задрал')
        for sd, nm in ((1, 'дээш'), (-1, 'доош')):
            g = t[t.side == sd]
            print(f'    {nm:6} n={len(g):5}  {g.R.mean():+.3f}R  '
                  f'ялсан {(g.R > 0).mean():.0%}')
        by_pos(t, 'Байрлалаар:')

    print('\n\n  Доод хилд ойр тогтсон шахалтын ДООШ задрал нь бусад доош')
    print('  задралаас мэдэгдэхүйц дээр бол — доош талын нүх нөхөгдөнө.')


if __name__ == '__main__':
    main()
