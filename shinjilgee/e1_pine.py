"""e1. TradingView-ийн Pine кодыг ЖИНХЭНЭ өгөгдөл дээр шалгана.

`tradingview/shahalt.pine` доторх төлөвт машиныг Python дээр ЯГ адилаар
давтаж, судалгааны тоо гарч байгаа эсэхийг хэмжинэ. Зорилго нь «код
сайхан харагдаж байна» гэдгийг биш, «код нь судалгаагаа үнэн
хэрэгжүүлсэн үү» гэдгийг шалгах.

Pine ба судалгааны хооронд ЗОРИУДААР гурван ялгаа бий — тэдгээрийн
нөлөөг тусад нь хэмжинэ:

  1. Босго. Судалгаа нь `nanquantile(sq, .2)` — БҮХ өгөгдлийг
     хараад тооцсон (арилжаанд боломжгүй, харагдах ирээдүй).
     Pine нь тогтмол 0.80. Хоёр нь ижил багц сонгож байна уу.

  2. Нэр дэвшигч. Судалгаа нь шахагдсан бар БҮРИЙГ тусдаа нэр
     дэвшигч болгодог тул нэг задрал олон удаа тоологдож болно.
     Pine нь нэг зэвсэглэлд НЭГ дохио өгнө.

  3. Цоорхой. Pine нь нээлтээр хилээс хэтэрсэн барт ОРДОГГҮЙ
     (c8-ийн сургамж). d3/d5-ийн `collect` үүнийг шалгадаггүй.

    python3 e1_pine.py                 # өдрийн график
    python3 e1_pine.py --tf 4h         # 4 цаг (хэмнэл цэвэрлэхгүй)
    python3 e1_pine.py --tf 4h --norm  # 4 цаг, цагийн хэмнэл цэвэрлэсэн
"""
import argparse
import numpy as np
import pandas as pd
from core import load
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def prep_daily():
    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['tr'] = tr
    d['atr'] = tr.rolling(14).mean()
    d['sq'] = d.atr / tr.rolling(100).mean()
    m = d.close.rolling(20).mean()
    d['up'], d['dn'] = m + 1.5 * d.atr, m - 1.5 * d.atr
    return d.dropna(subset=['sq', 'up', 'atr'])


def prep_tf(tf, norm=False, slow=100):
    """Доод давхрага. `norm` нь цагийн хэмнэлийг цэвэрлэнэ — c3-д
    үүнгүйгээр «шахалт» нь зүгээр л «аль сесс вэ» гэдгийг олдог
    байсан. Pine нь цэвэрлэдэггүй тул зөрүүг нь ХЭМЖИХ хэрэгтэй."""
    h = load('XAU_5m_data.csv')
    d = h.resample(tf).agg(open=('open', 'first'), high=('high', 'max'),
                           low=('low', 'min'), close=('close', 'last'),
                           volume=('volume', 'sum')).dropna()
    d = d[d.index >= '2010-01-01'].copy()
    pc = d.close.shift(1)
    tr = pd.concat([d.high - d.low, (d.high - pc).abs(),
                    (d.low - pc).abs()], axis=1).max(axis=1)
    d['tr'], d['atr'] = tr, tr.rolling(14).mean()
    if norm:
        key = d.index.hour * 60 + d.index.minute
        base = pd.Series(np.nan, index=d.index)
        for k, g in d.groupby(key):
            base.loc[g.index] = (g.tr / g.tr.rolling(60, min_periods=20)
                                 .mean().shift(1)).to_numpy()
        d['sq'] = base.rolling(14).mean() / base.rolling(slow).mean()
    else:
        d['sq'] = d.atr / tr.rolling(slow).mean()
    m = d.close.rolling(20).mean()
    d['up'], d['dn'] = m + 1.5 * d.atr, m - 1.5 * d.atr
    return d.dropna(subset=['sq', 'up', 'atr'])


def pine(d, thr, pos_min=.50, use_leg=True, zz=3.0, stop_atr=2.0,
         targ_atr=4.0, max_bars=5, hold=15, spread=.25, gap='open',
         one_shot=True):
    """gap: нээлтээр хилээс хэтэрсэн барыг яах вэ.

      'skip'   — алгасна (хэт хатуу: ихэнх тохиргоог хаядаг)
      'open'   — НЭЭЛТИЙН үнээр орно, стоп/зорилт нь тэрнээс (үнэн)
      'ignore' — хил дээр оролоо гэж тооцно (d3/d5-ийн байдал, ӨӨДРӨГ)
    """
    """Pine дэх төлөвт машиныг бар бүрээр ЯГ адилаар давтана.

    Дараалал нь Pine-ийнхтэй ижил байх ЁСТОЙ: эхлээд дохио (анкр нь
    өмнөх барын утгыг барина), дараа нь арилжаа, дараа нь хөл, хамгийн
    сүүлд анкр. Эс бөгөөс бар өөрийн хилээр өөрийгөө баталгаажуулж,
    байхгүй ирмэг гарч ирнэ.
    """
    O, H, L, C = (d.open.to_numpy(), d.high.to_numpy(),
                  d.low.to_numpy(), d.close.to_numpy())
    A, U, DN, SQ = (d.atr.to_numpy(), d.up.to_numpy(),
                    d.dn.to_numpy(), d.sq.to_numpy())
    n = len(d)

    leg, ext = 1, C[0]
    a_up = a_dn = a_atr = a_pos = np.nan
    a_bar, a_live, a_fired = -10**9, False, False
    t_entry = t_stop = t_t = np.nan
    t_bar, t_open = 0, False
    trades, misses, gaps = [], 0, 0

    for i in range(n):
        sq_on = np.isfinite(SQ[i]) and SQ[i] <= thr

        # ── дохио (анкр = ӨМНӨХ барын утга) ───────────────────────
        waited = i - a_bar
        fresh = a_live and not a_fired and 1 <= waited <= max_bars
        leg_ok = (not use_leg) or leg == 1
        pos_ok = np.isfinite(a_pos) and a_pos >= pos_min

        gap_up = np.isfinite(a_up) and O[i] >= a_up
        hit_up = fresh and np.isfinite(a_up) and H[i] >= a_up
        brk_up = hit_up and not (gap == 'skip' and gap_up)
        gap_dn = np.isfinite(a_dn) and O[i] <= a_dn
        brk_dn = fresh and np.isfinite(a_dn) and L[i] <= a_dn and \
            not (gap == 'skip' and gap_dn)

        if hit_up and gap_up:
            gaps += 1
        long_sig = brk_up and pos_ok and leg_ok and not t_open
        if brk_up and not (pos_ok and leg_ok):
            misses += 1
        if one_shot and (brk_up or brk_dn):
            a_fired = True

        # ── арилжаа ───────────────────────────────────────────────
        if long_sig:
            # Нээлт хилээс дээш байвал хил дээр орох БОЛОМЖГҮЙ —
            # жинхэнэ оролт нь нээлтийн үнэ (c8-ийн сургамж).
            t_entry = O[i] if (gap == 'open' and gap_up) else a_up
            t_stop = t_entry - stop_atr * a_atr
            t_t = t_entry + targ_atr * a_atr
            t_bar, t_open = i, True
            trades.append({'i': i, 'date': d.index[i], 'entry': t_entry,
                           'atr': a_atr, 'pos': a_pos, 'exit': np.nan,
                           'why': ''})
        if t_open:
            risk = stop_atr * trades[-1]['atr']
            if L[i] <= t_stop:                    # стоп ТҮРҮҮЛЖ
                t_open = False
                trades[-1].update(exit=t_stop, why='стоп')
            elif H[i] >= t_t:
                t_open = False
                trades[-1].update(exit=t_t, why='зорилт')
            elif i - t_bar >= hold:
                t_open = False
                trades[-1].update(exit=C[i], why='хугацаа')
            _ = risk

        # ── хөл (дохионы ДАРАА) ───────────────────────────────────
        if leg == 1:
            ext = max(ext, H[i])
            if L[i] <= ext * (1 - zz / 100):
                leg, ext = -1, L[i]
        else:
            ext = min(ext, L[i])
            if H[i] >= ext * (1 + zz / 100):
                leg, ext = 1, H[i]

        # ── анкр ──────────────────────────────────────────────────
        if sq_on:
            a_up, a_dn, a_atr = U[i], DN[i], A[i]
            a_pos = (C[i] - DN[i]) / (U[i] - DN[i]) \
                if U[i] > DN[i] else np.nan
            a_bar, a_live, a_fired = i, True, False
        elif a_live and waited > max_bars:
            a_live = False

    if t_open and trades:
        trades[-1].update(exit=C[-1], why='дуусаагүй')
    t = pd.DataFrame(trades)
    if len(t):
        risk = stop_atr * t.atr
        t['R'] = (t.exit - t.entry) / risk - spread / risk
    return t, misses, gaps


def report(t, label):
    if not len(t):
        print(f'  {label:34} арилжаа алга')
        return
    print(f'  {label:34} n={len(t):4}  {t.R.mean():+.3f}R  '
          f'ялсан {(t.R > 0).mean():.0%}  медиан {t.R.median():+.3f}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tf', default='day')
    ap.add_argument('--norm', action='store_true')
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    if a.tf == 'day':
        d = prep_daily()
        tfname = 'ӨДӨР'
    else:
        d = prep_tf(a.tf, norm=a.norm)
        tfname = a.tf.upper() + (' (хэмнэл цэвэрлэсэн)' if a.norm
                                 else ' (Pine шиг ТҮҮХИЙ)')
    q20 = float(np.nanquantile(d.sq, .2))
    print(f'\n{"=" * 68}\n{tfname}   {len(d):,} бар   '
          f'{d.index[0].date()} … {d.index[-1].date()}\n{"=" * 68}')
    print(f'  Судалгааны босго (20 хувь) = {q20:.3f}')
    print(f'  Pine-ийн тогтмол босго     = 0.800')
    print(f'  0.80-аас доош бар: {(d.sq <= .80).mean():.1%}   '
          f'q20-оос доош: {(d.sq <= q20).mean():.1%}')

    print('\n── Pine-ийн ЯГ тэр логик, босго 0.80 ──')
    for pm, nm in ((0.0, 'байрлалын шүүлтгүй'),
                   (.50, 'байрлал ≥ 0.50 (Pine-ийн анхдагч)'),
                   (.67, 'байрлал ≥ 0.67 (дээд гуравны нэг)')):
        t, ms, gp = pine(d, .80, pos_min=pm, spread=a.spread)
        report(t, nm)

    print('\n── Тогтмол 0.80 vs судалгааны q20 (байрлал ≥ 0.50) ──')
    for thr, nm in ((.80, 'тогтмол 0.80'), (q20, f'q20 = {q20:.3f}')):
        t, _, _ = pine(d, thr, pos_min=.50, spread=a.spread)
        report(t, nm)

    print('\n── Тус бүрийн шүүлтүүрийн нөлөө (байрлал ≥ 0.50) ──')
    base, ms, gp = pine(d, .80, pos_min=.50, spread=a.spread)
    report(base, 'бүгд асаалттай')
    t, _, _ = pine(d, .80, pos_min=.50, use_leg=False, spread=a.spread)
    report(t, 'хөлийн шүүлтүүр УНТРААСАН')
    for gm, nm in (('skip', 'цоорхой: АЛГАСНА'),
                   ('open', 'цоорхой: НЭЭЛТЭЭР орно (үнэн)'),
                   ('ignore', 'цоорхой: хил дээр оролоо гэнэ (өөдрөг)')):
        t, _, _ = pine(d, .80, pos_min=.50, gap=gm, spread=a.spread)
        report(t, nm)
    t, _, _ = pine(d, .80, pos_min=.50, one_shot=False, spread=a.spread)
    report(t, 'нэг зэвсэглэл-нэг дохио УНТРААСАН')
    print(f'\n  шүүлтүүрт таслагдсан задрал: {ms}   '
          f'цоорхойгоор алгассан: {gp}')

    print('\n── Зорилтын нөлөө (байрлал ≥ 0.50) ──')
    for ta_ in (1.0, 2.0, 3.0, 3.8, 4.0, 6.0):
        t, _, _ = pine(d, .80, pos_min=.50, targ_atr=ta_, spread=a.spread)
        if len(t):
            res = t[t.why.isin(['стоп', 'зорилт'])]
            print(f'  зорилт {ta_:.1f} ATR = {ta_ / 2:.1f}R   '
                  f'{t.R.mean():+.3f}R   шийдэгдсэн {len(res) / len(t):.0%} '
                  f'({res.R.mean():+.3f}R)')

    print('\n── Спредэд тэсвэртэй юу (байрлал ≥ 0.50) ──')
    for sp in (0.0, .25, .50, 1.0):
        t, _, _ = pine(d, .80, pos_min=.50, spread=sp)
        print(f'  спред ${sp:.2f}   {t.R.mean():+.3f}R')

    print('\n── Жилээр (байрлал ≥ 0.50) ──')
    base['y'] = pd.to_datetime(base.date).dt.year
    g = base.groupby('y').R.agg(['mean', 'count'])
    pos_y = (g['mean'] > 0).sum()
    print(f'  эерэг жил: {pos_y}/{len(g)}')
    for y, r in g.iterrows():
        bar = '█' * max(0, int(r['mean'] * 10))
        print(f'   {y}  n={int(r["count"]):3}  {r["mean"]:+.3f}  {bar}')

    print('\n── Гарцын шалтгаан ──')
    for w, c in base.why.value_counts().items():
        sub = base[base.why == w]
        print(f'  {w:10} {c:4} ({c / len(base):4.0%})  {sub.R.mean():+.3f}R')


if __name__ == '__main__':
    main()
