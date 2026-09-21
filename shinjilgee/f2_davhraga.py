"""f2. Sweep загвар АЛЬ ДАВХРАГА дээр хамгийн сайн ажиллах вэ.

f1 нь зөвхөн 5 минут дээр хэмжсэн. Загварын бүх параметр нь БАРААР
тодорхойлогддог (12 барын өмнөх дээд/доод, 6 барын дотор BOS, 72 барын
дотор үр дүн) тул давхрага солиход өөрөө томордог — «1 цагийн 12 бар»
нь 12 цагийн ликвидити болно.

Асуулт: тэр томрол ирмэгийг сайжруулах уу, устгах уу.

Давталтын шүүлтүүр f1-д ирмэгийг устгаж байсан тул энд ОРУУЛААГҮЙ.
Хаалт бүрд санамсаргүй оролтын суурийг тусад нь бодно — давхрага
өөрчлөгдөхөд дрифтийн нөлөө ч өөрчлөгддөг.

    python3 f2_davhraga.py
    python3 f2_davhraga.py --spread 0.5
"""
import argparse
from math import erfc, sqrt

import numpy as np
import pandas as pd

import f1_sweep as F

TFS = [('5min', '5 мин'), ('15min', '15 мин'), ('30min', '30 мин'),
       ('1h', '1 цаг'), ('2h', '2 цаг'), ('4h', '4 цаг')]
KS = [1.5, 2.0, 3.0, 4.0]


def prep(base, rule):
    """Давхрага болгож, загварт хэрэгтэй бүх баганыг бэлтгэнэ."""
    if rule == '5min':
        d = base.copy()
    else:
        d = (base.set_index('Date').resample(rule)
             .agg({'Open': 'first', 'High': 'max', 'Low': 'min',
                   'Close': 'last'}).dropna().reset_index())
    d['ATR'] = F.atr_of(d.High.to_numpy(), d.Low.to_numpy(),
                        d.Close.to_numpy())
    d['PriorHigh'] = d.High.shift(1).rolling(F.SWEEP_LOOKBACK).max()
    d['PriorLow'] = d.Low.shift(1).rolling(F.SWEEP_LOOKBACK).min()
    # momentum шүүлтүүр нь f1-д юу ч нэмээгүй тул энд хэрэглэхгүй,
    # гэхдээ detect() багана нэрээ хайдаг тул хоосон тавина.
    d['h1'] = np.nan
    d['m15'] = np.nan
    return d


def pv(t, n, q):
    if n == 0:
        return np.nan
    z = (t / n - q) / sqrt(q * (1 - q) / n)
    return erfc(abs(z) / sqrt(2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=0.25)
    a = ap.parse_args()

    base = F.load()
    print(f'{len(base):,} × 5 минутын бар   '
          f'{base.Date.iloc[0].date()} … {base.Date.iloc[-1].date()}')
    print(f'Спред ${a.spread:.2f}   давталтын шүүлтүүр АШИГЛААГҮЙ '
          f'(f1-д ирмэгийг устгасан)\n')

    rows = []
    for rule, nm in TFS:
        d = prep(base, rule)
        e = F.dedup(F.detect(d))
        if len(e) < 60:
            print(f'{nm}: эвент хэтэрхий цөөн ({len(e)})')
            continue
        split = int(len(d) * F.TRAIN_RATIO)
        e = e.copy()
        e['ds'] = np.where(e.anchor_i + F.HORIZON < split, 'TRAIN',
                           np.where(e.anchor_i >= split, 'UNSEEN', 'B'))
        yrs = (d.Date.iloc[-1] - d.Date.iloc[0]).days / 365.25
        print(f'{"=" * 72}')
        print(f'{nm}   {len(d):,} бар   {len(e):,} эвент   '
              f'жилд {len(e) / yrs:.0f}   дээш {(e.dir == 1).mean():.0%}')
        print(f'{"=" * 72}')
        print(f'  {"хаалт":>7}{"багц":>8}{"n":>7}{"зорилт%":>10}'
              f'{"суурь":>8}{"зөрүү":>8}{"зардал":>9}{"цэвэр R":>10}{"p":>9}')
        for k in KS:
            o, st = F.outcomes(d, e, k)
            bk = F.baseline(d, k, n_draw=8000)
            x = e.copy()
            x['out'] = o
            x['step'] = st
            for ds in ('TRAIN', 'UNSEEN'):
                g = x[x.ds == ds]
                t = (g.out == 'TARGET').sum()
                s = (g.out == 'STOP').sum()
                if t + s < 30:
                    continue
                p = t / (t + s) * 100
                w = (g.dir == 1).mean()
                q = (bk[1] * w + bk[-1] * (1 - w)) / 100
                res = g[g.out.isin(('TARGET', 'STOP'))]
                cost = float(np.nanmean(a.spread / res.step))
                net = (p / 100) - (1 - p / 100) - cost
                print(f'  {k:6.1f}{ds[:6]:>8}{t + s:7}{p:9.1f}%'
                      f'{q * 100:7.1f}%{p - q * 100:+8.1f}{cost:9.3f}'
                      f'{net:+10.3f}{pv(t, t + s, q):9.4f}')
                rows.append({'tf': nm, 'k': k, 'ds': ds, 'n': t + s,
                             'pct': p, 'base': q * 100, 'net': net,
                             'per_yr': len(e) / yrs,
                             'p': pv(t, t + s, q)})
        print()

    r = pd.DataFrame(rows)
    un = r[r.ds == 'UNSEEN'].copy()
    print(f'{"=" * 72}\nUNSEEN дээрх ЦЭВЭР R — аль давхрага, аль хаалт\n'
          f'{"=" * 72}')
    piv = un.pivot_table(index='tf', columns='k', values='net')
    piv = piv.reindex([n for _, n in TFS if n in piv.index])
    print(piv.round(3).to_string())

    print(f'\n{"=" * 72}\nЖИЛИЙН ӨГӨӨЖ (цэвэр R × эвент/жил)\n{"=" * 72}')
    un['yr_R'] = un.net * un.per_yr
    piv2 = un.pivot_table(index='tf', columns='k', values='yr_R')
    piv2 = piv2.reindex([n for _, n in TFS if n in piv2.index])
    print(piv2.round(1).to_string())

    best = un.sort_values('yr_R', ascending=False).head(5)
    print('\nШилдэг 5 (UNSEEN, жилийн R-ээр):')
    for _, b in best.iterrows():
        print(f'  {b.tf:8} хаалт {b.k} ATR   n={int(b.n):4}  '
              f'{b.pct:.1f}% vs суурь {b.base:.1f}%   '
              f'цэвэр {b.net:+.3f}R × {b.per_yr:.0f}/жил = '
              f'{b.yr_R:+.1f}R   p={b.p:.4f}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
