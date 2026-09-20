"""c2. ХУУЧИН шахалтын бүс — үнэ буцаж ирэхэд хариу үйлдэл үзүүлдэг үү?

Асуулт: шахалт үүссэн үнийн бүс (тэр үеийн 10 хоногийн дээд/доод)
дараа нь түшлэг эсвэл эсэргүүцэл болдог уу? Үнэ тийш буцаж ирэхэд
мэдрэг хариу үйлдэл өгдөг үү?

Энэ бол «хуучин нягтралын бүс ажилладаг» гэсэн итгэл үнэмшлийн нэг
хэлбэр. a8 (трендлайн), a9 (order block) хоёрт ажиллаагүй — тэдгээр
нь өөр тодорхойлолттой ч гэсэн болгоомжлох шалтгаан бий.

ХЯНАЛТЫН БҮЛЭГГҮЙГЭЭР ЭНЭ ТЕСТ УТГАГҮЙ. «Үнэ бүсэд хүрээд 60%-д нь
эргэсэн» гэсэн тоо дангаараа юу ч хэлэхгүй: үнэ хаана ч байсан
эргэж болно. Тиймээс ЯГ ИЖИЛ хэмжилтийг ХУУРАМЧ бүсүүд дээр хийнэ —
шахалттай огт холбоогүй, санамсаргүй сонгосон өдрүүдийн мужууд.
Зөрүү нь л мэдээлэл.

Хэмжих зүйл: бүсэд анх хүрсний дараах 5 хоногт —

    ЭРГЭСЭН — бүснээс холдож, ирсэн зүгтээ буцсан
    ДАМЖСАН — бүсийг нэвт гарсан

Мөн бүсээс хэр хол түлхэгдсэнийг ATR-ийн дахинаар хэмжинэ.

    python3 c2_huuchin.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

RNG = 10
COOL = 20        # бүс үүссэнээс хойш хэдэн хоногийн дараа тоолж эхлэх


def zones_from(d, days):
    """Өгөгдсөн өдрүүдэд тогтсон бүсүүд: (индекс, доод, дээд)."""
    up = d.high.rolling(RNG).max().to_numpy()
    dn = d.low.rolling(RNG).min().to_numpy()
    return [(i, dn[i], up[i]) for i in days
            if np.isfinite(up[i]) and np.isfinite(dn[i])]


def test_zones(d, zones, horizon=5, max_age=250):
    """Бүс бүрд АНХ хүрэх мөчийг олж, дараагийн хариу үйлдлийг хэмжинэ."""
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A = d.atr14.to_numpy()
    n = len(d)
    out = []
    for i, lo, hi in zones:
        # Бүснээс ГАДНА гарахыг хүлээнэ, тэгэхгүй бол «хүрэв» нь утгагүй
        j = i + COOL
        while j < n and lo <= C[j] <= hi:
            j += 1
        if j >= n:
            continue
        above = C[j] > hi
        end = min(j + max_age, n)
        hit = None
        for k in range(j, end):
            if (L[k] <= hi) if above else (H[k] >= lo):
                hit = k
                break
        if hit is None or hit + horizon >= n:
            continue
        # Хүрсний дараах 5 хоног: ирсэн зүг рүүгээ хэр түлхэгдэв
        seg_h = H[hit + 1:hit + 1 + horizon].max()
        seg_l = L[hit + 1:hit + 1 + horizon].min()
        ref = hi if above else lo
        push = (seg_h - ref) / A[hit] if above else (ref - seg_l) / A[hit]
        thru = (seg_l < lo) if above else (seg_h > hi)
        out.append((d.index[hit], push, int(not thru), (hit - i)))
    return pd.DataFrame(out, columns=['date', 'push', 'held', 'age'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--thresh', type=float, default=.85)
    ap.add_argument('--horizon', type=int, default=5)
    ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    d = d.dropna(subset=['sq', 'atr14'])
    sq = d.sq.to_numpy()
    n = len(d)

    ins = sq < a.thresh
    starts = [i for i in range(RNG, n) if ins[i] and not ins[i - 1]]
    sq_zones = zones_from(d, starts)

    # ── ХЯНАЛТ: шахалттай огт холбоогүй санамсаргүй өдрүүд ───────────
    rng = np.random.default_rng(a.seed)
    pool = [i for i in range(RNG, n) if sq[i] > 1.0]     # ТЭЛСЭН үеүүд
    ctrl_days = rng.choice(pool, size=min(len(pool), 600), replace=False)
    ct_zones = zones_from(d, sorted(ctrl_days))

    print(f'Босго {a.thresh}   хариу үйлдлийг {a.horizon} хоногоор хэмжинэ')
    print(f'Шахалтын бүс: {len(sq_zones)}   хяналтын бүс: {len(ct_zones)}\n')

    r_sq = test_zones(d, sq_zones, a.horizon)
    r_ct = test_zones(d, ct_zones, a.horizon)

    print(f'{"бүлэг":18} {"хүрсэн":>7} {"БАРЬСАН":>9} '
          f'{"түлхэлт медиан":>15} {"дундаж":>8} {"нас (хоног)":>12}')
    print('─' * 74)
    for nm, r in (('шахалтын бүс', r_sq), ('хяналт (тэлсэн)', r_ct)):
        if len(r) == 0:
            print(f'  {nm}: хүрэлт алга')
            continue
        print(f'{nm:18} {len(r):7} {r.held.mean():8.0%} '
              f'{r.push.median():15.2f} {r.push.mean():8.2f} '
              f'{r.age.median():12.0f}')

    if len(r_sq) and len(r_ct):
        print(f'\n  ЗӨРҮҮ:  барьсан {r_sq.held.mean() - r_ct.held.mean():+.1%}'
              f'   түлхэлт {r_sq.push.median() - r_ct.push.median():+.2f} ATR')
        print('  Энэ зөрүү тэгд ойр бол — хуучин шахалтын бүс онцгой БИШ.')

    # Насаар нь — шинэ бүс илүү мэдрэг үү
    if len(r_sq) > 60:
        r_sq['grp'] = pd.cut(r_sq.age, [0, 40, 100, 10000],
                             labels=['шинэ (<40х)', 'дунд (40-100х)', 'хуучин (100х+)'])
        print('\n  Бүсийн НАСААР (шахалтын бүс):')
        for g, x in r_sq.groupby('grp', observed=True):
            if len(x) < 15:
                continue
            print(f'    {str(g):16} n={len(x):4}  барьсан {x.held.mean():4.0%}  '
                  f'түлхэлт {x.push.median():.2f} ATR')


if __name__ == '__main__':
    main()
