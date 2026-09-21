"""f1. Sweep → Displacement → BOS → Retest — зассан хувилбар.

Эх код (ICT маягийн загвар) нь бүтцийн хувьд зөв байсан ч гурван зүйл
үр дүнг нь бүхэлд нь хүчингүй болгож байв. Бүгдийг жинхэнэ өгөгдөл
дээр баталсан:

  1. КОД УНАНА. `df["H1_Momentum"] = ...reindex(...)` нь DatetimeIndex
     бүхий Series-ийг RangeIndex-тэй df-д оноодог тул бүхэлдээ NaN.
     Дараа нь merge_asof ижил нэртэй багана нэмэхэд pandas `_x`/`_y`
     дагавар өгч, `row["H1_Momentum"]` нь KeyError болно.

  2. ИРЭЭДҮЙ ХАРНА. merge_asof(direction="backward") нь 10:00 гэж
     тэмдэглэгдсэн 1 цагийн барыг 10:05-ын 5м барт хавсаргадаг — гэтэл
     тэр барын Close нь 10:55-д болно. Хэмжихэд эхний 200 цагийн 1897
     мөрийн 1897 нь (100%) дуусаагүй цагийн хаалтыг хэрэглэж байв.
     h1_momentum бол гол шүүлтүүр тул түүгээр гарах бүх дүн хуурамч.
     → Засвар: resample хийсэн шинжийг merge-ээс ӨМНӨ `.shift(1)`.

  3. ТОГТМОЛ ДОЛЛАРЫН ЗОРИЛТ утгаа алдана. $7 нь 2004-д 19.6 ATR,
     2026-д 1.2 ATR — 16 дахин зөрүү. TRAIN дунджаар 10.2 ATR, UNSEEN
     5.4 ATR. Хоёр багц огт өөр тест хийж байгаа тул дүрмээ хөлдөөсөн
     ч харьцуулах боломжгүй.
     → Засвар: зорилт/стоп нь оролтын ATR-ийн дахин.

Мөн засагдсан бүтцийн дутагдлууд:

  · ХЯНАЛТЫН БҮЛЭГ нэмэв. Эх кодод `momentum >= 0.0` ба
    `retest >= 0.0` хоёул ШҮҮДЭГ (`NaN >= 0.0` нь False тул сүүлийнх нь
    давталтгүй бүх эвентийг хаядаг). Сүлжээнд «шүүлтгүй» мөр байгаагүй
    тул загвар өөрөө ажилладаг эсэхийг мэдэх аргагүй байв. Энд `None`
    нь ҮНЭХЭЭР шүүлтгүй, мөн САНАМСАРГҮЙ оролттой суурь бий.
  · ХИЛИЙН НЭВЧИЛТ. Үр дүнгийн цонх нь хуваалтын шугамыг давсан
    эвентүүдийг хасав.
  · AMBIGUOUS-ийг хоёр аргаар: хуваариас хасах ба алдагдал гэж тооцох.
  · СПРЕД. Хариу нь ±1R тул зардал нь spread/(k·ATR) R.
  · ХОЁР ТАЛЫН sweep нэг барт таарвал алгасна (эх код чимээгүй дээшийг
    сонгодог байв).
  · ХУРД. `.iloc` мөр бүрээр биш, numpy массив.

    python3 f1_sweep.py
    python3 f1_sweep.py --k 1.5 --spread 0.25
"""
import argparse
import os
import numpy as np
import pandas as pd

# Өгөгдөл нь төслийн үндэст, скрипт нь shinjilgee/ дотор — хаанаас
# дуудсанаас үл хамааран олдох ёстой.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(_ROOT, 'XAU_5m_data.csv')
ATR_P = 14
SWEEP_LOOKBACK = 12
MAX_DISP_BARS = 3
MAX_BOS_BARS = 6
MAX_RETEST_BARS = 8
DISP_ATR = 2.0
HORIZON = 72          # 72 × 5м = 6 цаг
COOLDOWN = 12
TRAIN_RATIO = 0.70


def atr_of(h, l, c, p=ATR_P):
    pc = np.roll(c, 1)
    pc[0] = np.nan
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    return pd.Series(tr).rolling(p).mean().to_numpy()


def load():
    df = pd.read_csv(CSV, sep=';')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d %H:%M')
    for c in ('Open', 'High', 'Low', 'Close', 'Volume'):
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
    return df.sort_values('Date').reset_index(drop=True)


def htf_feature(df, rule, span=6):
    """Дээд давхрагын momentum — ИРЭЭДҮЙГҮЙ.

    resample хийсэн бар нь өөрийн ЭХЛЭХ цагаар тэмдэглэгддэг ч зөвхөн
    ДУУСАХ үедээ мэдэгдэнэ. `.shift(1)` тавихад 10:00 гэсэн мөр нь
    09:00 барын утгыг барих бөгөөд тэр нь 10:00-д бүрэн болсон байна.
    Ингэснээр 10:05-ын 5м бар зөвхөн өнгөрсөнийг хардаг.
    """
    g = (df.set_index('Date').resample(rule)
         .agg({'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna())
    a = atr_of(g.High.to_numpy(), g.Low.to_numpy(), g.Close.to_numpy())
    mom = (g.Close - g.Close.shift(span)).to_numpy() / a
    out = pd.DataFrame({'Date': g.index, 'mom': mom})
    out['mom'] = out['mom'].shift(1)          # ← ГОЛ ЗАСВАР
    return out


def build():
    df = load()
    H, L, C = (df.High.to_numpy(), df.Low.to_numpy(), df.Close.to_numpy())
    df['ATR'] = atr_of(H, L, C)
    df['PriorHigh'] = df.High.shift(1).rolling(SWEEP_LOOKBACK).max()
    df['PriorLow'] = df.Low.shift(1).rolling(SWEEP_LOOKBACK).min()
    for rule, nm in (('1h', 'h1'), ('15min', 'm15')):
        f = htf_feature(df, rule).rename(columns={'mom': nm})
        df = pd.merge_asof(df, f, on='Date', direction='backward')
    return df.reset_index(drop=True)


def detect(df):
    """Эвентүүдийг олно. Sweep-ийг вектороор шүүж, зөвхөн тэдэн дээр
    давтана — 1.44 сая мөр дээр `.iloc` давтахаас олон зуу дахин хурдан."""
    n = len(df)
    O, H, L, C = (df.Open.to_numpy(), df.High.to_numpy(),
                  df.Low.to_numpy(), df.Close.to_numpy())
    A = df.ATR.to_numpy()
    PH, PL = df.PriorHigh.to_numpy(), df.PriorLow.to_numpy()
    h1, m15 = df.h1.to_numpy(), df.m15.to_numpy()

    up = (L < PL) & (C > PL)
    dn = (H > PH) & (C < PH)
    both = up & dn                     # хоёр тал зэрэг — алгасна
    ok = np.isfinite(A) & (A > 0) & np.isfinite(PH) & np.isfinite(PL)
    cand = np.where((up | dn) & ~both & ok)[0]
    lo = SWEEP_LOOKBACK + ATR_P
    hi = n - MAX_BOS_BARS - MAX_RETEST_BARS - HORIZON
    cand = cand[(cand >= lo) & (cand < hi)]

    rows = []
    for i in cand:
        d = 1 if up[i] else -1
        lvl = PL[i] if d == 1 else PH[i]

        # ── Displacement ──────────────────────────────────────────
        di = dsz = None
        for j in range(i + 1, min(i + 1 + MAX_DISP_BARS, n)):
            if not np.isfinite(A[j]) or A[j] <= 0:
                continue
            body = abs(C[j] - O[j])
            fwd = (C[j] > O[j]) if d == 1 else (C[j] < O[j])
            if fwd and body / A[j] >= DISP_ATR:
                di, dsz = j, body / A[j]
                break
        if di is None:
            continue

        # ── BOS ───────────────────────────────────────────────────
        bi = None
        for j in range(di, min(di + MAX_BOS_BARS, n)):
            if (d == 1 and C[j] > lvl) or (d == -1 and C[j] < lvl):
                bi = j
                break
        if bi is None:
            continue

        # ── Retest ────────────────────────────────────────────────
        ri, rd = None, np.nan
        for j in range(bi + 1, min(bi + 1 + MAX_RETEST_BARS, n)):
            if not np.isfinite(A[j]) or A[j] <= 0:
                continue
            if d == 1 and L[j] <= lvl and C[j] >= lvl:
                ri, rd = j, abs(lvl - L[j]) / A[j]
                break
            if d == -1 and H[j] >= lvl and C[j] <= lvl:
                ri, rd = j, abs(H[j] - lvl) / A[j]
                break

        ai = ri if ri is not None else di
        rows.append((i, di, bi, -1 if ri is None else ri, ai, d, lvl,
                     abs((L[i] if d == 1 else H[i]) - lvl) / A[i],
                     dsz, rd, h1[i], m15[i]))

    e = pd.DataFrame(rows, columns=[
        'sweep_i', 'disp_i', 'bos_i', 'retest_i', 'anchor_i', 'dir', 'lvl',
        'sweep_atr', 'disp_atr', 'retest_atr', 'h1', 'm15'])
    e['date'] = df.Date.to_numpy()[e.sweep_i.to_numpy()]
    e['has_retest'] = e.retest_i >= 0
    return e


def dedup(e, cd=COOLDOWN):
    e = e.sort_values('anchor_i').reset_index(drop=True)
    keep, last = [], -10 ** 9
    for idx, a in enumerate(e.anchor_i.to_numpy()):
        if a - last >= cd:
            keep.append(idx)
            last = a
    return e.iloc[keep].reset_index(drop=True)


def outcomes(df, e, k):
    """Тэгш хаалт: оролтоос ±k·ATR. Аль нь ТҮРҮҮЛЖ хүрэв.

    Нэг барт хоёулаа хүрвэл AMBIGUOUS — барын дотор аль нь эхэлснийг
    мэдэх аргагүй. Далдлахгүй, тусад нь тоолно.
    """
    H, L, C = df.High.to_numpy(), df.Low.to_numpy(), df.Close.to_numpy()
    A = df.ATR.to_numpy()
    n = len(df)
    out, dist = [], []
    for ai, d in zip(e.anchor_i.to_numpy(), e.dir.to_numpy()):
        ent, a = C[ai], A[ai]
        if not np.isfinite(a) or a <= 0:
            out.append('NONE')
            dist.append(np.nan)
            continue
        step = k * a
        tgt = ent + d * step
        stp = ent - d * step
        end = min(ai + HORIZON, n - 1)
        res = 'NONE'
        for j in range(ai + 1, end + 1):
            ht = (H[j] >= tgt) if d == 1 else (L[j] <= tgt)
            hs = (L[j] <= stp) if d == 1 else (H[j] >= stp)
            if ht and hs:
                res = 'AMBIG'
                break
            if ht:
                res = 'TARGET'
                break
            if hs:
                res = 'STOP'
                break
        out.append(res)
        dist.append(step)
    return np.array(out), np.array(dist)


def baseline(df, k, n_draw=20000, seed=0):
    """САНАМСАРГҮЙ оролтын суурь. Ижил хаалт, ижил хугацаа.

    Тэгш хаалт дээр «тэг» нь 50% БИШ — алт өсдөг тул урт тал давуу.
    Загвар ажиллаж байгаа эсэхийг ЭНЭ тооноос дээш гарсан эсэхээр
    шүүнэ, 50%-иас биш.
    """
    rng = np.random.default_rng(seed)
    lo = SWEEP_LOOKBACK + ATR_P
    hi = len(df) - HORIZON - 1
    idx = rng.integers(lo, hi, n_draw)
    res = {}
    for d in (1, -1):
        fake = pd.DataFrame({'anchor_i': idx, 'dir': d})
        o, _ = outcomes(df, fake, k)
        r = (o == 'TARGET').sum()
        s = (o == 'STOP').sum()
        res[d] = (r / (r + s) * 100) if r + s else np.nan
    return res


def rate(o, ambig_as_loss=False):
    t = (o == 'TARGET').sum()
    s = (o == 'STOP').sum()
    a = (o == 'AMBIG').sum()
    if ambig_as_loss:
        s += a
        a = 0
    n = t + s
    return (t / n * 100 if n else np.nan), t, s, a, (o == 'NONE').sum()


def pick(e, mom=None, ret=None, need_retest=False):
    x = e
    if mom is not None:
        x = x[(x.h1 * x.dir) >= mom]
    if need_retest:
        x = x[x.has_retest]
    if ret is not None:
        x = x[x.retest_atr >= ret]      # NaN нь автоматаар хасагдана
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--k', type=float, default=1.5,
                    help='зорилт ба стоп нь ATR-ийн хэдэн дахин')
    ap.add_argument('--spread', type=float, default=0.25)
    a = ap.parse_args()

    print('Өгөгдөл уншиж байна…')
    df = build()
    print(f'  {len(df):,} бар   {df.Date.iloc[0].date()} … '
          f'{df.Date.iloc[-1].date()}')

    e = dedup(detect(df))
    print(f'  {len(e):,} эвент (давхардал арилгасан)')
    print(f'  давталттай: {e.has_retest.mean():.0%}   '
          f'дээш: {(e.dir == 1).mean():.0%}')

    o, step = outcomes(df, e, a.k)
    e = e.copy()
    e['out'] = o
    e['step'] = step

    # Хуваалт — үр дүнгийн цонх шугамыг давсан эвентийг ХАСНА
    split = int(len(df) * TRAIN_RATIO)
    e['ds'] = np.where(e.anchor_i + HORIZON < split, 'TRAIN',
                       np.where(e.anchor_i >= split, 'UNSEEN', 'BOUNDARY'))
    nb = (e.ds == 'BOUNDARY').sum()
    print(f'  хуваалтын шугам дээрх {nb} эвентийг хасав')
    print(f'  TRAIN {(e.ds == "TRAIN").sum():,}   '
          f'UNSEEN {(e.ds == "UNSEEN").sum():,}')

    print(f'\nЗорилт = стоп = {a.k} ATR   спред ${a.spread:.2f}')
    print('Хариу нь ±1R тул зардал = спред ÷ (k·ATR)')

    # ── СУУРЬ ────────────────────────────────────────────────────
    print(f'\n{"=" * 66}\nСУУРЬ — САНАМСАРГҮЙ оролт, ижил хаалт\n{"=" * 66}')
    bl = baseline(df, a.k)
    print(f'  урт   {bl[1]:.1f}%   богино {bl[-1]:.1f}%')
    print('  (тэгш хаалт дээр «тэг» нь 50% БИШ — алтны дрифт нөлөөлнө)')

    # ── ШҮҮЛТГҮЙ ЗАГВАР ──────────────────────────────────────────
    print(f'\n{"=" * 66}\nЗАГВАР ӨӨРӨӨ — ямар ч шүүлтгүй\n{"=" * 66}')
    print(f'  {"багц":10}{"n":>7}{"зорилт%":>10}{"суурь":>9}'
          f'{"зөрүү":>9}{"AMBIG":>8}{"дуусаагүй":>11}')
    for nm in ('TRAIN', 'UNSEEN'):
        for d, dn in ((1, 'дээш'), (-1, 'доош')):
            x = e[(e.ds == nm) & (e.dir == d)]
            p, t, s, am, nn = rate(x.out.to_numpy())
            base = bl[d]
            print(f'  {nm[:5]} {dn:5}{len(x):7}{p:9.1f}%{base:8.1f}%'
                  f'{p - base:+9.1f}{am:8}{nn:11}')

    # ── ДАВТАЛТ ──────────────────────────────────────────────────
    # Эх кодын гол санаа нь давталт (retest) хүлээх байв. Тэр нь яг
    # ирмэгийг устгадаг хэсэг болж таарав — c7-ийн «баталгааны буфер
    # хортой» дүгнэлттэй нэг чиглэлд.
    from math import erfc as _erfc, sqrt as _sqrt

    def _pv(t, n, q=0.5):
        z = (t / n - q) / _sqrt(q * (1 - q) / n)
        return _erfc(abs(z) / _sqrt(2))

    print(f'\n{"=" * 66}\nДАВТАЛТ ХҮЛЭЭХ НЬ ЮУ ХИЙДЭГ ВЭ\n{"=" * 66}')
    print(f'  {"багц":8}{"давталт":12}{"n":>7}{"зорилт%":>10}{"p":>10}')
    for ds in ('TRAIN', 'UNSEEN'):
        for lab, m in (('БАЙХГҮЙ', ~e.has_retest), ('БАЙГАА', e.has_retest)):
            x = e[(e.ds == ds) & m]
            p, t, s, _, _ = rate(x.out.to_numpy())
            if t + s < 20:
                continue
            print(f'  {ds:8}{lab:12}{t + s:7}{p:9.1f}%{_pv(t, t + s):10.4f}')
    print('  Давталтын ГҮН нь ч аварч чаддаггүй:')
    r = e[e.has_retest]
    for lo, hi, nm in ((0, .1, '< 0.1 ATR'), (.1, .3, '0.1–0.3'),
                       (.3, .6, '0.3–0.6'), (.6, 99, '> 0.6')):
        x = r[(r.retest_atr >= lo) & (r.retest_atr < hi)]
        p, t, s, _, _ = rate(x.out.to_numpy())
        if t + s:
            print(f'    {nm:12}{t + s:7}{p:9.1f}%')

    # ── СҮЛЖЭЭ ───────────────────────────────────────────────────
    print(f'\n{"=" * 66}\nTRAIN СҮЛЖЭЭ — None нь ҮНЭХЭЭР шүүлтгүй\n'
          f'{"=" * 66}')
    tr = e[e.ds == 'TRAIN']
    grid = []
    for mom in (None, 0.0, 0.5, 1.0):
        for rq, rt, rn in ((False, None, 'шаардахгүй'),
                           (True, None, 'зөвхөн байх'),
                           (True, 0.1, '≥ 0.1 ATR'),
                           (True, 0.3, '≥ 0.3 ATR'),
                           (True, 0.5, '≥ 0.5 ATR')):
            x = pick(tr, mom, rt, rq)
            p, t, s, am, nn = rate(x.out.to_numpy())
            grid.append({'mom': mom, 'ret': rn, 'n': len(x),
                         'resolved': t + s, 'pct': p})
    g = pd.DataFrame(grid)
    print(f'  {"1ц momentum":14}{"давталт":14}{"n":>7}{"шийдэгдсэн":>12}'
          f'{"зорилт%":>10}')
    for _, r in g.iterrows():
        mm = 'шүүлтгүй' if r['mom'] is None else f'≥ {r["mom"]}'
        print(f'  {mm:14}{r["ret"]:14}{r["n"]:7}{r["resolved"]:12}'
              f'{r["pct"]:9.1f}%')

    # ── СОНГОЛТ ──────────────────────────────────────────────────
    MIN_N = 200      # эх кодод 20 байсан — n=20 дээр алдаа ±11 пункт
    v = g[g.resolved >= MIN_N].sort_values('pct', ascending=False)
    print(f'\n  Хамгийн бага {MIN_N} шийдэгдсэн арилжаа шаардав '
          f'({len(v)}/{len(g)} мөр тэнцэв)')
    if v.empty:
        print('  ✗ нэг ч дүрэм тэнцсэнгүй')
        return 0
    best = v.iloc[0]
    print(f'  → 1ц momentum {best["mom"]}, давталт {best["ret"]}  '
          f'({best["pct"]:.1f}% TRAIN дээр)')

    # ── UNSEEN ───────────────────────────────────────────────────
    print(f'\n{"=" * 66}\nUNSEEN — дүрмийг хөдөлгөөгүй\n{"=" * 66}')
    rmap = {'шаардахгүй': (False, None), 'зөвхөн байх': (True, None),
            '≥ 0.1 ATR': (True, 0.1), '≥ 0.3 ATR': (True, 0.3),
            '≥ 0.5 ATR': (True, 0.5)}
    rq, rt = rmap[best['ret']]
    un = pick(e[e.ds == 'UNSEEN'], best['mom'], rt, rq)
    for lbl, al in (('AMBIG хассан', False), ('AMBIG алдагдал гэж', True)):
        p, t, s, am, nn = rate(un.out.to_numpy(), al)
        cost = a.spread / (a.k * df.ATR.iloc[-len(df) // 3:].median())
        exp_r = (p / 100 * 1 + (1 - p / 100) * -1) - cost if np.isfinite(p) \
            else np.nan
        print(f'  {lbl:20} n={t + s:5}  зорилт {p:.1f}%  '
              f'зардлын дараа {exp_r:+.3f}R')
    print(f'  суурь (санамсаргүй): урт {bl[1]:.1f}%  богино {bl[-1]:.1f}%')
    print(f'  AMBIG {(un.out == "AMBIG").sum()}   '
          f'дуусаагүй {(un.out == "NONE").sum()}')

    # ── ХААЛТЫН ХЭМЖЭЭ ───────────────────────────────────────────
    # Зардал нь R-ээр илэрхийлэхэд spread ÷ (k·ATR) — хаалт ТОМ байх
    # тусам харьцангуй зардал БАГА. Тиймээс «ирмэг байна уу» ба
    # «зардлын дараа үлдэх үү» хоёр өөр асуулт.
    print(f'\n{"=" * 66}\nХААЛТЫН ХЭМЖЭЭ — ирмэг зардлыг давж байна уу\n'
          f'{"=" * 66}')
    print(f'  {"k":>5}{"багц":>8}{"n":>7}{"зорилт%":>10}{"суурь":>9}'
          f'{"зөрүү":>8}{"зардал":>9}{"цэвэр R":>10}{"p":>9}')
    from math import erfc, sqrt
    for k in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
        ok, st = outcomes(df, e, k)
        bk = baseline(df, k)
        for nm in ('TRAIN', 'UNSEEN'):
            m = (e.ds == nm).to_numpy()
            oo, ss = ok[m], st[m]
            dd = e.dir.to_numpy()[m]
            t = (oo == 'TARGET').sum()
            s_ = (oo == 'STOP').sum()
            nres = t + s_
            if not nres:
                continue
            p = t / nres * 100
            # Суурь нь чиглэлийн хольцоор жигнэгдэнэ
            w = (dd == 1).mean()
            base = bk[1] * w + bk[-1] * (1 - w)
            res = np.isin(oo, ('TARGET', 'STOP'))
            cost = np.nanmean(a.spread / ss[res])
            net = (p / 100) - (1 - p / 100) - cost
            # Суурьтай харьцуулсан хоёр талт p-утга. n нь хэдэн зуу тул
            # хэвийн ойролцоолол хангалттай (яг биномыг бодоход
            # факториал нь хэт том болж халина).
            q = base / 100
            z = (t / nres - q) / sqrt(q * (1 - q) / nres)
            pv = erfc(abs(z) / sqrt(2))
            print(f'  {k:5.1f}{nm[:6]:>8}{nres:7}{p:9.1f}%{base:8.1f}%'
                  f'{p - base:+8.1f}{cost:9.3f}{net:+10.3f}{pv:9.4f}')

    print(f'\n{"=" * 66}')
    print('  Уншихдаа: «зорилт %» нь 50-иас биш, СУУРИАС дээш гарсан')
    print('  эсэхээр шүүнэ. Тэгш хаалт дээр алтны дрифт нь урт талыг')
    print('  аль хэдийн 50-аас дээш гаргадаг.')
    print('  «цэвэр R» нь спредийг арилжаа тус бүрийн ЖИНХЭНЭ хаалтаар')
    print('  хассан дүн — эерэг байж байж л ирмэг нь ашиг болно.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
