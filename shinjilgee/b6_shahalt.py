"""b6. ШАХАЛТ — хэр шахагдсан бэ, дараа нь хэр явах вэ?

«Хэлбэлзэл шахагдвал дараа нь тэсэрдэг» гэдэг нь арилжааны хамгийн
түгээмэл итгэл үнэмшлийн нэг. Үүнийг хатуу шалгана.

САНАМСАРГҮЙ ХУУРАХ ЗАНГА: шахалттай үед дараагийн хөдөлгөөн нь
ҮНЭМЛЭХҮЙ хэмжээгээр БАГА байдаг — хэлбэлзэл бөөгнөрдөг тул. Тиймээс
«шахалтын дараа 1.2% явсан, тайван үед 1.8% явсан» гэсэн тоо нь
шахалт ажиллахгүй гэсэн үг БИШ. Зөв асуулт:

    Шахагдсан үеийн ATR-тайгаа ХАРЬЦУУЛАХАД дараагийн хөдөлгөөн нь
    хэвийн үеийнхээс том үсрэлт үү?

Тиймээс бүх зүйлийг тухайн мөчийн ATR-ийн ДАХИНААР хэмжинэ.

Шахалтыг хэмжих: ATR-14 / ATR-100. Энэ нь «сүүлийн үеийн хэлбэлзэл
урт хугацааныхаасаа хэдэн хувь вэ» гэсэн утгатай, хэмжээнээс хамаарахгүй
тул 2005 оны $450, 2026 оны $4800 хоёрт адил ажиллана.

Хэмжих зүйл: дараагийн N хоногт үнэ шахалтын цэгээс ХАМГИЙН ХОЛ хэр
явсан (MFE — дээш ба доош хамгийн их зөрүү). Чиглэл хамаарахгүй, учир
нь b3 чиглэл таамаглагдахгүйг харуулсан.

2004 оноос хойшхи БҮХ өгөгдөл дээр ажиллана — 5 500 өдөр. 2020+ гэж
хязгаарлавал дүгнэлт хийхэд дээж хүрэлцэхгүй.

    python3 b6_shahalt.py [--horizon 5]
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR


def true_range(d):
    pc = d.close.shift(1)
    return pd.concat([d.high - d.low, (d.high - pc).abs(),
                      (d.low - pc).abs()], axis=1).max(axis=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--horizon', type=int, default=5,
                    help='дараагийн хэдэн хоногийг харах')
    a = ap.parse_args()
    H = a.horizon

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['atr100'] = tr.rolling(100).mean()
    # АНХААР: баганыг `squeeze` гэж нэрлэж БОЛОХГҮЙ — pandas-ийн
    # DataFrame.squeeze() аргатай мөргөлдөж, d.squeeze нь багана
    # биш функц буцаадаг.
    d['sq'] = d.atr14 / d.atr100               # < 1 = шахагдсан

    # Дараагийн H хоногт хамгийн хол явсан зай (хоёр тал), % ба ATR-ээр
    hi = d.high.shift(-1).rolling(H, min_periods=H).max().shift(-(H - 1))
    lo = d.low.shift(-1).rolling(H, min_periods=H).min().shift(-(H - 1))
    d['up'] = (hi - d.close) / d.close * 100
    d['dn'] = (d.close - lo) / d.close * 100
    d['mfe'] = d[['up', 'dn']].max(axis=1)     # хамгийн хол — аль ч тийш
    d['atr_pct'] = d.atr14 / d.close * 100
    d['mfe_atr'] = d.mfe / d.atr_pct           # ← ГОЛ хэмжүүр

    d = d.dropna(subset=['sq', 'mfe_atr'])
    print(f'{len(d):,} өдөр   {d.index.min().date()} → {d.index.max().date()}'
          f'   давхрага {H} хоног\n')

    # ── Шахалтын зэргээр 5 бүлэг ─────────────────────────────────────
    d['bin'] = pd.qcut(d.sq, 5, labels=False)
    names = ['1 хамгийн шахагдсан', '2', '3 хэвийн', '4', '5 хамгийн тэлсэн']
    print(f'{"бүлэг":22} {"ATR14/ATR100":>13} {"явсан %":>9} '
          f'{"ATR-ийн дахин":>14} {"өдрийн тоо":>11}')
    print('─' * 74)
    rows = []
    for b in range(5):
        g = d[d.bin == b]
        rows.append((names[b], g.sq.mean(), g.mfe.mean(),
                     g.mfe_atr.mean(), len(g)))
        print(f'{names[b]:22} {g.sq.mean():13.2f} {g.mfe.mean():9.2f} '
              f'{g.mfe_atr.mean():14.2f} {len(g):11,}')

    lo_b, hi_b = rows[0], rows[-1]
    print(f'\n  ҮНЭМЛЭХҮЙ хэмжээгээр: шахагдсан {lo_b[2]:.2f}% vs '
          f'тэлсэн {hi_b[2]:.2f}%  → {lo_b[2] / hi_b[2]:.2f} дахин')
    print(f'  ATR-ийн ДАХИНААР    : шахагдсан {lo_b[3]:.2f} vs '
          f'тэлсэн {hi_b[3]:.2f}  → {lo_b[3] / hi_b[3]:.2f} дахин')

    # ── Шахалт гүнзгий байх тусам үсрэлт том уу ──────────────────────
    from b4_hemjee import spearman
    rho = spearman(-d.sq.to_numpy(float), d.mfe_atr.to_numpy(float))
    print(f'\n  «гүнзгий шахалт → том үсрэлт» зэрэглэл: {rho:+.3f}')
    print('  (эерэг = шахалт гүнзгий байх тусам ATR-ийн дахин их)')

    # ── Хамгийн шахагдсан 10% дээр тусад нь ──────────────────────────
    q10 = d.sq.quantile(.10)
    tight = d[d.sq <= q10]
    rest = d[d.sq > q10]
    print(f'\n  Хамгийн шахагдсан 10% (n={len(tight):,}):')
    print(f'    ATR-ийн дахин  {tight.mfe_atr.mean():.2f}   '
          f'бусад нь {rest.mfe_atr.mean():.2f}')
    print(f'    медиан         {tight.mfe_atr.median():.2f}   '
          f'бусад нь {rest.mfe_atr.median():.2f}')
    print(f'    3 ATR-ээс давсан нь  {(tight.mfe_atr > 3).mean():.1%}   '
          f'бусад нь {(rest.mfe_atr > 3).mean():.1%}')

    # ── Жилээр тогтвортой юу ─────────────────────────────────────────
    print('\n  Жилээр (хамгийн шахагдсан 20% ÷ хамгийн тэлсэн 20%):')
    out = []
    for y in sorted(d.index.year.unique()):
        g = d[d.index.year == y]
        if len(g) < 100:
            continue
        a1 = g[g.sq <= g.sq.quantile(.2)].mfe_atr.mean()
        a2 = g[g.sq >= g.sq.quantile(.8)].mfe_atr.mean()
        out.append(f'{y}:{a1 / a2:.2f}')
    print('    ' + '  '.join(out))
    print('\n  1.00-аас дээш = шахалт ажиллаж байна. Жил бүр тогтвортой')
    print('  давсан эсэхийг хараарай — нэг хоёр жилд гарсан нь санамсаргүй.')


if __name__ == '__main__':
    main()
