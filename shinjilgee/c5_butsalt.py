"""c5. Шахалт ЭХЭЛСЭН ЦЭГ рүү үнэ хэр их буцаж ирдэг вэ?

c2 нь шахалтын БҮС-ийг (10 хоногийн дээд/доод) шалгасан. Энд өөр
зүйл: шахалт эхэлсэн өдрийн ХААЛТЫН ҮНЭ — тэр ганц түвшин рүү үнэ
буцаж ирдэг үү, хэр олон удаа, хэр хурдан.

Ийм асуулт нь өөрийгөө хуурах хоёр аргатай:

  1. ОЙРХОН БАЙВАЛ ЗААВАЛ ХҮРНЭ. Ямар ч түвшин одоогийн үнэтэй
     ойрхон бол хүрэгдэнэ. Тиймээс түвшнийг зүгээр тоолж болохгүй —
     үнэ тэрнээс ХОЛДСОНЫ дараа л тоолж эхэлнэ (энд 1 ATR).

  2. ХЯНАЛТГҮЙ БОЛ УТГАГҮЙ. «70% нь буцаж ирдэг» гэсэн тоо дангаараа
     юу ч хэлэхгүй. Санамсаргүй өдрийн хаалтын үнэ мөн адил хүрэгдэнэ.
     Тиймээс ижил хэмжилтийг САНАМСАРГҮЙ өдрүүд дээр давтана.

Хэмжих зүйл:

    буцсан  — 1 ATR холдсоны дараа тэр түвшинд дахин хүрсэн эсэх
    хоног   — хүрэх хүртэл хэдэн хоног
    давтамж — хэдэн удаа хүрсэн (соронз уу, нэг удаагийн уу)

    python3 c5_butsalt.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def retest(d, days, horizon, away=1.0, mode='pct'):
    """Түвшнээс холдсоны ДАРАА дахин хүрэх эсэхийг хэмжинэ.

    `mode='atr'` нь ХАЗАЙЛТТАЙ: шахалтын эхлэлд ATR жижиг ($18.23 vs
    хяналтын $22.53) тул «1 ATR холдох» нь доллараар БОГИНО зай болж,
    буцаж ирэх нь амар болно. Энэ хазайлт дангаараа +5.9% хуурамч
    давуу тал үүсгэж байв.

    `mode='pct'` (анхдагч) нь үнийн ТОГТМОЛ хувиар хэмжинэ — хоёр
    бүлэгт ижил зай. Үүгээр хэмжихэд зөрүү -5.4% болж ЭРГЭДЭГ.
    """
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A = d.atr14.to_numpy()
    n = len(d)
    out = []
    for i in days:
        if not np.isfinite(A[i]) or A[i] <= 0:
            continue
        lvl = C[i]
        gap = away * A[i] if mode == 'atr' else away * .015 * C[i]
        # 1) Түвшнээс ХОЛДОХЫГ хүлээнэ
        j = i + 1
        while j < n and abs(C[j] - lvl) < gap:
            j += 1
        if j >= n or j - i > horizon:
            continue
        above = C[j] > lvl
        # 2) Буцаж хүрэх эсэх
        end = min(j + horizon, n)
        first, hits = None, 0
        touching = False
        for k in range(j, end):
            hit = (L[k] <= lvl) if above else (H[k] >= lvl)
            if hit and not touching:
                hits += 1
                if first is None:
                    first = k - j
            touching = hit
        out.append((int(first is not None), first if first is not None else np.nan,
                    hits, j - i))
    return pd.DataFrame(out, columns=['back', 'days', 'hits', 'leave'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--thresh', type=float, default=.85)
    ap.add_argument('--horizon', type=int, default=60)
    ap.add_argument('--away', type=float, default=1.0)
    ap.add_argument('--mode', default='pct', choices=('pct', 'atr'),
                    help='pct = тогтмол 1.5%% (шударга), atr = хазайлттай')
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
    starts = [i for i in range(1, n) if ins[i] and not ins[i - 1]]

    rng = np.random.default_rng(a.seed)
    pool = [i for i in range(1, n) if i not in set(starts)]
    ctrl = sorted(rng.choice(pool, size=min(len(pool), 1500), replace=False))

    unit = f'{a.away} ATR' if a.mode == 'atr' else f'{a.away * 1.5:.1f}%'
    print(f'Босго {a.thresh}   {unit} холдсоны дараа тоолно   '
          f'{a.horizon} хоног хардаг   (--mode {a.mode})\n')
    print(f'{"бүлэг":24} {"n":>6} {"БУЦСАН":>8} {"хоног":>8} '
          f'{"хүрэлт":>8} {"холдох":>8}')
    print(f'{"":24} {"":>6} {"":>8} {"медиан":>8} {"дундаж":>8} {"хоног":>8}')
    print('─' * 70)
    res = {}
    for nm, days in (('шахалт эхэлсэн цэг', starts),
                     ('хяналт (санамсаргүй)', ctrl)):
        r = retest(d, days, a.horizon, a.away, a.mode)
        res[nm] = r
        b = r[r.back == 1]
        print(f'{nm:24} {len(r):6} {r.back.mean():7.0%} '
              f'{b.days.median():8.0f} {b.hits.mean():8.2f} '
              f'{r.leave.median():8.0f}')

    s, c = res['шахалт эхэлсэн цэг'], res['хяналт (санамсаргүй)']
    print(f'\n  ЗӨРҮҮ: буцсан {s.back.mean() - c.back.mean():+.1%}')
    print('  Тэгд ойр бол — шахалтын эхлэлийн цэг онцгой БИШ.')

    print('\n  Хугацаагаар (буцсан хувь):')
    for hz in (10, 20, 40, 60, 120):
        rs = retest(d, starts, hz, a.away, a.mode)
        rc = retest(d, ctrl, hz, a.away, a.mode)
        print(f'    {hz:3} хоногт  шахалт {rs.back.mean():4.0%}   '
              f'хяналт {rc.back.mean():4.0%}   зөрүү '
              f'{rs.back.mean() - rc.back.mean():+.1%}')


if __name__ == '__main__':
    main()
