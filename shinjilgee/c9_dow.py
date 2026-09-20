"""c9. ШАХАЛТ + DOW-гийн бүтэц — чиглэлийн нүхийг нөхөж чадах уу?

b3-д чиглэл таамаглагдахгүй, b7-д богино тал ажиллахгүй нь гарсан.
Энэ бол шахалтын хамгийн том хязгаар: ХЭЗЭЭ гэдгийг хэлдэг, АЛЬ ТИЙШ
гэдгийг хэлдэггүй.

Dow-гийн бүтэц чиглэлийн контекст өгдөг:

    HH + HL  (өсөх оргил, өсөх ёроол)  = өсөх хандлага
    LL + LH  (буурах ёроол, буурах оргил) = буурах хандлага
    бусад                              = муж / тодорхойгүй

Хоёр зүйлийг шалгана:

  1. ХАНДЛАГА ДАГАСАН задрал эсрэгээсээ дээр үү? Өөрөөр хэлбэл
     өсөх бүтцэд ДЭЭШ задарсан нь доош задарснаас дээр үү.

  2. ХЭДДЭХ шахалт вэ. Нэг хандлагын дотор 1, 2, 3 дахь шахалт
     өөр өөр үр дүнтэй юу. («Сүүлийн шахалт нь ядрах дохио» гэсэн
     нийтлэг ойлголт.)

ЗАНГА — БУЦААД ХАРАХ. Эргэлтийн цэгийг zigzag олдог ч сүүлийн цэг нь
ХОЖИМ баталгаажна: оргил болсныг мэдэхийн тулд үнэ pct-ээр буух
хэрэгтэй. Тиймээс `confirm_index`-ээр баталгаажсан ӨДРИЙГ авч,
зөвхөн тэр өдрөөс ХОЙШ тэр бүтцийг мэдэж байсан гэж үзнэ. Үгүй бол
ирээдүйг харсан болно — энэ ажилд хамгийн олон удаа гарсан алдаа.

    python3 c9_dow.py [--pct 0.03]
"""
import argparse
import numpy as np
import pandas as pd
from core import zigzag, confirm_index
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def structure(d, pct):
    """Өдөр бүрд тухайн үед МЭДЭГДЭЖ байсан бүтэц: +1 өсөх, -1 буурах, 0 муж."""
    piv = zigzag(d, pct)
    n = len(d)
    st = np.zeros(n, int)
    seq = []                     # (баталгаажсан өдөр, үнэ, чиглэл)
    for pi, pv, pd_ in piv:
        ci = confirm_index(d, pi, pv, pd_, pct)
        if ci is not None and ci < n:
            seq.append((ci, pv, pd_))
    seq.sort()
    highs, lows = [], []
    k = 0
    cur = 0
    for i in range(n):
        while k < len(seq) and seq[k][0] <= i:
            _, pv, pdir = seq[k]
            (highs if pdir == 1 else lows).append(pv)
            k += 1
            if len(highs) >= 2 and len(lows) >= 2:
                hh = highs[-1] > highs[-2]
                hl = lows[-1] > lows[-2]
                ll = lows[-1] < lows[-2]
                lh = highs[-1] < highs[-2]
                cur = 1 if (hh and hl) else (-1 if (ll and lh) else 0)
        st[i] = cur
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pct', type=float, default=.03)
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    m20 = d.close.rolling(20).mean()
    d['up'] = m20 + 1.5 * d.atr14
    d['dn'] = m20 - 1.5 * d.atr14
    d = d.dropna(subset=['sq', 'up', 'atr14'])
    d['st'] = structure(d, a.pct)
    q20 = d.sq.quantile(.2)

    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = d.atr14.to_numpy(), d.up.to_numpy(), d.dn.to_numpy()
    ST = d.st.to_numpy()
    n = len(d)

    # Шахалтын дугаар — НЭГ бүтцийн дотор хэддэх нь вэ
    sqz = (d.sq <= q20).to_numpy()
    num = np.zeros(n, int)
    cnt, last_st, inside = 0, None, False
    for i in range(n):
        if ST[i] != last_st:
            cnt, last_st = 0, ST[i]
        if sqz[i] and not inside:
            cnt += 1
        inside = sqz[i]
        num[i] = cnt

    rows = []
    for i in np.where(sqz)[0]:
        if not np.isfinite(A[i]) or A[i] <= 0:
            continue
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
        risk = 2.0 * A[i]
        stop, targ = lvl - side * risk, lvl + side * 4.0 * A[i]
        out = None
        k2 = min(ej + 10, n)
        for j in range(ej, k2):
            sh = (L[j] <= stop) if side > 0 else (H[j] >= stop)
            th = (H[j] >= targ) if side > 0 else (L[j] <= targ)
            if sh:
                out = stop
                break
            if th:
                out = targ
                break
        if out is None:
            out = C[k2 - 1]
        r = side * (out - lvl) / risk - a.spread / risk
        rows.append((ST[i], side, num[i], r))

    t = pd.DataFrame(rows, columns=['st', 'side', 'num', 'R'])
    lbl = {1: 'өсөх (HH+HL)', -1: 'буурах (LL+LH)', 0: 'муж'}
    print(f'zigzag {a.pct:.0%}   {len(t)} задрал   бүтэц нь БАТАЛГААЖСАН '
          f'өдрөөс хойш мэдэгдэнэ\n')

    print(f'{"бүтэц":16} {"задрал":>10} {"n":>6} {"R":>9} {"ялсан":>7}')
    print('─' * 54)
    for s in (1, 0, -1):
        for sd, snm in ((1, 'дээш'), (-1, 'доош')):
            g = t[(t.st == s) & (t.side == sd)]
            if len(g) < 20:
                continue
            tag = '  ← дагасан' if s == sd else (
                '  ← эсрэг' if s == -sd and s != 0 else '')
            print(f'{lbl[s]:16} {snm:>10} {len(g):6} {g.R.mean():+9.3f} '
                  f'{(g.R > 0).mean():7.0%}{tag}')
        print()

    wi = t[(t.st != 0) & (t.st == t.side)]
    ag = t[(t.st != 0) & (t.st == -t.side)]
    rg = t[t.st == 0]
    print(f'  ХАНДЛАГА ДАГАСАН  n={len(wi):4}  {wi.R.mean():+.3f}R  '
          f'ялсан {(wi.R > 0).mean():.0%}')
    print(f'  ЭСРЭГ             n={len(ag):4}  {ag.R.mean():+.3f}R  '
          f'ялсан {(ag.R > 0).mean():.0%}')
    print(f'  МУЖ               n={len(rg):4}  {rg.R.mean():+.3f}R  '
          f'ялсан {(rg.R > 0).mean():.0%}')
    print(f'  → зөрүү (дагасан − эсрэг) {wi.R.mean() - ag.R.mean():+.3f}R')

    print('\n  ХЭДДЭХ шахалт вэ (нэг бүтцийн дотор):')
    for k in (1, 2, 3):
        g = t[t.num == k]
        if len(g) >= 30:
            print(f'    {k}-р  n={len(g):4}  {g.R.mean():+.3f}R  '
                  f'ялсан {(g.R > 0).mean():.0%}')
    g = t[t.num >= 4]
    if len(g) >= 30:
        print(f'    4+   n={len(g):4}  {g.R.mean():+.3f}R  '
              f'ялсан {(g.R > 0).mean():.0%}')


if __name__ == '__main__':
    main()
