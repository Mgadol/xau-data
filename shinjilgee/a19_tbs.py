"""19. TBS (Turtle Body Soup) + «Model #1» баталгаа.

БҮТЭЦ (зурган дээрхээр)
    Өмнөх K лааны ДЭЭД цэг = түвшин
    Лаа түүнийг цэвэрлээд буцаж ДООШ хаагдана        → TBS
    Дараа нь үнэ «Model #1» буюу цэвэрлэгээний ӨМНӨХ
    K лааны ДООД цэгээс доош хаагдвал                → БАТАЛГААЖСАН

  Зурган дээр зүүн талд баталгаажаагүй, баруун талд баталгаажсан.
  Ялгаа нь ганцхан: сүүлчийн улаан лаа доод түвшнийг эвдсэн эсэх.

ХОЁР ЯЛГАА ШАЛГАНА

  1. Цэвэрлэгээний гүн — «soup» vs «BODY soup»
       wick : лааны СҮҮЛ л түвшнээс дээш гарна  (энгийн Turtle Soup)
       body : лааны ИХ БИЕ ч дээш гарна          (Turtle BODY Soup)
     TBS нь илүү гүн цэвэрлэгээ гэсэн үг. a4-т гүн нь мэдээлэлтэй
     гарсан тул энэ нь тустай байж МАГАДГҮЙ.

  2. «Model #1» баталгаа
       none   : цэвэрлэсэн лаа хаагдахад шууд орно  (= a7-гийн CRT)
       model1 : доод түвшин эвдэртэл ХҮЛЭЭНЭ

УРЬДЧИЛСАН ТААМАГ (тест хийхээс ӨМНӨ бичив)
  Баталгаа хүлээхэд ялалтын хувь ӨСНӨ, гэхдээ стоп нь цэвэрлэгээний
  туйл дээр ТОГТСОН хэвээр үлддэг тул оролт стопоос холдож эрсдэл
  өснө → R жижгэрнэ. a9 (order block)-д яг ингэж болсон: limit
  −0.036R, баталгаа −0.069R.

  a2-т баталгаа ТУСАЛСАН, учир нь тэнд стоп нь бүтцээс хамаарч
  ХОЛ байсан. Дүрэм нь: баталгаа хүлээх нь стоп ХӨДӨЛДӨГ үед л
  ажиллана. Энд стоп хөдөлдөггүй.

  Тиймээс таамаг: ялалт ӨСНӨ, дундаж R нь ДООШЛОНО эсвэл тэгэлцэнэ.

═══════════════════════════════════════════════════════════════════
ҮР ДҮН — ТААМАГ БУРУУ БАЙВ. Баталгаа ТУСАЛСАН.
═══════════════════════════════════════════════════════════════════

      Turtle Soup · шууд          9309   35.0%   −0.053R ±0.013
      Turtle Soup · БАТАЛГААТАЙ   2544   46.3%   +0.025R ±0.017

  0.078R-ийн сайжруулалт. Ялалт 35.0% → 46.3%. Би эсрэгээр таамагласан.

ЯАГААД ТУСАЛСАН БЭ — ЖИНХЭНЭ ШАЛТГААН

  Эрсдэл үнэхээр ГУРВА ДАХИН өссөн:

      TS · шууд         медиан эрсдэл  $4.40
      TS · баталгаатай  медиан эрсдэл  $14.25

  Би үүнийг сул тал гэж бодсон. Гэтэл ЭСРЭГЭЭРЭЭ — стоп холдох тусам
  спред эрсдэлийн бага хувийг эзэлнэ:

      $4.40  → спред $0.3 нь 6.8%
      $14.25 → спред $0.3 нь 2.1%

  a18-д яг ижил зүй тогтол гарсан (стоп ≥$4 нь хамгийн сайн).
  Өргөн стоп нь ХОРОГДОЛ биш, зардал даах ЧАДВАР юм.

  a9 (order block)-д баталгаа хүлээхэд ДОРДСОН нь стоп нь мужийн
  цаана ОЙРХОН тогтсон байсан учир. Энд стоп нь цэвэрлэгээний туйл
  дээр байгаа ч оролт нь түүнээс ХОЛДДОГ тул үр дүн нь өөр.

  → ЗӨВ ДҮРЭМ нь «баталгаа хүлээ» ч биш, «бүү хүлээ» ч биш:
    ҮҮССЭН СТОПЫН ЗАЙ спредээс хэр том бэ гэдэг нь шийднэ.

ГЭВЧ ДӨРВӨН ШАЛГУУРЫГ ДАВААГҮЙ

      бүгд            2544   46.3%   +0.025R ±0.017  ✗
      2005–2016       1432   47.5%   +0.048R ±0.023  ✓
      2017–2025       1112   44.7%   −0.004R ±0.025  ✗   ← алга болсон
      зөвхөн УРТ      1311   49.6%   +0.065R ±0.024  ✓
      зөвхөн БОГИНО   1233   42.7%   −0.017R ±0.024  ✗   ← ТЭГШ ХЭМ АЛДАРСАН

  Урт, богиногийн зөрүү 0.082R. Зөвхөн урт тал нь ажиллаж байгаа нь
  аргачлал биш, алтны өсөх хандлага гэдгийн шинж.

  Спред $0.6 болгоход −0.001R. 2017-оос хойш тэг. Хугацаагаар:
  1ц −0.035R, 4ц +0.025R, өдөр +0.008R.

«BODY SOUP» ГЭДЭГ НЬ ХЭМЖИХ БОЛОМЖГҮЙ ХОВОР

      Turtle BODY Soup · шууд        187
      Turtle BODY Soup · баталгаатай  47

  Их бие нь түвшнээс дээш гарсан цэвэрлэгээ 20 жилд 187 удаа —
  жилд 9. Баталгаатай нь 47 буюу жилд 2. Ямар ч тоо утгагүй.
  Зурган дээрх «TS vs TBS» ялгаа нь практикт бараг тохиолддоггүй.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def setups(tf='4h', soup='wick', confirm='none', K=3, wait=6):
    """TBS бүтцүүдийг олно.

    K    : түвшин тогтоох ухрах цонх (лааны тоо)
    wait : баталгааг хэдэн лааны дотор хүлээх вэ
    """
    d = resample(h, tf)
    H, L, C, O = (d['high'].values, d['low'].values,
                  d['close'].values, d['open'].values)
    dt = bar_len(tf)
    out = []
    for i in range(K, len(d) - wait - 1):
        for short in (True, False):
            if short:
                lvl = H[i - K:i].max()          # өмнөх K лааны дээд
                m1 = L[i - K:i].min()           # Model #1 = доод
                swept = H[i] > lvl
                back = C[i] < lvl
                body = max(O[i], C[i]) > lvl
            else:
                lvl = L[i - K:i].min()
                m1 = H[i - K:i].max()
                swept = L[i] < lvl
                back = C[i] > lvl
                body = min(O[i], C[i]) < lvl
            if not (swept and back):
                continue
            if soup == 'body' and not body:
                continue

            far = H[i] if short else L[i]       # стоп — цэвэрлэгээний туйл
            if confirm == 'none':
                j, entry = i, C[i]
            else:
                j = None
                for x in range(i + 1, i + 1 + wait):
                    # Баталгаа ирэхээс өмнө стоп хүрвэл арилжаа БАЙХГҮЙ
                    if (H[x] > far) if short else (L[x] < far):
                        break
                    if (C[x] < m1) if short else (C[x] > m1):
                        j, entry = x, C[x]
                        break
                if j is None:
                    continue
            out.append(dict(t=d.index[j] + dt, short=short, entry=entry,
                            stop=far, lvl=lvl, m1=m1, year=d.index[j].year))
    return out


def run(tf='4h', soup='wick', confirm='none', rr=2.0, spread=0.3,
        hold=288, side=None, years=None, ret_risk=False, **kw):
    """R-ийн жагсаалт. ret_risk=True бол (R, эрсдэл $) буцаана."""
    res = []
    for s in setups(tf, soup, confirm, **kw):
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        short = s['short']
        if side == 'urt' and short:
            continue
        if side == 'bogino' and not short:
            continue
        e = s['entry'] - spread if short else s['entry'] + spread
        st = s['stop']
        risk = (st - e) if short else (e - st)
        if risk <= 0:
            continue
        tg = e - rr * risk if short else e + rr * risk
        k = I5.searchsorted(s['t'])
        if k >= len(I5) - hold:
            continue
        r = None
        for x in range(k, k + hold):
            if short:
                if H5[x] >= st: r = -1.0; break
                if L5[x] <= tg: r = rr;   break
            else:
                if L5[x] <= st: r = -1.0; break
                if H5[x] >= tg: r = rr;   break
        if r is None:
            px = C5[k + hold - 1]
            r = ((e - px) if short else (px - e)) / risk
        res.append((r, risk) if ret_risk else r)
    return np.array(res)


if __name__ == '__main__':
    print("TBS (Turtle Body Soup) + «Model #1» баталгаа")
    print("4 цаг, түвшин = өмнөх 3 лаа, стоп = цэвэрлэгээний туйл,")
    print("TP 1:2, спред $0.3\n")

    print("── 1. ГОЛ ХАРЬЦУУЛАЛТ — баталгаа тусалдаг уу ──\n")
    print(f"   {'':<34}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 66)
    for soup in ('wick', 'body'):
        nm = 'Turtle Soup' if soup == 'wick' else 'Turtle BODY Soup'
        for cf in ('none', 'model1'):
            lbl = f"{nm} · {'шууд' if cf == 'none' else 'БАТАЛГААТАЙ'}"
            print("   " + stat(run(soup=soup, confirm=cf), lbl))
        print()

    print("── 2. ЯАГААД — эрсдэл хэр өсдөг вэ ──")
    print("   Баталгаа хүлээхэд оролт стопоос ХОЛДОНО. Стоп хөдөлдөггүй.\n")
    print(f"   {'':<34}{'n':>6}{'медиан эрсдэл':>15}")
    print("   " + "─" * 56)
    for soup in ('wick', 'body'):
        for cf in ('none', 'model1'):
            a = run(soup=soup, confirm=cf, ret_risk=True)
            if len(a) < 25:
                continue
            nm = 'TS' if soup == 'wick' else 'TBS'
            print(f"   {nm + ' · ' + ('шууд' if cf == 'none' else 'баталгаатай'):<34}"
                  f"{len(a):>6}{np.median(a[:, 1]):>14.2f}$")
    print("\n   Эрсдэл өсөх тусам ижил хөдөлгөөн БАГА R өгнө.")

    print("\n── 3. Түвшин тогтоох цонх (K) ──\n")
    for K in (1, 3, 5, 10):
        print("   " + stat(run(soup='body', confirm='model1', K=K),
                           f'өмнөх {K} лаа'))

    print("\n── 4. Баталгааг хэр удаан хүлээх вэ ──\n")
    for w in (2, 4, 6, 12):
        print("   " + stat(run(soup='body', confirm='model1', wait=w),
                           f'{w} лааны дотор'))

    print("\n── 5. Хугацааны хүрээ ──\n")
    for tf in ('1h', '4h', '1D'):
        print("   " + stat(run(tf=tf, soup='body', confirm='model1'),
                           f'{tf} · TBS баталгаатай'))

    print("\n── 6. ДӨРВӨН ШАЛГУУР — TS + баталгаа (n=2544) ──")
    print("   TBS нь n=47 тул шалгах боломжгүй. Утга бүхий нь ЭНЭ.\n")
    for kw, lbl in ((dict(), 'бүгд'),
                    (dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО')):
        print("   " + stat(run(soup='wick', confirm='model1', **kw), lbl))
    print("\n   Урт ажиллаж, богино ажиллахгүй → алтны өсөх хандлага.")
    print("   2017-оос хойш алга болсон.\n")
    print("   Спредэд мэдрэг эсэх (стоп $14 тул тэсвэртэй байх ёстой):")
    for sp in (0.0, 0.3, 0.6, 1.5):
        print("   " + stat(run(soup='wick', confirm='model1', spread=sp),
                           f'спред ${sp}'))

    print("\n── 7. Target ──\n")
    for rr in (1.0, 2.0, 3.0):
        print("   " + stat(run(soup='body', confirm='model1', rr=rr),
                           f'TP 1:{rr:.0f}'))
