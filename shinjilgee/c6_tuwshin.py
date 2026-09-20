"""c6. АЛЬ түвшин үнэхээр онцгой вэ — өргөн хайлт.

c2, c5-д шахалттай холбоотой хоёр түвшин шалгагдаад онцгой биш гарав.
Гэхдээ арилжаачдын хэрэглэдэг өөр олон түвшин бий. Энд тэдгээрийг
БҮГДИЙГ НЬ нэг хэмжүүрээр, нэг хяналттай зэрэгцүүлнэ.

Шалгах түвшнүүд:

    эвдэрсэн муж    — 20 хоногийн дээд/доод эвдэрсэн түвшин
                      («эвдээд буцаж шалгадаг» гэсэн сонгодог санаа)
    өмнөх өдрийн    — өчигдрийн дээд ба доод
    өмнөх 7 хоногийн — сүүлийн 5 барын дээд ба доод
    эргэлтийн цэг   — 5 барын зүүн/баруун талаараа өндөр/нам (pivot)
    дугуй тоо       — $50-аар хуваагддаг түвшин
    шахалтын эхлэл  — c5-аас (харьцуулахын тулд)
    ХЯНАЛТ          — санамсаргүй өдрийн хаалт

ХОЁР зүйлийг зэрэг хэмжинэ. Зөвхөн нэгийг нь харвал төөрнө:

    БУЦСАН  — үнэ тэр түвшинд эргэж ирдэг үү (соронз уу)
    ХАРИУ   — ирээд хариу үйлдэл өгдөг үү (тулгуур уу)

Түвшин «80%-д буцаж ирдэг» байж болно — гэхдээ хяналт ч 80% бол тэр
нь түвшний шинж биш, үнийн шинж.

Зайг ҮНИЙН ХУВИАР хэмжинэ, ATR-аар биш. c5-д ATR-аар хэмжсэн нь
тэмдгийг эргүүлсэн: ATR жижиг бүлэгт «1 ATR холдох» нь доллараар
богино зай болж, буцалт хуурамчаар өснө.

    python3 c6_tuwshin.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

AWAY = .015      # түвшнээс энэ хувиар холдсоны дараа тоолж эхэлнэ


def measure(d, items, horizon, react=5):
    """items = [(индекс, түвшин)] → буцсан эсэх ба хариу үйлдэл."""
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A = d.atr14.to_numpy()
    n = len(d)
    out = []
    for i, lvl in items:
        if not np.isfinite(A[i]) or A[i] <= 0 or not np.isfinite(lvl):
            continue
        gap = AWAY * lvl
        j = i + 1
        while j < n and abs(C[j] - lvl) < gap:
            j += 1
        if j >= n or j - i > horizon:
            continue
        above = C[j] > lvl
        end = min(j + horizon, n)
        hit = None
        for k in range(j, end):
            if (L[k] <= lvl) if above else (H[k] >= lvl):
                hit = k
                break
        if hit is None:
            out.append((0, np.nan, np.nan))
            continue
        # Хариу үйлдэл: ирсэн зүг рүүгээ хэр түлхэгдэв (ATR-ийн дахин)
        e = min(hit + 1 + react, n)
        if e <= hit + 1:
            out.append((1, np.nan, np.nan))
            continue
        push = ((H[hit + 1:e].max() - lvl) if above
                else (lvl - L[hit + 1:e].min())) / A[hit]
        thru = (L[hit + 1:e].min() < lvl * (1 - AWAY / 2)) if above else \
               (H[hit + 1:e].max() > lvl * (1 + AWAY / 2))
        out.append((1, push, int(not thru)))
    return pd.DataFrame(out, columns=['back', 'push', 'held'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--horizon', type=int, default=40)
    ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d = d.dropna(subset=['sq', 'atr14']).reset_index()
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    n = len(d)
    u20 = d.high.rolling(20).max().to_numpy()
    l20 = d.low.rolling(20).min().to_numpy()
    sq = d.sq.to_numpy()

    lv = {}

    # 1. Эвдэрсэн муж — «эвдээд буцаж шалгана» гэсэн сонгодог санаа
    brk = []
    for i in range(21, n):
        if H[i] > u20[i - 1]:
            brk.append((i, u20[i - 1]))
        elif L[i] < l20[i - 1]:
            brk.append((i, l20[i - 1]))
    lv['эвдэрсэн муж (20х)'] = brk

    # 2. Өмнөх өдрийн дээд/доод
    lv['өчигдрийн дээд/доод'] = [(i, H[i - 1] if i % 2 else L[i - 1])
                                 for i in range(21, n)]

    # 3. Сүүлийн 5 барын дээд/доод
    lv['7 хоногийн дээд/доод'] = [
        (i, d.high[i - 5:i].max() if i % 2 else d.low[i - 5:i].min())
        for i in range(21, n)]

    # 4. Эргэлтийн цэг (pivot) — 5 талдаа
    piv = []
    for i in range(26, n - 5):
        w = slice(i - 5, i + 6)
        if H[i] == d.high[w].max():
            piv.append((i + 5, H[i]))
        elif L[i] == d.low[w].min():
            piv.append((i + 5, L[i]))
    lv['эргэлтийн цэг'] = piv

    # 5. Дугуй тоо — $50-аар
    lv['дугуй тоо ($50)'] = [(i, round(C[i] / 50) * 50) for i in range(21, n)]

    # 6. Шахалтын эхлэл
    ins = sq < .85
    lv['шахалтын эхлэл'] = [(i, C[i]) for i in range(1, n)
                            if ins[i] and not ins[i - 1]]

    rng = np.random.default_rng(a.seed)

    print(f'{a.horizon} хоног хардаг   түвшнээс {AWAY:.1%} холдсоны '
          f'дараа тоолно\n')
    print(f'{"түвшин":24} {"n":>6} {"БУЦСАН":>8} {"ХАРИУ (ATR)":>12} '
          f'{"БАРЬСАН":>9}')
    print('─' * 64)
    for nm, items in lv.items():
        if len(items) > 3000:
            idx = rng.choice(len(items), 3000, replace=False)
            items = [items[k] for k in sorted(idx)]
        # ШУДАРГА ХЯНАЛТ: ижил өдөр, ижил зэрэгцээ зайд боловч
        # УТГАГҮЙ болгож 0.5-1.5%-иар зөөсөн «хуурамч» түвшин.
        # Санамсаргүй ӨДРИЙН ХААЛТ-ыг хяналт болгох нь ШУДАРГА БИШ:
        # хаалт нь тархалтын голд, дээд/доод/эргэлт нь ЗАХАД байдаг
        # тул захын түвшин рүү буцах нь угаасаа хэцүү. Тэр хазайлт
        # бүх түвшнийг «санамсаргүйгээс муу» мэт харуулж байв.
        off = rng.uniform(.005, .015, len(items)) * rng.choice([-1, 1], len(items))
        fake = [(i, lvl * (1 + o)) for (i, lvl), o in zip(items, off)]

        r = measure(d, items, a.horizon)
        f = measure(d, fake, a.horizon)
        rb, fb = r[r.back == 1], f[f.back == 1]
        print(f'{nm:24} {len(r):6} {r.back.mean():7.0%} '
              f'{rb.push.median():12.2f} {rb.held.mean():8.0%}')
        print(f'{"  └ хуурамч хяналт":24} {len(f):6} {f.back.mean():7.0%} '
              f'{fb.push.median():12.2f} {fb.held.mean():8.0%}'
              f'   зөрүү {r.back.mean() - f.back.mean():+.1%} / '
              f'{rb.push.median() - fb.push.median():+.2f} ATR')
    print('\n  Мөр бүрийн «зөрүү» тэгд ойр бол — тэр түвшин утгагүй.')
    print('  Хуурамч түвшин нь ИЖИЛ өдөр, ИЖИЛ зайд, зүгээр л 0.5-1.5%')
    print('  зөөгдсөн — өөрөөр хэлбэл «утга»-аас нь бусад бүхэн ижил.')


if __name__ == '__main__':
    main()
