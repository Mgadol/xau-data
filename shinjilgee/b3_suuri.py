"""b3. СУУРЬ ТЕСТ — гадаад мэдээлэл таамаглахад тус болох уу?

Ганц асуулт: 60 баганат багц маргаашийн чиглэлийг ЗАРДЛЫН ДАРАА
таамаглаж чадах уу? Хариулт нь «үгүй» байсан ч ХЭРЭГТЭЙ — a1…a28
шинжилгээнүүдийн адил, юу болохгүйг мэдэх нь мөнгө хэмнэдэг.

Гурван багцыг харьцуулна:

    суурь  — «үргэлж UP». Юу ч сураагүй загвар. 2020-2026 бол алтны
             өсөлтийн үе тул энэ дангаараа 50%-иас дээш гарна. Үүнийг
             давахгүй загвар нь юу ч сураагүй гэсэн үг.
    үнэ    — 45 багана, бүгд алтны үнийн хувирал
    бүтэн  — 60 багана, гадаад мэдээлэлтэй

Өөрийгөө хуурахаас сэргийлсэн дүрмүүд:

  · ЦАГ ХУГАЦААНЫ дараалал хатуу. Холихгүй, санамсаргүй хуваахгүй.
    Сургалт үргэлж шалгалтаас ӨМНӨ байна.
  · Дутууг нөхөх дундаж, масштабын коэффициентийг ЗӨВХӨН сургалтын
    хэсгээс тооцно. Бүтэн багц дээр тооцвол ирээдүйн тархалт
    сургалтад нэвчинэ.
  · Нэг хуваалт биш, ГУРВАН жилээр (2023, 2024, 2025) тус тусад нь.
    Нэг жилд азаар сайн гарч болно, гурвуулаа биш.
  · Нарийвчлал ХАНГАЛТГҮЙ. Зардлын дараах цэвэр өгөөжийг хэмжинэ.
    56% нарийвчлалтай ч спред идчихвэл ашиггүй.

Зардал: нэг удаагийн арилжаанд 0.03% (нээх + хаах). XAUUSD-ийн спред
ихэвчлэн $0.20-0.50 — $2000-4000 үнэ дээр 0.01-0.025%. Гулсалт нэмээд
0.03% нь бодитой. `--cost`-оор өөрчилж мэдрэмжийг шалгана.

    python3 b3_suuri.py [--cost 0.03] [--horizon 1]
"""
import argparse
import os
import sys
import numpy as np
import pandas as pd
from core import DATA

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TEST_YEARS = (2023, 2024, 2025)


def sets(cols):
    """Багана → хоёр багц: зөвхөн үнэ, ба бүтэн.

    `y` нь ЗОРИЛТОТ багана — энд орвол загвар хариултаа шууд хараад
    100% нарийвчлал өгнө. Нэг удаа яг ингэж болсон тул нэрээр нь
    хассаны дээр доорх guard() давхар шалгана.
    """
    drop = {'date', 'year', 'day_of_week', 'price_close', 'y'}
    feat = [c for c in cols if c not in drop and not c.startswith('label')]
    ext = [c for c in feat if c.startswith(('macro_', 'mkt_'))]
    return {'үнэ': [c for c in feat if c not in ext], 'бүтэн': feat}


def guard(d, feat, y_col):
    """Нэвчилтийн хамгаалалт — сэжигтэй бол ШУУД зогсооно.

    Санамсаргүй нэмэгдсэн нэг багана бүх дүнг утгагүй болгодог. Тэр нь
    чимээгүй өнгөрвөл «загвар ажиллаж байна» гэж итгэчихнэ.
    """
    bad = [c for c in feat if c == y_col or c.startswith('label')]
    if bad:
        raise SystemExit(f'НЭВЧИЛТ: зорилтот багана шинжид орсон — {bad}')
    y = d[y_col]
    hot = [(c, abs(d[c].corr(y))) for c in feat if d[c].dtype.kind in 'fi']
    hot = [(c, v) for c, v in hot if v == v and v > .5]
    if hot:
        raise SystemExit('НЭВЧИЛТ: шошготой хэт нийцсэн шинж — '
                         + ', '.join(f'{c} ({v:.2f})' for c, v in hot))


def run_fold(d, feat, y_col, test_year, seed=0):
    """Нэг жилийг шалгалт болгож, түүнээс ӨМНӨХ бүхнээр сургана."""
    from sklearn.ensemble import HistGradientBoostingClassifier

    tr = d[d.year < test_year]
    te = d[d.year == test_year]
    if len(tr) < 250 or len(te) < 50:
        return None

    Xtr, Xte = tr[feat].to_numpy(float), te[feat].to_numpy(float)
    ytr, yte = tr[y_col].to_numpy(int), te[y_col].to_numpy(int)

    m = HistGradientBoostingClassifier(
        max_iter=200, max_depth=3, learning_rate=.05,
        l2_regularization=1.0, min_samples_leaf=40, random_state=seed)
    m.fit(Xtr, ytr)
    p = m.predict_proba(Xte)[:, 1]
    return te, p, yte


def evaluate(te, p, yte, cost, thresh=.5):
    """Нарийвчлал ба ЗАРДЛЫН ДАРААХ цэвэр өгөөж."""
    pred = (p >= thresh).astype(int)
    acc = (pred == yte).mean()

    # Арилжаа: таамаг UP бол урт, DOWN бол богино. Өдөр бүр байр солино
    # гэж үзээд өдөр бүрд зардал тооцно — хамгийн хатуу таамаглал.
    r = te['label_return_1d'].to_numpy(float)
    side = np.where(pred == 1, 1.0, -1.0)
    gross = side * r
    net = gross - cost
    return dict(acc=acc, gross=np.nansum(gross), net=np.nansum(net),
                n=len(te), win=(np.nan_to_num(net) > 0).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='GOLD_Features_Full.csv')
    ap.add_argument('--cost', type=float, default=.03,
                    help='нэг арилжааны зардал, хувиар')
    ap.add_argument('--horizon', type=int, default=1, choices=(1, 3, 5))
    a = ap.parse_args()

    d = pd.read_csv(os.path.join(DATA, a.data), parse_dates=['date'])
    d['year'] = d.date.dt.year
    lab = f'label_return_{a.horizon}d'
    d = d[d[lab].notna()].copy()
    d['y'] = (d[lab] > 0).astype(int)

    S = sets(d.columns)
    for _n, _f in S.items():
        guard(d, _f, 'y')
    print(f'{a.data}: {len(d):,} мөр   давхрага {a.horizon} хоног   '
          f'зардал {a.cost}%')
    print('   багцууд: ' + ',  '.join(f'{n} = {len(f)} шинж'
                                      for n, f in S.items()) + '\n')

    # ── Суурь: үргэлж UP ─────────────────────────────────────────────
    print('─' * 66)
    print(f'{"багц":14} {"жил":>5} {"нарийвчлал":>11} {"нийт %":>9} '
          f'{"зардлын дараа":>14}')
    print('─' * 66)
    rows = []
    for ty in TEST_YEARS:
        te = d[d.year == ty]
        if len(te) < 50:
            continue
        r = te[lab].to_numpy(float)
        acc = (r > 0).mean()
        rows.append(('үргэлж UP', ty, acc, np.nansum(r),
                     np.nansum(r) - a.cost * len(te)))
    for n, y, ac, g, ne in rows:
        print(f'{n:14} {y:5} {ac:10.1%} {g:9.1f} {ne:14.1f}')

    # ── Загварууд ────────────────────────────────────────────────────
    for name, feat in S.items():
        print('─' * 66)
        tot = []
        for ty in TEST_YEARS:
            out = run_fold(d, feat, 'y', ty)
            if out is None:
                continue
            te, p, yte = out
            e = evaluate(te, p, yte, a.cost)
            tot.append(e)
            print(f'{name:14} {ty:5} {e["acc"]:10.1%} {e["gross"]:9.1f} '
                  f'{e["net"]:14.1f}')
        if tot:
            acc = np.mean([e['acc'] for e in tot])
            net = np.sum([e['net'] for e in tot])
            print(f'{name:14} {"дүн":>5} {acc:10.1%} '
                  f'{np.sum([e["gross"] for e in tot]):9.1f} {net:14.1f}')
    print('─' * 66)
    print('\nЯаж унших вэ: «зардлын дараа» багана нь эерэг бөгөөд «үргэлж UP»-ийн')
    print('мөрөөс ӨНДӨР байвал л загвар ямар нэг зүйл сурсан гэсэн үг.')
    print('Нарийвчлал дангаараа хангалтгүй — 55% нарийвчлалтай ч зардал идэж болно.')


if __name__ == '__main__':
    main()
