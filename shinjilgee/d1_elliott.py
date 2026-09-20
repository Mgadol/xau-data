"""d1. ELLIOTT-ийн механик араг яс + шахалт.

Elliott давалгааг БҮХЭЛД нь шалгах боломжгүй: тоолол нь субъектив,
хоёр хүн ижил графикийг өөрөөр тэмдэглэдэг. Тиймээс энд зөвхөн
МЕХАНИК, маргаангүй хэсгийг шалгана:

  1. ДАВАЛГААНЫ ДУГААР — zigzag-аар тодорхойлсон хөлийн дугаар.
     Elliott-оор 3-р давалгаа хамгийн хүчтэй, 5-р нь суларсан байдаг.
     Тэгвэл шахалтын задрал 3 дахь хөл дээр илүү сайн байх ёстой.

  2. ФИБОНАЧЧИЙН УХРАЛТ — өмнөх хөлийн хэдэн хувийг ухарсан бэ.
     Elliott-оор 2-р давалгаа 50-61.8%, 4-р нь 38.2% ухардаг.
     Тэгвэл ухралтын ГҮН нь дараагийн хөлийг хэлэх ёстой.

  3. ЭЭЛЖЛЭЛ — гүехэн ухралтын дараах хөл нь гүн ухралтынхаас
     өөр үү.

БУЦААД ХАРАХААС сэргийлсэн: хөлийн дугаар ба ухралтын гүнийг
`confirm_index`-ээр БАТАЛГААЖСАН эргэлтийн цэгээс л тооцно. Сүүлийн
эргэлт нь хожим баталгаажих тул түүнийг мэдэж байсан гэж үзэхгүй.

zigzag-ийн pct нь БҮХ дүгнэлтэд нөлөөлнө (core.py-ийн анхааруулга),
тиймээс 2%, 3%, 5% гурваар давтана.

    python3 d1_elliott.py
"""
import argparse
import numpy as np
import pandas as pd
from core import zigzag, confirm_index
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

FIB = [(0, .382, '<38%'), (.382, .5, '38-50%'), (.5, .618, '50-62%'),
       (.618, .786, '62-79%'), (.786, 9, '>79%')]


def legs(d, pct):
    """Өдөр бүрд: (хөлийн дугаар, сүүлийн ухралтын гүн, хөлийн чиглэл).

    Бүгд нь тухайн өдөр МЭДЭГДЭЖ байсан мэдээллээр.
    """
    n = len(d)
    piv = []
    for pi, pv, pdir in zigzag(d, pct):
        ci = confirm_index(d, pi, pv, pdir, pct)
        if ci is not None and ci < n:
            piv.append((ci, pv, pdir))
    piv.sort()

    leg = np.zeros(n, int)
    ret = np.full(n, np.nan)
    dirn = np.zeros(n, int)
    pts = []
    k = 0
    cur_leg, cur_ret, cur_dir = 0, np.nan, 0
    for i in range(n):
        while k < len(piv) and piv[k][0] <= i:
            pts.append(piv[k][1:])
            k += 1
            if len(pts) >= 3:
                # Сүүлийн гурван цэг: A → B → C
                a, b, c = pts[-3][0], pts[-2][0], pts[-1][0]
                span = abs(b - a)
                cur_ret = abs(c - b) / span if span > 0 else np.nan
                cur_dir = 1 if pts[-1][1] == -1 else -1   # дараагийн хөл
                # Хөлийн дугаар: ижил чиглэлийн дараалсан хөлийг тоолно
                cur_leg = 1
                for t in range(len(pts) - 1, 0, -1):
                    if (pts[t][0] > pts[t - 1][0]) == (c > b):
                        cur_leg += 1
                    else:
                        break
                cur_leg = min(cur_leg, 6)
        leg[i], ret[i], dirn[i] = cur_leg, cur_ret, cur_dir
    return leg, ret, dirn


def trades(d, pct):
    leg, ret, dirn = legs(d, pct)
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = (d.atr14.to_numpy(), d.up.to_numpy(), d.dn.to_numpy())
    sq = d.sq.to_numpy()
    q20 = np.nanquantile(sq, .2)
    n = len(d)
    rows = []
    for i in np.where(sq <= q20)[0]:
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
        rows.append((leg[i], ret[i], dirn[i], side,
                     side * (out - lvl) / risk - .25 / risk))
    return pd.DataFrame(rows, columns=['leg', 'ret', 'edir', 'side', 'R'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pcts', default='0.02,0.03,0.05')
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

    for pct in [float(x) for x in a.pcts.split(',')]:
        t = trades(d, pct)
        print(f'\n{"="*66}\nzigzag {pct:.0%}   {len(t)} задрал')
        print('=' * 66)

        print('\n  ХӨЛИЙН ДУГААР (Elliott-оор 3-р нь хамгийн хүчтэй байх ёстой):')
        for k in range(1, 6):
            g = t[t.leg == k]
            if len(g) >= 25:
                print(f'    {k}-р хөл  n={len(g):4}  {g.R.mean():+.3f}R  '
                      f'ялсан {(g.R > 0).mean():.0%}')

        print('\n  ФИБОНАЧЧИЙН УХРАЛТЫН ГҮН:')
        for lo, hi, nm in FIB:
            g = t[(t.ret >= lo) & (t.ret < hi)]
            if len(g) >= 25:
                print(f'    {nm:8} n={len(g):4}  {g.R.mean():+.3f}R  '
                      f'ялсан {(g.R > 0).mean():.0%}')

        print('\n  ДАВАЛГААНЫ ХҮЛЭЭЛТИЙН ЧИГЛЭЛД задарсан уу:')
        for m, nm in ((t.edir == t.side, 'хүлээлттэй ижил'),
                      (t.edir == -t.side, 'эсрэг')):
            g = t[m]
            if len(g) >= 25:
                print(f'    {nm:16} n={len(g):4}  {g.R.mean():+.3f}R  '
                      f'ялсан {(g.R > 0).mean():.0%}')

    print('\n\nДүгнэх дүрэм: гурван pct-д ЖИГД давтагдаагүй ялгаа бол')
    print('zigzag-ийн параметрийн үр дүн — Elliott-ийн нотолгоо БИШ.')


if __name__ == '__main__':
    main()
