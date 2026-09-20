"""d4. ЗАДРАЛ жижигээс том руу хэрхэн тархдаг вэ — 5м → өдөр.

Санаа: том бар нь жижиг барнаас УГСРАГДДАГ. Тиймээс өдрийн задрал
болоход 5м, 15м, 1ц, 4ц бүгд тэр зүг рүү явж байх ёстой. Тэгвэл:

  1. КАСКАД — аль давхрага ЭХЛЭЭД задардаг вэ. 5м хамгийн түрүүнд
     задарч, дараа нь 15м, 1ц … гэж дараалдаг уу. Хэрэв тийм бол
     жижиг давхрага нь ЭРТ анхааруулга өгнө.

  2. ЭГНЭЭ — задрах мөчид доод давхрагууд хэд нь тэр зүг рүү
     чиглэсэн байна вэ. Олон нь эгнэсэн бол үр дүн дээр үү.

Эгнээг хэмжих: давхрага бүрийн хаалт өөрийнхөө 20 барын дунджаас
дээш байна уу (дээш задралд). Энгийн, тогтвортой, параметр цөөн.

ЗАНГА: доод давхрагууд том давхрагатай АВТОМАТААР нийцэх хандлагатай
— өдрийн үнэ дээшилж байвал 1 цагийнх ч дээшилсэн байна. Тиймээс
«эгнээ бүрэн» гэдэг нь ихэнх тохиолдолд биелэх ба ялгаа гарахгүй
байж магадгүй. Тархалтыг нь ЗААВАЛ хэвлэж, бодит ялгаа байгаа эсэхийг
хар.

    python3 d4_shatlal.py
"""
import argparse
import numpy as np
import pandas as pd
from core import load
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

TFS = ['5min', '15min', '1h', '4h']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=.25)
    ap.add_argument('--base', default='1D', choices=('1D', '4h'))
    a = ap.parse_args()

    h5 = load('XAU_5m_data.csv')

    # Доод давхрага бүрийн «чиглэл» ба өөрийн хил
    low = {}
    for tf in TFS:
        x = h5.resample(tf).agg(high=('high', 'max'), low=('low', 'min'),
                                close=('close', 'last')).dropna()
        pc = x.close.shift(1)
        tr = pd.concat([x.high - x.low, (x.high - pc).abs(),
                        (x.low - pc).abs()], axis=1).max(axis=1)
        m = x.close.rolling(20).mean()
        atr = tr.rolling(14).mean()
        x['above'] = (x.close > m).astype(float)     # чиглэл
        x['up'] = m + 1.5 * atr
        x['dn'] = m - 1.5 * atr
        low[tf] = x.dropna(subset=['up', 'above'])

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2010-01-01'].copy()
    tr = true_range(d)
    d['atr'] = tr.rolling(14).mean()
    d['sq'] = d.atr / tr.rolling(100).mean()
    m20 = d.close.rolling(20).mean()
    d['up'], d['dn'] = m20 + 1.5 * d.atr, m20 - 1.5 * d.atr
    d = d.dropna(subset=['sq', 'up', 'atr'])

    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = d.atr.to_numpy(), d.up.to_numpy(), d.dn.to_numpy()
    sq = d.sq.to_numpy()
    q20 = np.nanquantile(sq, .2)
    n = len(d)
    rows = []

    for i in np.where(sq <= q20)[0]:
        if not np.isfinite(A[i]) or A[i] <= 0 or U[i] <= DN[i]:
            continue
        pos = (C[i] - DN[i]) / (U[i] - DN[i])
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

        # Задрах ЯГ мөчийг 5м-ээс олно
        t0 = d.index[ej - 1].normalize() + pd.Timedelta(hours=DAY_CLOSE_HOUR + 1)
        t1 = d.index[ej].normalize() + pd.Timedelta(hours=DAY_CLOSE_HOUR + 1)
        w = h5.loc[t0:t1]
        if len(w) == 0:
            continue
        hitm = w.index[(w.high >= lvl) if side > 0 else (w.low <= lvl)]
        if len(hitm) == 0:
            continue
        tm = hitm[0]

        # ЭГНЭЭ — тэр мөчид доод давхрагууд хэд нь тэр зүгт
        # НЭР: `align` гэж нэрлэж БОЛОХГҮЙ — DataFrame.align() аргатай
        # мөргөлдөж, t.align нь багана биш функц буцаана (`squeeze`-тэй
        # ижил занга, энэ ажилд хоёр дахь удаагаа).
        algn = 0
        for tf in TFS:
            x = low[tf]
            k = x.index.searchsorted(tm, side='right') - 1
            if k < 0:
                continue
            ab = x['above'].iloc[k]
            if (ab == 1 and side > 0) or (ab == 0 and side < 0):
                algn += 1

        # КАСКАД — давхрага бүр өөрийн хилээ хэдэн цагийн өмнө эвдсэн
        lead = {}
        for tf in TFS:
            x = low[tf]
            k = x.index.searchsorted(tm, side='right') - 1
            s = max(0, k - 200)
            seg = x.iloc[s:k + 1]
            if len(seg) == 0:
                continue
            br = (seg.high >= seg.up) if side > 0 else (seg.low <= seg.dn)
            idx = seg.index[br.to_numpy()]
            lead[tf] = ((tm - idx[-1]).total_seconds() / 3600
                        if len(idx) else np.nan)

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
        rows.append(dict(date=d.index[ej], side=side, pos=pos, algn=algn,
                         R=side * (out - lvl) / risk - a.spread / risk,
                         **{f'ld_{t}': lead.get(t, np.nan) for t in TFS}))

    t = pd.DataFrame(rows)
    print(f'{len(t)} задрал   2010–2026\n')

    print('  КАСКАД — давхрага бүр өдрийн задралаас хэдэн ЦАГИЙН ӨМНӨ')
    print('  өөрийн хилээ эвдсэн бэ (медиан):')
    for tf in TFS:
        v = t[f'ld_{tf}'].dropna()
        if len(v):
            print(f'    {tf:6}  {v.median():7.1f} цаг өмнө   '
                  f'(25%: {v.quantile(.25):.1f}, 75%: {v.quantile(.75):.1f})')

    print('\n  ЭГНЭЭ — задрах мөчид хэдэн давхрага тэр зүгт байсан бэ:')
    up = t[t.side == 1]
    print(f'    {"эгнээ":8}{"тоо":>7}{"хувь":>8}{"R":>10}{"ялсан":>8}')
    for k in range(5):
        g = up[up.algn == k]
        if len(g) >= 15:
            print(f'    {k}/4{"":5}{len(g):7}{len(g) / len(up):8.0%}'
                  f'{g.R.mean():+10.3f}{(g.R > 0).mean():8.0%}')

    print('\n  ДЭЭД байрлалын дээш задрал дотор эгнээний нөлөө:')
    hi = up[up.pos >= up.pos.quantile(.5)]
    for k in (2, 3, 4):
        g = hi[hi.algn == k]
        if len(g) >= 12:
            print(f'    эгнээ {k}/4  n={len(g):4}  {g.R.mean():+.3f}R')


if __name__ == '__main__':
    main()
