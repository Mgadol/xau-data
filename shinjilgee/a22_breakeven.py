"""22. Break-even стоп — ашигт орсны дараа стопыг оролт руу зөөх.

АСУУЛТ
  «Ашигтай болонгуут break-even тавьж байгаа юу? 20 pip яваад
   тавиад үзээч.»

  Өмнөх бүх тест (a2–a21) ХАТУУ стоптой байсан. Break-even огт
  шалгаагүй. Энэ нь шударга эсэргүүцэл.

PIP-ИЙН ТОХИРОЛЦОО
  Алтан дээр ихэвчлэн 1 pip = $0.10 тул 20 pip = $2.00.
  Зарим брокер $1.00-г 1 pip гэдэг. Тиймээс энд $1, $2, $5, $10
  болон R-ийн эзлэхүүнээр (0.5R, 1R) — бүгдийг шалгана.

БУСАД ЮУ Ч ӨӨРЧЛӨГДӨХГҮЙ
  Оролт, анхны стоп, target бүгд a19-ийн Turtle Soup-тай ижил.
  Цорын ганц ялгаа нь стоп ХӨДӨЛДӨГ болсон явдал.

ШУДАРГА ТООЦОО — ХОЁР ЗҮЙЛИЙГ АЛДАХГҮЙ

  1. Break-even гэдэг нь ҮНЭНДЭЭ ТЭГ БИШ. Оролт дээр хаагдахад
     спред дахин төлнө. Тиймээс BE стоп нь бага зэрэг СӨРӨГ.

  2. Нэг барын дотор BE босго ба стоп хоёулаа хүрч болно. 5 минутын
     барын дотор ямар дараалалтай болсныг мэдэх аргагүй тул
     БОЛГООМЖТОЙ тал руу нь тооцно: эхлээд стоп хүрсэн гэж үзнэ.

     ШАЛГАСАН: эсрэг дараалал (BE-г эхэлж) нь үр дүнг БҮР ДОРДУУЛАВ
     (BE $2: −0.090R → −0.138R). Учир нь эрт зөөвөл илүү олон
     хожлыг таслана. Тэгэхээр миний таамаг BE-д ТААТАЙ байсан —
     дүгнэлт аль ч талаас нь бат бөх.

═══════════════════════════════════════════════════════════════════
ҮР ДҮН: BREAK-EVEN БҮХ ТОХИРГООНД ДОРДУУЛСАН
═══════════════════════════════════════════════════════════════════

      BE АШИГЛААГҮЙ (жишиг)   9309   35.0%   −0.053R
      BE $1  (10 pip)         9309   10.8%   −0.112R
      BE $2  (20 pip)         9309   16.6%   −0.090R
      BE $5  (50 pip)         9309   25.9%   −0.077R
      BE $10 (100 pip)        9309   32.3%   −0.057R

      BE 0.25R                9309   11.7%   −0.115R
      BE 0.5R                 9309   18.4%   −0.105R
      BE 1.0R                 9309   27.5%   −0.076R
      BE 1.5R                 9309   32.4%   −0.062R

  ЖИГД: босго нарийсах тусам дордоно. Босго хол болох тусам
  ховор ажиллаж, BE-гүйтэй ойртоно. Хаана ч сайжруулаагүй.

ЯАГААД — ЗАДАРГАА

                       алдсан    BE   хожсон   дундаж
      BE ашиглаагүй     60.0%   9.4%   25.3%   −0.053R
      BE $2 (20 pip)    37.0%  46.8%   14.7%   −0.090R
      BE 1R             49.9%  25.6%   20.5%   −0.076R

  BE нь ҮНЭХЭЭР алдагдлыг бууруулж байна: 60.0% → 37.0%.
  Гэвч хожлыг мөн таслав: 25.3% → 14.7%.

  Тооцоо нь энгийн:
      нэг хожлыг таслах       = −2R алдана (TP 1:2)
      нэг алдагдлыг аврах     = +1R авна
  Тиймээс аврах нь таслахаас ХОЁР ДАХИН олон байж гэмээнэ ашигтай.
  Бодит дээр 23.0 нэгж аврахад 10.6 нэгж хожил тасарсан — харьцаа
  2.17:1 буюу 2:1-ээс арай дээш. Гэвч «BE» гэдэг нь ҮНЭНДЭЭ ТЭГ
  БИШ (спред дахин төлнө) тул эцсийн дүн нь сөрөг үлдэв.

ТҮГЭЭМЭЛ ОЙЛГОЛТЫН ЭСРЭГ — TARGET ХОЛ БАЙХ ТУСАМ BE НЬ ИЛҮҮ ХОРТОЙ

      TP 1:1   BE-гүй −0.070R   BE 1R −0.070R   ялгаа +0.000R
      TP 1:2   BE-гүй −0.053R   BE 1R −0.076R   ялгаа −0.022R
      TP 1:3   BE-гүй −0.050R   BE 1R −0.079R   ялгаа −0.029R
      TP 1:5   BE-гүй −0.022R   BE 1R −0.057R   ялгаа −0.035R

  «Target хол байвал BE илүү хэрэгтэй» гэдэг нь ЭСРЭГЭЭРЭЭ.
  Хол target-д хүрэх зам урт тул BE-д тасрах магадлал өснө.

ШУДАРГА БАЙХЫН ТУЛД — BE-Д ХЭМЖИГДЭХГҮЙ АШИГ БАЙНА

  R-ийн тоо бүхнийг хэмждэггүй. BE нь БҮТЭН АЛДАГДЛЫН ДАВТАМЖИЙГ
  60% → 37% болгож бууруулсан. Энэ нь арилжааны СЭТГЭЛ ЗҮЙН
  туршлагыг бодитоор өөрчилнө — дараалсан бүтэн алдагдал бол
  дүрэм зөрчих гол шалтгаан.

  Өртөг нь 0.02–0.06R. Хэрэв энэ нь чамайг дүрэмдээ үлдэхэд
  тусалдаг бол тэр үнэ нь хямд байж болно. Гэхдээ энэ нь
  СЭТГЭЛ ЗҮЙН хэрэгсэл болохоос ИРМЭГ бүтээдэг зүйл БИШ —
  эдгээр хоёрыг андуурч болохгүй.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def setups(tf='4h', K=3):
    """a19-ийн Turtle Soup — өмнөх K лааны туйлыг цэвэрлээд буцаж хаагдана."""
    d = resample(h, tf)
    H, L, C = d['high'].values, d['low'].values, d['close'].values
    dt = bar_len(tf)
    out = []
    for i in range(K, len(d) - 1):
        for short in (True, False):
            if short:
                lvl = H[i - K:i].max()
                if not (H[i] > lvl and C[i] < lvl):
                    continue
                far = H[i]
            else:
                lvl = L[i - K:i].min()
                if not (L[i] < lvl and C[i] > lvl):
                    continue
                far = L[i]
            out.append(dict(t=d.index[i] + dt, short=short,
                            entry=C[i], stop=far, year=d.index[i].year))
    return out


SET = setups()


def run(be=None, be_r=None, rr=2.0, spread=0.3, hold=288,
        side=None, years=None):
    """be   : break-even босго $-аар (ж: 2.0 = 20 pip)
       be_r : break-even босго R-ээр (ж: 1.0 = 1R яваад)
       Хоёулаа None бол break-even АШИГЛАХГҮЙ (a19-тай ижил)."""
    res = []
    for s in SET:
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        short = s['short']
        if side == 'urt' and short:
            continue
        if side == 'bogino' and not short:
            continue
        e = s['entry'] - spread if short else s['entry'] + spread
        st0 = s['stop']
        risk = (st0 - e) if short else (e - st0)
        if risk <= 0:
            continue
        tg = e - rr * risk if short else e + rr * risk
        trig = be if be is not None else (be_r * risk if be_r else None)

        k = I5.searchsorted(s['t'])
        if k >= len(I5) - hold:
            continue
        st = st0
        moved = False
        r = None
        for x in range(k, k + hold):
            # ── БОЛГООМЖТОЙ ДАРААЛАЛ: стопыг ЭХЛЭЭД шалгана ──
            # Нэг барын дотор аль нь түрүүлснийг мэдэх аргагүй тул
            # муу талд нь тооцно. Эс тэгвэл BE хиймлээр сайхан гарна.
            if short:
                if H5[x] >= st:
                    r = 0.0 - spread / risk if moved else -1.0
                    break
                if L5[x] <= tg:
                    r = rr
                    break
                if trig is not None and not moved and (e - L5[x]) >= trig:
                    st, moved = e, True
            else:
                if L5[x] <= st:
                    r = 0.0 - spread / risk if moved else -1.0
                    break
                if H5[x] >= tg:
                    r = rr
                    break
                if trig is not None and not moved and (H5[x] - e) >= trig:
                    st, moved = e, True
        if r is None:
            px = C5[min(k + hold, len(I5)) - 1]
            r = ((e - px) if short else (px - e)) / risk
        res.append(r)
    return np.array(res)


if __name__ == '__main__':
    print("Break-even стоп · Turtle Soup бүтэц · 4 цаг · TP 1:2 · спред $0.3")
    print(f"{len(SET):,} setup\n")

    print("── 1. $-аар тогтоосон босго ──")
    print("   «20 pip» = $2.00 (1 pip = $0.10)\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 62)
    print("   " + stat(run(), 'BE АШИГЛААГҮЙ (жишиг)'))
    for x in (1.0, 2.0, 5.0, 10.0):
        print("   " + stat(run(be=x), f'BE {x:.0f}$ яваад  ({x * 10:.0f} pip)'))

    print("\n── 2. R-ээр тогтоосон босго ──")
    print("   Эрсдэлийн хэмжээнээс хамаарна — илүү утга учиртай.\n")
    print("   " + stat(run(), 'BE АШИГЛААГҮЙ (жишиг)'))
    for x in (0.25, 0.5, 0.75, 1.0, 1.5):
        print("   " + stat(run(be_r=x), f'BE {x}R яваад'))

    print("\n── 3. ЮУ БОЛЖ БАЙНА ВЭ — үр дүнгийн задаргаа ──")
    print("   BE нь хожлыг ХАЗААРДАГ уу, алдагдлыг АВРАДАГ уу?\n")
    print(f"   {'':<24}{'n':>6}{'алдсан':>9}{'BE':>8}{'хожсон':>9}{'дундаж':>10}")
    print("   " + "─" * 66)
    for lbl, kw in (('BE ашиглаагүй', {}), ('BE $2 (20 pip)', dict(be=2.0)),
                    ('BE 0.5R', dict(be_r=0.5)), ('BE 1R', dict(be_r=1.0))):
        R = run(**kw)
        loss = (R <= -0.9).mean() * 100
        bee = ((R > -0.9) & (R < 0.5)).mean() * 100
        win = (R >= 1.5).mean() * 100
        print(f"   {lbl:<24}{len(R):>6}{loss:>8.1f}%{bee:>7.1f}%"
              f"{win:>8.1f}%{R.mean():>+9.3f}R")

    print("\n── 4. Хамгийн сайн BE-г дөрвөн шалгуураар ──\n")
    print("   " + stat(run(be_r=1.0), 'BE 1R · бүгд'))
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО')):
        print("   " + stat(run(be_r=1.0, **kw), '  ' + lbl))

    print("\n── 5. Target өөр байвал BE ашигтай болох уу ──")
    print("   TP хол байх тусам BE илүү хэрэгтэй гэж үздэг.\n")
    for rr in (1.0, 2.0, 3.0, 5.0):
        a = run(rr=rr)
        b = run(rr=rr, be_r=1.0)
        d = b.mean() - a.mean()
        print(f"   TP 1:{rr:.0f}   BE-гүй {a.mean():>+7.3f}R   "
              f"BE 1R {b.mean():>+7.3f}R   ялгаа {d:>+7.3f}R")
