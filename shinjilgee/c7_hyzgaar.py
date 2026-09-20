"""c7. Шахалтын ХИЛ хаана вэ — «эндээс хэтэрвэл задарлаа» гэдэг цэг.

b6-c6 бүгд «20 хоногийн дээд/доод» гэдгийг ДУР МЭДЭН сонгосон. Энд
тэр сонголтыг шалгана: аль тодорхойлолт хамгийн сайн ялгаж байна вэ,
мөн хилээс хэр хол хэтэрвэл жинхэнэ задрал гэж үзэх вэ.

Шалгах ХИЛҮҮД:

    N хоногийн муж   — сүүлийн 5 / 10 / 20 барын дээд, доод
    шахалтын муж     — шахалт ЭХЭЛСЭНЭЭС хойшхи дээд, доод
                       (хамгийн «зөв» мэт санагддаг тодорхойлолт)
    Bollinger 2σ     — 20 барын дундаж ± 2 стандарт хазайлт
    ATR зурвас       — 20 барын дундаж ± 1.5 ATR

БАТАЛГААНЫ БУФЕР: хил дээр яг хүрэхэд орох уу, эсвэл 0.25 / 0.5 ATR
хэтрэхийг хүлээх үү. Буфер нь хуурамч задралыг шүүх ёстой — гэхдээ
сайн хөдөлгөөний эхний хэсгийг ч алдуулна. Аль нь давамгайлахыг
өгөгдөл хэлнэ.

Хоёр зүйлийг зэрэг хардаг нь чухал:

    ҮРГЭЛЖЛЭЛ — задарсны дараа хэр явсан (ATR)
    ХУУРАМЧ   — задраад буцаад эсрэг хилийг нь эвдсэн хувь

Зөвхөн үргэлжлэлийг харвал хатуу буфер үргэлж «сайн» харагдана —
учир нь муу задралуудыг шүүгээд хаячихдаг. Тиймээс АЛДСАН
боломжийг ч тоолно (хэдэн дохио үлдэв).

    python3 c7_hyzgaar.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def boundaries(d):
    """Нэр → (доод массив, дээд массив)."""
    H, L, C = d.high, d.low, d.close
    out = {}
    for k in (5, 10, 20):
        out[f'{k} барын муж'] = (L.rolling(k).min().to_numpy(),
                                 H.rolling(k).max().to_numpy())
    m20 = C.rolling(20).mean()
    sd = C.rolling(20).std()
    out['Bollinger 2σ'] = ((m20 - 2 * sd).to_numpy(), (m20 + 2 * sd).to_numpy())
    atr = d.atr14
    out['ATR зурвас 1.5'] = ((m20 - 1.5 * atr).to_numpy(),
                             (m20 + 1.5 * atr).to_numpy())
    return out


def squeeze_range(d, thresh):
    """Шахалт ЭХЭЛСЭНЭЭС хойшхи дээд/доод — өсөн тэлэх муж."""
    sq = d.sq.to_numpy()
    H, L = d.high.to_numpy(), d.low.to_numpy()
    n = len(d)
    lo = np.full(n, np.nan)
    hi = np.full(n, np.nan)
    st = None
    for i in range(n):
        if sq[i] < thresh:
            if st is None:
                st = i
            lo[i] = L[st:i + 1].min()
            hi[i] = H[st:i + 1].max()
        else:
            st = None
    return lo, hi


def run(d, mask, lo, hi, buf, wait=5, hold=10):
    H, L = d.high.to_numpy(), d.low.to_numpy()
    A = d.atr14.to_numpy()
    n = len(d)
    mfes, fakes = [], []
    for i in np.where(mask)[0]:
        if not np.isfinite(A[i]) or A[i] <= 0 or not np.isfinite(hi[i]):
            continue
        up, dn = hi[i] + buf * A[i], lo[i] - buf * A[i]
        lvl = side = ej = None
        for j in range(i + 1, min(i + 1 + wait, n)):
            hu, hd = H[j] >= up, L[j] <= dn
            if hu and hd:
                break
            if hu:
                lvl, side, ej = up, 1, j
                break
            if hd:
                lvl, side, ej = dn, -1, j
                break
        if lvl is None:
            continue
        k = min(ej + hold, n)
        hh, ll = H[ej:k].max(), L[ej:k].min()
        mfes.append((hh - lvl) / A[i] if side > 0 else (lvl - ll) / A[i])
        fakes.append(int((ll <= dn) if side > 0 else (hh >= up)))
    return np.array(mfes), np.array(fakes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--thresh', type=float, default=.85)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d = d.dropna(subset=['sq', 'atr14'])

    B = boundaries(d)
    B['шахалтын муж'] = squeeze_range(d, a.thresh)
    mask = (d.sq <= d.sq.quantile(.2)).to_numpy()

    print(f'Шахагдсан 20% ({mask.sum()} өдөр)   буфер = хилээс цааш ATR\n')
    print(f'{"хил":18} {"буфер":>6} {"дохио":>7} {"ҮРГЭЛЖЛЭЛ":>10} '
          f'{"медиан":>8} {"хуурамч":>8}')
    print('─' * 64)
    for nm, (lo, hi) in B.items():
        for buf in (0.0, .25, .5, 1.0):
            m, f = run(d, mask, lo, hi, buf)
            if len(m) < 50:
                continue
            print(f'{nm if buf == 0 else "":18} {buf:6.2f} {len(m):7} '
                  f'{m.mean():10.2f} {np.median(m):8.2f} {f.mean():8.0%}')
        print()

    print('  Буфер өсгөхөд дохио цөөрч, үргэлжлэл өсдөг нь ХЭВИЙН —')
    print('  муу задралуудыг шүүсний үр дүн. Асуулт нь: цөөрсөн дохионы')
    print('  хэрээр үргэлжлэл ХАНГАЛТТАЙ өсч байна уу.')


if __name__ == '__main__':
    main()
