"""b4. ЧИГЛЭЛ БИШ — ХЭМЖЭЭ. Маргааш хэр их хөдлөх вэ?

b3 чиглэл таамаглах боломжгүйг харуулав. Гэхдээ a28 «АНУ-ын том мэдээ
— хэмжээнд 4.4 дахин нөлөө, чиглэлд тэг» гэж олсон байсан. Тэр санааг
одоо бүтэн багц дээр шалгана.

Зорилт: маргаашийн |өгөөж| (хэдэн хувиар хөдлөх, аль тийш нь биш).

Яагаад энэ нь бодитой зорилт вэ: хэлбэлзэл БӨӨГНӨРДӨГ — тайван өдрийн
маргааш тайван, шуургатай өдрийн маргааш шуургатай байх хандлагатай.
Энэ нь санхүүгийн хамгийн тогтвортой ажиглагдсан зүй тогтлуудын нэг.
Тиймээс «таамаглаж чадах уу» гэдэг нь буруу асуулт — чадна. Зөв
асуулт нь: ЭНГИЙН аргаас илүү үү?

Тиймээс гурван хатуу суурьтай харьцуулна:

    тогтмол   — сургалтын дундаж. Хамгийн тэнэг таамаг.
    өчигдөр   — өчигдрийн |өгөөж|. Санамсаргүй алхалт.
    vol_20d   — 20 хоногийн хэлбэлзэл. АРИЛЖААЧДЫН ХЭРЭГЛЭДЭГ арга.
                Үүнийг давахгүй бол загвар нэмэх зүйлгүй.

Хэмжүүр: MAE (дундаж алдаа) ба Spearman зэрэглэл. Зэрэглэл нь илүү
чухал — бидэнд яг тоо биш, «маргааш чимээгүй юу, шуургатай юу» гэдэг
эрэмбэ л хэрэгтэй.

Практик шалгалт: таамагласан хамгийн тайван 20% ба хамгийн шуургатай
20% өдрүүдийн ЖИНХЭНЭ хөдөлгөөн хэр зөрөх вэ. Энэ зөрүү том бол
байрын хэмжээ, стопын зай тогтооход хэрэглэж болно.

    python3 b4_hemjee.py [--horizon 1]
"""
import argparse
import os
import numpy as np
import pandas as pd
from core import DATA
from b3_suuri import load, guard, TEST_YEARS


def spearman(a, b):
    m = ~(np.isnan(a) | np.isnan(b))
    if m.sum() < 10:
        return np.nan
    ra = pd.Series(a[m]).rank().to_numpy()
    rb = pd.Series(b[m]).rank().to_numpy()
    return np.corrcoef(ra, rb)[0, 1]


def score(name, true, pred, extra=''):
    mae = np.nanmean(np.abs(true - pred))
    rho = spearman(true, pred)
    print(f'  {name:16} MAE {mae:6.3f}   зэрэглэл {rho:6.3f} {extra}')
    return mae, rho


def spread(true, pred, q=.2):
    """Таамагласан тайван 20% ба шуургатай 20%-ийн ЖИНХЭНЭ хөдөлгөөн."""
    m = ~(np.isnan(true) | np.isnan(pred))
    t, p = true[m], pred[m]
    lo, hi = np.quantile(p, q), np.quantile(p, 1 - q)
    return t[p <= lo].mean(), t[p >= hi].mean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='GOLD_Features_Full.csv')
    ap.add_argument('--horizon', type=int, default=1, choices=(1, 3, 5))
    a = ap.parse_args()

    from sklearn.ensemble import HistGradientBoostingRegressor

    d, S, lab = load(os.path.join(DATA, a.data), a.horizon)
    d['mag'] = d[lab].abs()                     # ЗОРИЛТ: хэмжээ
    for _n, _f in S.items():
        guard(d, _f, d['mag'])
    print(f'{a.data}   давхрага {a.horizon} хоног   зорилт: |өгөөж|')
    print(f'   бүх хугацааны дундаж хөдөлгөөн: {d.mag.mean():.3f}%\n')

    for ty in TEST_YEARS:
        tr, te = d[d.year < ty], d[d.year == ty]
        if len(tr) < 250 or len(te) < 50:
            continue
        true = te.mag.to_numpy(float)
        print(f'─── {ty}   ({len(te)} өдөр, жинхэнэ дундаж '
              f'{np.nanmean(true):.3f}%) ───')

        # Суурь гурав
        score('тогтмол', true, np.full(len(te), tr.mag.mean()))
        score('өчигдөр', true, te[f'price_return_{a.horizon}d'].abs().to_numpy(float))
        base_mae, base_rho = score('vol_20d', true,
                                   te.tech_vol_20d.to_numpy(float))

        # Загварууд
        for name, feat in S.items():
            m = HistGradientBoostingRegressor(
                max_iter=200, max_depth=3, learning_rate=.05,
                l2_regularization=1.0, min_samples_leaf=40, random_state=0)
            m.fit(tr[feat].to_numpy(float), tr.mag.to_numpy(float))
            p = m.predict(te[feat].to_numpy(float))
            mae, rho = score(f'загвар {name}', true, p)
            lo, hi = spread(true, p)
            print(f'{"":18}  тайван 20% → {lo:.3f}%   '
                  f'шуургатай 20% → {hi:.3f}%   ({hi / lo:.2f} дахин)')
        # vol_20d-ийн зэрэглэлийн хүчийг мөн харуулна
        lo, hi = spread(true, te.tech_vol_20d.to_numpy(float))
        print(f'{"vol_20d":18}  тайван 20% → {lo:.3f}%   '
              f'шуургатай 20% → {hi:.3f}%   ({hi / lo:.2f} дахин)')
        print()

    print('Яаж унших вэ: загварын зэрэглэл нь vol_20d-ийнхээс ӨНДӨР байж,')
    print('MAE нь ДООГУУР байж байж л нэмэх зүйлтэй гэсэн үг. Хэлбэлзэл')
    print('бөөгнөрдөг тул «таамаглаж чадсан» нь өөрөө ололт биш.')


if __name__ == '__main__':
    main()
