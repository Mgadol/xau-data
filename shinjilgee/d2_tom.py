"""d2. Шахалтад ТОМ ТОГЛОГЧ орж байгааг мэдэж болох уу?

ХЯЗГААР — ЭХЛЭЭД ҮҮНИЙГ МЭД. Өгөгдлийн `Volume` нь ЖИНХЭНЭ арилжааны
хэмжээ БИШ. MetaTrader-ийн tick volume — үнэ хэдэн удаа шинэчлэгдсэн
тоо. Нэг сая унцийн арилжаа нэг tick, зуун унцийнх ч нэг tick.
Тиймээс «том тоглогч ОРЖ БАЙНА» гэдгийг ШУУД харах БОЛОМЖГҮЙ.

Харагдаж болох зүйл нь ИДЭВХ. Том оролцогч ажиллахад ихэвчлэн:
үнэ хөдлөхгүй атал tick олширдог (захиалга шингээгдэж байна),
эсвэл лаа тодорхой тал руугаа хаагддаг (шахаж байна).

Тиймээс шууд биш, ШИНЖЭЭР нь хайна:

  1. ИДЭВХ — шахалтын үеийн tick нь ердийнхөөсөө их үү
  2. ШИНГЭЭЛТ — идэвх/муж харьцаа. Өндөр = олон tick боловч үнэ
     хөдлөхгүй байна = хэн нэгэн эсрэг талыг нь шингээж байна
  3. ХААЛТЫН БАЙРЛАЛ — лаанууд тогтмол дээд/доод талдаа хаагдаж
     байна уу (accumulation / distribution)
  4. ИДЭВХ + ЧИГЛЭЛ — дээш өдрүүдийн tick доош өдрүүдийнхээс их үү

3, 4 нь ЧИГЛЭЛИЙН талаар мэдээлэл өгч магадгүй — энэ нь төслийн
хамгийн том нээлттэй асуудал.

ЗАНГА: tick volume жилээс жилд өсдөг (брокерын систем сайжирсан,
арилжаа идэвхжсэн). Тиймээс ТҮҮХИЙ tick-ийг харьцуулж болохгүй —
бүгдийг сүүлийн 100 өдрийн дунджид харьцуулна.

    python3 d2_tom.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    m20 = d.close.rolling(20).mean()
    d['up'] = m20 + 1.5 * d.atr14
    d['dn'] = m20 - 1.5 * d.atr14

    # ── Шинжүүд, бүгд ХАРЬЦАНГУЙ (100 өдрийн дунджид) ───────────────
    v = d.volume
    d['act'] = v / v.rolling(100).mean()                  # идэвх
    rng = (d.high - d.low).replace(0, np.nan)
    ar = (v / rng)
    d['absorb'] = ar / ar.rolling(100).mean()             # шингээлт
    # Хаалтын байрлал: 0 = доод, 1 = дээд
    pos = ((d.close - d.low) / rng).clip(0, 1)
    d['clpos'] = pos.rolling(5).mean()                    # 5 өдрийн дундаж
    # Идэвхийн чиглэл: дээш өдрийн tick − доош өдрийн tick (5 өдөр)
    sgn = np.sign(d.close.diff())
    d['vdir'] = ((sgn * v).rolling(5).sum() / v.rolling(5).sum())

    d = d.dropna(subset=['sq', 'up', 'atr14', 'act', 'absorb',
                         'clpos', 'vdir'])
    q20 = d.sq.quantile(.2)
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = d.atr14.to_numpy(), d.up.to_numpy(), d.dn.to_numpy()
    n = len(d)

    rows = []
    for i in np.where((d.sq <= q20).to_numpy())[0]:
        if not np.isfinite(A[i]) or A[i] <= 0:
            continue
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
        rows.append((d.act.iloc[i], d.absorb.iloc[i], d.clpos.iloc[i],
                     d.vdir.iloc[i], side,
                     side * (out - lvl) / risk - a.spread / risk))

    t = pd.DataFrame(rows, columns=['act', 'absorb', 'clpos', 'vdir',
                                    'side', 'R'])
    print(f'{len(t)} задрал   (Volume = tick тоо, ЖИНХЭНЭ хэмжээ БИШ)\n')

    # ── ЧИГЛЭЛ таах чадвар — хамгийн чухал асуулт ───────────────────
    print('  ЧИГЛЭЛИЙН мэдээлэл: задрал ДЭЭШ гарах магадлал')
    for col, nm in (('clpos', 'хаалтын байрлал'), ('vdir', 'идэвхийн чиглэл')):
        t['b'] = pd.qcut(t[col], 4, labels=False, duplicates='drop')
        line = []
        for b in sorted(t.b.dropna().unique()):
            g = t[t.b == b]
            line.append(f'{(g.side > 0).mean():.0%}')
        print(f'    {nm:18} доод→дээд дөрөвний нэг: ' + '  '.join(line))
    print('    (25%-аас 75% рүү өөрчлөгдвөл мэдээлэлтэй, бүгд ~65% бол үгүй)')

    # ── R-ийн мэдээлэл ──────────────────────────────────────────────
    print('\n  R-ийн мэдээлэл (ДЭЭШ задрал дотор):')
    up = t[t.side == 1]
    for col, nm in (('act', 'идэвх'), ('absorb', 'шингээлт'),
                    ('clpos', 'хаалтын байрлал'), ('vdir', 'идэвхийн чиглэл')):
        up = up.copy()
        up['b'] = pd.qcut(up[col], 3, labels=False, duplicates='drop')
        vals = []
        for b in sorted(up.b.dropna().unique()):
            g = up[up.b == b]
            vals.append(f'{g.R.mean():+.3f}({len(g)})')
        lo = up[up.b == 0].R.mean()
        hi = up[up.b == up.b.max()].R.mean()
        print(f'    {nm:18} бага→их: ' + '  '.join(vals) +
              f'   зөрүү {hi - lo:+.3f}')

    print('\n  Зөрүү бүгд ±0.15R дотор бол — tick volume-д мэдээлэл алга.')


if __name__ == '__main__':
    main()
