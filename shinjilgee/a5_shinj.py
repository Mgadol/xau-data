"""5. Аль цэвэрлэгээ ХҮЧТЭЙ вэ — шинж бүрийг үр дүнтэй нь харьцуулна.

«IDM аль нь хүчтэй вэ» гэсэн асуултын хариу. Цэвэрлэгээ бүрд оролтын
ӨМНӨ мэдэгдэх шинжүүдийг тооцоод, шинж бүрээр 5 хэсэгт хувааж дундаж
R-ийг харна. Хэсгүүдийн хооронд ялгаа гарахгүй бол тэр шинж мэдээлэл
агуулаагүй гэсэн үг.

Шинжүүд (бүгд оролтын мөчид мэдэгддэг — ирээдүй харахгүй):
  depth     — түвшнээс хэр гүн давсан бэ (ATR-ээр)   ← ХАМГИЙН ХҮЧТЭЙ
  touches   — тэр түвшинг өмнө хэдэн удаа шалгасан бэ
  age       — түвшин тогтоод хэдэн бар өнгөрсөн бэ
  speed     — хэдэн барын дотор эргэж дотогшоо хаагдсан бэ
  squeeze   — өмнөх шахалт: 20 барын ATR / 100 барын ATR
  volspike  — цэвэрлэгээний барын эрчим / дундаж
  poc_dist  — хамгийн их эрчимтэй үнээс хэр хол вэ
  hour      — сессийн цаг (брокерийн цаг; УБ = +5)

ЧУХАЛ ДҮГНЭЛТҮҮД

1. ШАХАЛТЫН ТААМАГ БАТЛАГДААГҮЙ
   «5 минут дээр лаа жижгэрээд дараа нь хөдөлнө» гэсэн таамаг өгөгдөл
   дээр гараагүй. squeeze бага (шахагдсан) үед −0.092R, squeeze их
   (өргөжсөн) үед +0.083R. Тайван байдал биш, ХӨДӨЛГӨӨН нь дараагийн
   хөдөлгөөнийг авчирдаг.

2. ГҮН нь хамгийн их мэдээлэлтэй шинж — жигд өснө (доороос дээш).
   Гэхдээ a4-д үзсэнчлэн арилжаанд хүрэлцэхгүй.

3. ОРОЙН ЦАГ ХОРТОЙ. УБ-ийн 23:00-аас хойш −0.202R. Энэ бол
   хамгийн тодорхой САНУУЛГА: тэр цагт бүү ор.

4. touches, volspike, poc_dist бараг мэдээлэлгүй. «Түвшинг хэдэн удаа
   шалгасан бэ» гэдэг олон хүний ярьдаг зүйл — энд нөлөө үзүүлээгүй.

АНХААРУУЛГА — НЭГ УДАА ХУДАЛ ОЛДВОР ГАРСАН
  Анх `age` (түвшин хэдэн бар тогтсон) нь бүх шинжээс ХАМГИЙН хүчтэй
  харагдсан: age ≤ 32 бар дээр +0.790R, хоёр хугацаанд, урт богино
  хоёуланд нь. Энэ нь ирээдүй харсны үр дүн байв — core.bar_len-ийг
  үзнэ үү. Залруулсны дараа −0.079R болж алга болсон.

  Яг тэр шинж нь алдаанд хамгийн ойр байсан нь санамсаргүй биш:
  алдаа нь эхний 48 барт байсан, `age` нь яг тэрийг хэмждэг.
"""
import numpy as np
import pandas as pd
from core import load, resample, zigzag, confirm_index, bar_len
import a4_tsewerlegee as S

H, L, C, V = S.H, S.L, S.C, S.D5['volume'].values
IDX = S.IDX
ATR20 = S.ATR20
_tr = np.maximum(H[1:] - L[1:], np.maximum(abs(H[1:] - C[:-1]), abs(L[1:] - C[:-1])))
_TR = np.concatenate([[H[0] - L[0]], _tr])
ATR100 = pd.Series(_TR).rolling(100).mean().values
VOL50 = pd.Series(V).rolling(50).mean().values


def poc(i, n=500, bins=60):
    """Сүүлийн n барын хамгийн их эрчимтэй үнэ (point of control)."""
    a = max(0, i - n)
    if i - a < 50:
        return np.nan
    p, v = C[a:i], V[a:i]
    lo_, hi_ = p.min(), p.max()
    if hi_ <= lo_:
        return np.nan
    b = np.clip(((p - lo_) / (hi_ - lo_) * bins).astype(int), 0, bins - 1)
    return lo_ + (np.bincount(b, weights=v, minlength=bins).argmax() + 0.5) / bins * (hi_ - lo_)


def collect(tf='4h', pct=0.01, rr=2.0, maxbars=288, spread=0.3):
    """Цэвэрлэгээ бүрийг шинжүүдийнх нь хамт цуглуулна."""
    d = resample(S.h, tf)
    dt = bar_len(tf)          # баталгаа нь бар ХААГДАХАД мэдэгдэнэ — core.bar_len
    rows = []
    for (pi, pv, pdir) in zigzag(d, pct):
        ci = confirm_index(d, pi, pv, pdir, pct)
        if ci is None:
            continue
        s = IDX.searchsorted(d.index[ci] + dt)
        if s < 1000 or s >= len(IDX) - maxbars:
            continue
        short = (pdir == 1)
        far, first = pv, None
        for i in range(s, s + maxbars):
            if not (H[i] > pv if short else L[i] < pv):
                continue
            if first is None:
                first = i
            far = max(far, H[i]) if short else min(far, L[i])
            if not (C[i] < pv if short else C[i] > pv):
                continue

            e = C[i] - spread if short else C[i] + spread
            st = far
            if (st - e if short else e - st) <= 0:
                break
            risk = abs(st - e)
            tg = e - rr * risk if short else e + rr * risk
            r = None
            for j in range(i + 1, min(i + maxbars, len(IDX))):
                if short:
                    if H[j] >= st: r = -1.0; break
                    if L[j] <= tg: r = rr;   break
                else:
                    if L[j] <= st: r = -1.0; break
                    if H[j] >= tg: r = rr;   break
            if r is None:
                px = C[min(i + maxbars, len(IDX)) - 1]
                r = ((e - px) if short else (px - e)) / risk

            a = ATR20[i] if ATR20[i] > 0 else np.nan
            p_ = poc(i)
            w = slice(max(0, s - 1000), s)   # түвшнийг өмнө хэдэн удаа шалгасан
            near = np.sum((np.abs(H[w] - pv) < 0.15 * a) if short
                          else (np.abs(L[w] - pv) < 0.15 * a)) if a == a else np.nan
            rows.append(dict(
                t=IDX[i], R=r, short=short, year=IDX[i].year,
                touches=near, age=(i - s), speed=(i - first + 1),
                depth=abs(far - pv) / a if a == a else np.nan,
                squeeze=ATR20[i] / ATR100[i] if ATR100[i] > 0 else np.nan,
                volspike=V[i] / VOL50[i] if VOL50[i] > 0 else np.nan,
                poc_dist=abs(pv - p_) / a if (p_ == p_ and a == a) else np.nan,
                hour=IDX[i].hour))
            break
    return pd.DataFrame(rows)


def buhel(df, f, q=5):
    """Нэг шинжээр 5 хэсэгт хувааж дундаж R-ийг хэвлэнэ."""
    s = df.dropna(subset=[f])
    if len(s) < 200:
        return
    try:
        qq = pd.qcut(s[f], q, labels=False, duplicates='drop')
    except ValueError:
        return
    g = s.groupby(qq).agg(n=('R', 'size'), R=('R', 'mean'),
                          lo=(f, 'min'), hi=(f, 'max'))
    print(f"   {f:<10}  (хэсгүүдийн хамгийн их зөрүү {g['R'].max() - g['R'].min():+.3f}R)")
    for _, row in g.iterrows():
        bar = '█' * max(0, int((row['R'] + 0.3) * 20))
        print(f"      {row['lo']:>7.2f}–{row['hi']:<8.2f} n={int(row['n']):>4} "
              f"{row['R']:>+7.3f}R  {bar}")
    print()


if __name__ == '__main__':
    df = collect()
    print(f"Цэвэрлэгээ: {len(df):,}    дундаж {df['R'].mean():+.3f}R\n")
    print("Шинж бүрээр 5 хэсэгт хуваасан дундаж R")
    print("Зөрүү их байх тусам тэр шинж илүү их мэдээлэл агуулж байна.\n")
    for f in ('depth', 'touches', 'age', 'speed', 'squeeze', 'volspike', 'poc_dist'):
        buhel(df, f)

    print("   Сессийн цагаар (брокерийн цаг; Улаанбаатар = +5):")
    g = df.groupby(df['hour'] // 3 * 3).agg(n=('R', 'size'), R=('R', 'mean'))
    for k, row in g.iterrows():
        if row['n'] < 40:
            continue
        ub = (int(k) + 5) % 24
        print(f"      {int(k):>2}:00–{int(k) + 3:>2}:00  (УБ {ub:>2}:00)  "
              f"n={int(row['n']):>4}  {row['R']:>+6.3f}R")

    # АНХААР: s.squeeze бол DataFrame-ийн МЕТОД. Багана руу заавал s['squeeze'].
    print("\n   Шинжүүдийн хослол — гүн ба шахалт хамт:")
    s = df.dropna(subset=['depth', 'squeeze'])
    s = s.assign(g=(s['depth'] >= 3).map({True: 'гүн≥3', False: 'гүехэн'}),
                 q=(s['squeeze'] >= 1).map({True: 'өргөжсөн', False: 'шахагдсан'}))
    for (a, b), row in s.groupby(['g', 'q']).agg(n=('R', 'size'), R=('R', 'mean')).iterrows():
        print(f"      {a:<7} + {b:<10} n={int(row['n']):>4}  {row['R']:>+6.3f}R")

    # `age` нь `depth`-ээс ч том зөрүү үзүүлсэн тул тусад нь шалгах ёстой.
    # Зөрүү том байх нь хангалтгүй — хугацаа болон тал дээр давтагдах ёстой.
    print("\n   ШИНЭ түвшин (age ≤ 32 бар = 2.7 цаг) — дөрвөн шалгуураар:")
    a32 = df[df['age'] <= 32]
    for sel, lbl in ((a32, 'бүгд'),
                     (a32[a32['year'] < 2017], '2005–2016'),
                     (a32[a32['year'] >= 2017], '2017–2025'),
                     (a32[~a32['short']], 'зөвхөн УРТ'),
                     (a32[a32['short']], 'зөвхөн БОГИНО')):
        R = sel['R'].values
        if len(R) < 25:
            print(f"      {lbl:<14} n={len(R):>4}  (цөөн)"); continue
        se = R.std() / np.sqrt(len(R))
        print(f"      {lbl:<14} n={len(R):>4}  {R.mean():>+6.3f}R ±{se:.3f}"
              f"{'  ✓' if R.mean() > 2 * se else '  ✗'}")

    print("\n   ГҮН ба ШИНЭ хоёр ижил зүйлийг хэмжиж байна уу:")
    both = df.dropna(subset=['depth'])
    print(f"      харилцан хамаарал (age vs depth): "
          f"{both['age'].corr(both['depth']):+.3f}")
    for g_, lbl in ((both[(both['age'] <= 32) & (both['depth'] >= 3)], 'шинэ + гүн'),
                    (both[(both['age'] <= 32) & (both['depth'] < 3)], 'шинэ + гүехэн'),
                    (both[(both['age'] > 32) & (both['depth'] >= 3)], 'хуучин + гүн'),
                    (both[(both['age'] > 32) & (both['depth'] < 3)], 'хуучин + гүехэн')):
        print(f"      {lbl:<16} n={len(g_):>4}  {g_['R'].mean():>+6.3f}R")
