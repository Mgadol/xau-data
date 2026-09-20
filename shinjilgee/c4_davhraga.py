"""c4. ХИЛ ХААНА ВЭ — 15м, 1ц, 4ц, 8ц, өдөр.

c3-д 15 минут дээр шахалтын эвдрэл спредгүй ч сөрөг гарав. b7-д өдрийн
график дээр +0.335R гарсан. Тэгвэл хил хаана вэ?

Бүх давхрагад ЯГ ИЖИЛ дүрэм ажиллуулна — зөвхөн барын урт өөр:

    шахалт = (цагаар цэвэрлэсэн) ATR14 / ATR96
    орох   = 20 барын муж эвдрэх
    стоп   = 2 ATR,  зорилт = 4 ATR,  16 бар барина

Цагийн цэвэрлэгээ: өдрийн доторх давхрагад бар бүрийн TR-ийг ТУХАЙН
ЦАГИЙН ердийн TR-т (өнгөрсөн 60 хоногийн ижил цаг) хуваана. Үгүй бол
«шахалт» нь зүгээр л «Ази байна» гэдгийг олно — c3-д батлагдсан.
Өдрийн графикт энэ шаардлагагүй (бар бүр нэг л өдөр).

Хоёр тоог зэрэгцүүлж хардаг нь чухал:

    ЗАРДАЛ — $0.25 спред нь стопын (2 ATR) хэдэн хувь вэ. Бар богино
             байх тусам ATR жижиг → зардал хүнд.
    ИРМЭГ  — спредгүй үеийн цэвэр R. Энэ нь бүтэц өөрөө ажиллаж
             байгаа эсэхийг хэлнэ.

Ирмэг зардлаас том болох цэг нь хил.

    python3 c4_davhraga.py
"""
import argparse
import numpy as np
import pandas as pd
from core import load

TFS = [('15min', 96), ('1h', 96), ('4h', 60), ('8h', 45), ('1D', 60)]


def build(h, tf, slow):
    d = h.resample(tf).agg(open=('open', 'first'), high=('high', 'max'),
                           low=('low', 'min'), close=('close', 'last'),
                           volume=('volume', 'sum')).dropna()
    d = d[d.index >= '2015-01-01']
    pc = d.close.shift(1)
    tr = pd.concat([d.high - d.low, (d.high - pc).abs(),
                    (d.low - pc).abs()], axis=1).max(axis=1)
    d['tr'] = tr
    d['atr'] = tr.rolling(14).mean()
    if tf == '1D':
        base = tr                                   # цаг цэвэрлэх хэрэггүй
    else:
        key = d.index.hour * 60 + d.index.minute
        base = pd.Series(np.nan, index=d.index)
        for k, g in d.groupby(key):
            prof = g.tr.rolling(60, min_periods=20).mean().shift(1)
            base.loc[g.index] = (g.tr / prof).to_numpy()
    d['sq'] = base.rolling(14).mean() / base.rolling(slow).mean()
    d['up'] = d.high.rolling(20).max()
    d['dn'] = d.low.rolling(20).min()
    return d.dropna(subset=['sq', 'atr', 'up'])


def run(d, mask, spread, wait=8, hold=16, k=2.0, m=4.0):
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    U, D, A = d.up.to_numpy(), d.dn.to_numpy(), d.atr.to_numpy()
    n = len(d)
    rs, costs = [], []
    for i in np.where(mask)[0]:
        if not np.isfinite(A[i]) or A[i] <= 0:
            continue
        risk = k * A[i]
        lvl = side = ej = None
        for j in range(i + 1, min(i + 1 + wait, n)):
            hu, hd = H[j] >= U[i], L[j] <= D[i]
            if hu and hd:
                break
            if hu:
                lvl, side, ej = U[i], 1, j
                break
            if hd:
                lvl, side, ej = D[i], -1, j
                break
        if lvl is None:
            continue
        stop, targ = lvl - side * risk, lvl + side * m * A[i]
        out = None
        for j in range(ej, min(ej + hold, n)):
            sh = (L[j] <= stop) if side > 0 else (H[j] >= stop)
            th = (H[j] >= targ) if side > 0 else (L[j] <= targ)
            if sh:
                out = stop
                break
            if th:
                out = targ
                break
        if out is None:
            out = C[min(ej + hold - 1, n - 1)]
        rs.append(side * (out - lvl) / risk - spread / risk)
        costs.append(spread / risk)
    return pd.Series(rs), float(np.mean(costs)) if costs else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    h = load('XAU_5m_data.csv')
    print(f'Спред ${a.spread:.2f}   дүрэм бүх давхрагад ИЖИЛ\n')
    print(f'{"давхрага":>9} {"бар":>8} {"ATR $":>8} {"зардал R":>9} | '
          f'{"ИРМЭГ (спредгүй)":>17} {"цэвэр (спредтэй)":>17} {"n":>7}')
    print('─' * 84)
    for tf, slow in TFS:
        d = build(h, tf, slow)
        q20 = d.sq.quantile(.2)
        m = (d.sq <= q20).to_numpy()
        raw, _ = run(d, m, 0.0)
        net, cost = run(d, m, a.spread)
        if len(raw) == 0:
            continue
        mark = '  ←' if raw.mean() > cost else ''
        print(f'{tf:>9} {len(d):8,} {d.atr.mean():8.2f} {cost:9.3f} | '
              f'{raw.mean():+17.3f} {net.mean():+17.3f} {len(net):7,}{mark}')

    print('\n  ИРМЭГ > зардал R байвал тэр давхрагад бүтэц зардлаа даана.')
    print('  Спредгүй ирмэг өөрөө сөрөг бол — бүтэц тэнд огт ажиллахгүй,')
    print('  зардал буруутай биш.')


if __name__ == '__main__':
    main()
