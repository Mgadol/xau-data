"""b5. Маргаашийн ӨДРИЙН МУЖ — стоп хаана тавих вэ?

b4 хаалтаас хаалт хүртэлх |өгөөж|-ийг авсан. Тэр нь арилжаанд хэрэг
болох тоо БИШ: өдөр дотроо 2% явчихаад буцаж ирвэл |өгөөж| нь бараг
тэг гарна, гэтэл стоп чинь аль хэдийн цохигдсон байна.

Арилжаанд үнэндээ хэрэгтэй нь ӨДРИЙН МУЖ — (дээд − доод) / хаалт.
Энэ нь «маргааш үнэ хэр хол явах вэ» гэдгийг хэлнэ:

    · стопыг хаана тавих (мужаас дотогш тавивал цохиулна)
    · байрын хэмжээг хэр авах (муж өргөн өдөр жижиг байр)
    · зорилтоо хэр хол тавих

a24 «том хөдөлгөөн ирэх үү — ТИЙМ, таамаглагдана» гэж олсон. Энэ нь
тэр санааг макро өгөгдөлтэй хамт, хатуу суурьтай шалгана.

Суурь нь ATR-14 — арилжаачдын ХЭРЭГЛЭДЭГ стандарт. MetaTrader, TradingView
бүгдэд нь байдаг, стопын зайг ихэвчлэн үүгээр тавьдаг. Загвар үүнийг
давахгүй бол нэмэх зүйлгүй: хүн аль хэдийн ATR-ээ хардаг.

Практик гаралт нь `atr_calib()` — маргаашийн муж нь ӨНӨӨДРИЙН ATR-14-ийн
хэдэн дахин болохыг хувиар харуулна. Стопын зай шууд эндээс гарна.

    python3 b5_muj.py
"""
import argparse
import os
import numpy as np
import pandas as pd
from core import DATA
from b1_features import daily, DAY_CLOSE_HOUR
from b3_suuri import load, guard, TEST_YEARS
from b4_hemjee import spearman


def atr_calib(d):
    """Маргаашийн муж = ӨНӨӨДРИЙН ATR-14 × хэд вэ. Стопын зай эндээс."""
    r = (d.target / d.atr14).dropna()
    print(f'\nМаргаашийн муж нь өнөөдрийн ATR-14-ийн хэдэн дахин вэ '
          f'(n={len(r)}):')
    for q in (.5, .8, .9, .95, .99):
        print(f'  {q:5.0%} тохиолдолд  {r.quantile(q):.2f} дахинаас бага')
    print('  жилээр (90% хувь): ' + '  '.join(
        f'{y}:{r[r.index.isin(d.index[d.year == y])].quantile(.9):.2f}'
        for y in sorted(d.year.unique()) if (d.year == y).sum() > 30))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='GOLD_Features_Full.csv')
    a = ap.parse_args()

    from sklearn.ensemble import HistGradientBoostingRegressor

    d, S, _lab = load(os.path.join(DATA, a.data), 1)

    # ── Зорилт: МАРГААШИЙН муж ───────────────────────────────────────
    # Өдрийн OHLC-г b1-тэй ИЖИЛ хилээр (18:00) дахин гаргана — өөр
    # хилээр бодвол муж нь багцын бусад тоотой зөрнө.
    bars = daily(close_hour=DAY_CLOSE_HOUR)
    rng = ((bars.high - bars.low) / bars.close * 100).rename('rng')
    d = d.merge(rng, left_on='date', right_index=True, how='left')
    d['atr14'] = rng.reindex(d.date).rolling(14).mean().to_numpy()  # ӨНӨӨДРИЙН
    d['target'] = d.rng.shift(-1)                                   # МАРГААШИЙН
    d = d[d.target.notna() & d.atr14.notna()].copy()

    for _n, _f in S.items():
        guard(d, _f, d['target'])

    print(f'Зорилт: маргаашийн (дээд−доод)/хаалт, %   |   {len(d):,} өдөр')
    print(f'Бүх хугацааны дундаж муж: {d.target.mean():.3f}%\n')

    for ty in TEST_YEARS:
        tr, te = d[d.year < ty], d[d.year == ty]
        if len(tr) < 250 or len(te) < 50:
            continue
        true = te.target.to_numpy(float)
        print(f'─── {ty}  ({len(te)} өдөр, жинхэнэ дундаж муж '
              f'{true.mean():.3f}%) ───')
        print(f'  {"арга":18} {"MAE":>6} {"зэрэглэл":>9} '
              f'{"тайван20%":>10} {"шуурга20%":>10} {"таамгаас давсан":>16}')

        def show(name, pred):
            pred = np.asarray(pred, float)
            m = ~np.isnan(pred)
            mae = np.nanmean(np.abs(true[m] - pred[m]))
            rho = spearman(true, pred)
            lo, hi = np.quantile(pred[m], .2), np.quantile(pred[m], .8)
            calm = true[m][pred[m] <= lo].mean()
            storm = true[m][pred[m] >= hi].mean()
            # Таамаг ДООГУУР гарсан өдрийн хувь (муж таамгаас давсан).
            # Энэ нь стопын тест БИШ — зүгээр л таамгийн хазайлтыг
            # харуулна. Жинхэнэ стопын тест нь орох цэг, чиглэл хоёрыг
            # шаардана, энд тэр хоёр байхгүй.
            hit = (true[m] > pred[m]).mean()
            print(f'  {name:18} {mae:6.3f} {rho:9.3f} {calm:10.3f} '
                  f'{storm:10.3f} {hit:15.0%}')

        show('тогтмол', np.full(len(te), tr.target.mean()))
        show('өнөөдрийн муж', te.rng.to_numpy(float))
        show('ATR-14', te.atr14.to_numpy(float))
        for name, feat in S.items():
            m = HistGradientBoostingRegressor(
                max_iter=200, max_depth=3, learning_rate=.05,
                l2_regularization=1.0, min_samples_leaf=40, random_state=0)
            m.fit(tr[feat].to_numpy(float), tr.target.to_numpy(float))
            show(f'загвар {name}', m.predict(te[feat].to_numpy(float)))
        print()

    print('Яаж унших вэ: загвар ATR-14-ээс MAE бага, зэрэглэл өндөр байж')
    print('байж л нэмэх зүйлтэй. Эс бөгөөс ATR-ийг шууд хэрэглэх нь дээр —')
    print('тэр нь MetaTrader дээр аль хэдийн байдаг.')
    atr_calib(d)


if __name__ == '__main__':
    main()
