"""d7. ФИБОНАЧЧИ шахалтын зурвас дээр — аль түвшин хүчтэй вэ?

Шахалт үүсэх үед дээд ба доод хилийг 0 ба 1 болгож Фибоначчи татвал
аль түвшин ажилладаг вэ. Хоёр аргаар шалгана:

  1. БӨӨГНӨРӨЛ. Задралын дараа үнэ хаана ЗОГСДОГ вэ (хамгийн хол
     явсан цэг), түүнийг зурвасын өргөний дахинаар хэмжинэ. Хэрэв
     Фибоначчи ажилладаг бол 1.272, 1.618, 2.618 зэрэг тоон дээр
     бөөгнөрөл харагдах ёстой.

     ЗАНГА: аливаа тархалт ямар нэг цэг дээр «бөөгнөрсөн» мэт
     харагддаг. Тиймээс Фибоначчийн тоонуудыг ХӨРШ тоонуудтай
     (1.1, 1.4, 1.5, 1.8 …) зэрэгцүүлж харна. Зөвхөн Фибоначчийнх
     нь ялгарвал л жинхэнэ.

  2. ПРАКТИК. Зорилтоо Фибоначчийн түвшинд тавих нь ATR-аар
     тавихаас дээр үү. Энэ нь R-ээр шууд хэмжигдэнэ.

Фибоначчийн түвшин нь зурвасын өргөнөөс (up − dn) хэмжигдэнэ:
задарсан хилээс цааш 0.618, 1.0, 1.272, 1.618, 2.0, 2.618 дахин.

    python3 d7_fibo.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

FIB = [.382, .618, 1.0, 1.272, 1.618, 2.0, 2.618]


def build():
    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr'] = tr.rolling(14).mean()
    d['sq'] = d.atr / tr.rolling(100).mean()
    m = d.close.rolling(20).mean()
    d['up'], d['dn'] = m + 1.5 * d.atr, m - 1.5 * d.atr
    return d.dropna(subset=['sq', 'up', 'atr'])


def breaks(d, hold=15):
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = d.atr.to_numpy(), d.up.to_numpy(), d.dn.to_numpy()
    sq = d.sq.to_numpy()
    q20 = np.nanquantile(sq, .2)
    n = len(d)
    out = []
    for i in np.where(sq <= q20)[0]:
        if not np.isfinite(A[i]) or A[i] <= 0 or U[i] <= DN[i]:
            continue
        w = U[i] - DN[i]                      # зурвасын өргөн
        pos = (C[i] - DN[i]) / w
        lvl = side = ej = None
        for j in range(i + 1, min(i + 6, n)):
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
        k2 = min(ej + hold, n)
        top, bot = H[ej:k2].max(), L[ej:k2].min()
        ext = ((top - lvl) if side > 0 else (lvl - bot)) / w
        out.append(dict(i=i, ej=ej, side=side, lvl=lvl, w=w, atr=A[i],
                        pos=pos, ext=ext, date=d.index[ej]))
    return pd.DataFrame(out)


def target_test(d, t, mult, mode, spread=.25, hold=15):
    """Зорилтыг зурвасын өргөний `mult` дахин (fib) эсвэл ATR-ийн
    `mult` дахин (atr) тавьж R хэмжинэ. Стоп үргэлж 2 ATR."""
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    n = len(d)
    rs = []
    for _, r in t.iterrows():
        side, lvl = int(r.side), r.lvl
        risk = 2.0 * r.atr
        targ = lvl + side * (mult * r.w if mode == 'fib' else mult * r.atr)
        stop = lvl - side * risk
        ej = int(r.ej)
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
        rs.append(side * (out - lvl) / risk - spread / risk)
    return pd.Series(rs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    d = build()
    t = breaks(d)
    up = t[t.side == 1]
    hi = up[up.pos >= up.pos.quantile(.5)]
    print(f'{len(t)} задрал, {len(up)} дээш, {len(hi)} дээд байрлалтай\n')

    # ── 1. БӨӨГНӨРӨЛ — НУТГИЙН ОРГИЛЫН шалгалт ────────────────────
    # Эхний хувилбарт Фибоначчийг «хөрш» тоонуудтай (0.3, 0.5, 0.8 …)
    # харьцуулсан нь ШУДАРГА БИШ байв: хөршүүд нь Фибоначчиас ДООГУУР
    # байсан тул мэдээж илүү олон удаа хүрэгдэнэ. Зөв шалгалт нь —
    # түвшин ӨӨРИЙН ХОЁР ТАЛААСАА илүү бөөгнөрөлтэй юу (нутгийн оргил).
    e = up.ext.dropna()
    print(f'  1) Зогссон цэг Фибоначчи дээр БӨӨГНӨРДӨГ үү (n={len(e)})')
    print(f'     {"түвшин":>8}{"±0.05":>9}{"зүүн":>8}{"баруун":>9}{"оргил":>8}')
    npk = 0
    for f in FIB:
        c = ((e >= f - .05) & (e < f + .05)).sum()
        lf = ((e >= f - .15) & (e < f - .05)).sum()
        rg = ((e >= f + .05) & (e < f + .15)).sum()
        pk = c > lf and c > rg
        npk += pk
        print(f'     {f:8.3f}{c:9}{lf:8}{rg:9}{"ТИЙМ" if pk else "—":>8}')
    rng = np.random.default_rng(0)
    base = 0
    for _ in range(200):
        f = rng.uniform(.3, 2.7)
        c = ((e >= f - .05) & (e < f + .05)).sum()
        lf = ((e >= f - .15) & (e < f - .05)).sum()
        rg = ((e >= f + .05) & (e < f + .15)).sum()
        base += (c > lf and c > rg)
    print(f'\n     Фибоначчийн оргил: {npk}/7 ({npk / 7:.0%})')
    print(f'     САНАМСАРГҮЙ түвшний оргил: {base}/200 ({base / 200:.0%})'
          f'   ← суурь')

    # ── 2. ПРАКТИК ─────────────────────────────────────────────────
    print('\n  2) Зорилтыг ФИБОНАЧЧИАР vs ATR-аар тавих (дээд байрлал, дээш)')
    print(f'     {"арга":22}{"зорилт":>10}{"R":>10}{"хүрсэн%":>10}')
    best = []
    for f in FIB:
        r = target_test(d, hi, f, 'fib', a.spread)
        best.append((r.mean(), f'фибо {f}', f, 'fib'))
        print(f'     {"фибо " + str(f):22}{f:10.3f}{r.mean():+10.3f}'
              f'{(hi.ext >= f).mean():10.0%}')
    print()
    for m in (2.0, 3.0, 4.0, 5.0, 6.0):
        r = target_test(d, hi, m, 'atr', a.spread)
        best.append((r.mean(), f'{m} ATR', m, 'atr'))
        print(f'     {str(m) + " ATR":22}{m:10.3f}{r.mean():+10.3f}')

    print(f'\n  ЗУРВАСЫН ӨРГӨН = {(hi.w / hi.atr).median():.3f} ATR '
          f'— ТОДОРХОЙЛОЛТООР яг 3 ATR')
    print('  ((дундаж + 1.5 ATR) − (дундаж − 1.5 ATR) = 3 ATR)')
    print('  Тиймээс «фибо f» ба «3f ATR» нь ИЖИЛ зорилт — Фибоначчи нь')
    print('  энэ зурвас дээр ATR-ийн зорилтыг өөр нэрээр дуудсан хэрэг.')


if __name__ == '__main__':
    main()
