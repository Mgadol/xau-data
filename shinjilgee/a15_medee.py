"""15. Мэдээний цаг — үнийн өгөгдлөөс өөрөөс нь гаргана.

ЯАГААД ЭНЭ ЧИГЛЭЛ РҮҮ ОРСОН БЭ
  a1–a14 хүртэл үнийн ХЭЛБЭР ДҮРСийг л шалгасан — давалгаа, бүтэц,
  түвшин, цоорхой. Аль нь ч зардлыг даван гарсангүй. Тиймээс
  «алт яагаад хөдөлдөг вэ» гэсэн ГАДНЫ шалтгаан руу харах ээлж.

  Бодит хүү, доллар, инфляци зэрэг макро өгөгдөл энэ орчноос
  ТАТАГДАХГҮЙ (прокси хаалттай). Гэхдээ МЭДЭЭНИЙ ЦАГ нь хуанлиас
  бүрэн гардаг — гадны өгөгдөл огт шаардахгүй:

      NFP (ажил эрхлэлт)  сар бүрийн ЭХНИЙ БААСАН, 08:30 ET
      АНУ-ын статистик    ихэнх нь 08:30 ET = 15:30 брокерийн цаг
      FOMC                14:00 ET = 21:00 брокерийн цаг

  Брокерийн цаг = ET + 7.  Улаанбаатар = брокер + 5.
      15:30 брокер = 08:30 ET = УБ 20:30
      21:00 брокер = 14:00 ET = УБ 02:00

ЮУ ХЭМЖИХ ВЭ
  1. Хэлбэлзлийн ЦАГ — аль 5 минутын нүдэнд хамгийн их хөдөлдөг вэ.
     Энэ нь мэдээний цагийг өгөгдлөөс өөрөөс нь ИЛРҮҮЛНЭ.
  2. NFP өдөр бусад өдрөөс юугаараа ялгаатай вэ.
  3. NFP-ийн «эхлээд нэг тийш, дараа нь эргэх» гэдэг үнэн үү.
  4. Мэдээний цонхыг ХАСВАЛ өмнөх шинжилгээ сайжрах уу.

  Эхний хоёр нь ТОДОРХОЙЛОЛТ (арилжаа биш) — үүнийг мэдэх нь
  «хэзээ бүү ор» гэдэгт хэрэгтэй. Сүүлийн хоёр нь шалгалт.
"""
import numpy as np
import pandas as pd
from core import load, stat

d5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
IDX = d5.index
O, H, L, C = (d5['open'].values, d5['high'].values,
              d5['low'].values, d5['close'].values)
MIN = IDX.hour * 60 + IDX.minute
DAY = IDX.normalize()

D = pd.DataFrame({'day': DAY, 'm': MIN, 'o': O, 'h': H, 'l': L, 'c': C,
                  'dow': IDX.dayofweek, 'dom': IDX.day})
D['rng'] = D['h'] - D['l']
# Өдрийн дундаж мужаар хэвийн болгоно — 2005 ба 2025 оны алт харьцуулахын тулд
dref = D.groupby('day')['rng'].mean()
D['norm'] = D['rng'] / D['day'].map(dref)

# NFP = сарын ЭХНИЙ БААСАН.  Хуанлиас шууд гарна, гадны өгөгдөл хэрэггүй.
D['is_nfp'] = (D['dow'] == 4) & (D['dom'] <= 7)


def hhmm(m):
    return f"{m // 60:02d}:{m % 60:02d}"


if __name__ == '__main__':
    print("Мэдээний цагийг ҮНИЙН ӨГӨГДЛӨӨС өөрөөс нь илрүүлэх\n")

    print("── 1. ХЭЛБЭЛЗЛИЙН ЦАГ — хамгийн идэвхтэй 12 нүд ──")
    print("   Өдрийн дундаж мужийг 1.00 гэж авав.\n")
    v = D.groupby('m')['norm'].mean().sort_values(ascending=False)
    print(f"   {'брокер':<9}{'УБ':<9}{'ET':<9}{'хэлбэлзэл':>11}")
    print("   " + "─" * 40)
    for m, x in v.head(12).items():
        print(f"   {hhmm(m):<9}{hhmm((m + 300) % 1440):<9}"
              f"{hhmm((m - 420) % 1440):<9}{x:>10.2f}×")

    print("\n   Хамгийн тайван 5 нүд:")
    for m, x in v.tail(5).items():
        print(f"   {hhmm(m):<9}{hhmm((m + 300) % 1440):<9}"
              f"{hhmm((m - 420) % 1440):<9}{x:>10.2f}×")

    print("\n   → 15:30 брокер (08:30 ET, УБ 20:30) нь АНУ-ын статистикийн")
    print("     цаг. Өгөгдөл түүнийг өөрөө олж байна — таамаглаагүй.")

    print("\n\n── 2. NFP ӨДӨР (сарын эхний Баасан) ──\n")
    nfp = D[D['is_nfp']]
    oth = D[~D['is_nfp']]
    print(f"   NFP өдрийн тоо: {nfp['day'].nunique()}   бусад: {oth['day'].nunique()}\n")
    print(f"   {'цонх':<22}{'NFP':>9}{'бусад':>9}{'харьцаа':>10}")
    print("   " + "─" * 52)
    for a, b, lbl in ((15 * 60 + 30, 15 * 60 + 45, '15:30–15:45'),
                      (15 * 60 + 30, 16 * 60, '15:30–16:00'),
                      (16 * 60, 17 * 60, '16:00–17:00'),
                      (0, 15 * 60 + 30, 'мэдээний ӨМНӨ'),
                      (0, 24 * 60, 'бүх өдөр')):
        x = nfp[(nfp['m'] >= a) & (nfp['m'] < b)]['norm'].mean()
        y = oth[(oth['m'] >= a) & (oth['m'] < b)]['norm'].mean()
        print(f"   {lbl:<22}{x:>8.2f}×{y:>8.2f}×{x / y:>9.2f}×")

    print("\n\n── 3. NFP-ийн «эхлээд нэг тийш, дараа нь ЭРГЭХ» ──")
    print("   Түгээмэл ойлголт: эхний догшин хөдөлгөөн хуурамч, эргэнэ.")
    print("   Хэмжилт: 15:30–15:45-ийн чиглэл vs 15:45–21:00-ийн чиглэл.\n")
    rows = []
    for day, g in D[D['is_nfp']].groupby('day'):
        a = g[(g['m'] >= 15 * 60 + 30) & (g['m'] < 15 * 60 + 45)]
        b = g[(g['m'] >= 15 * 60 + 45) & (g['m'] < 21 * 60)]
        if len(a) < 3 or len(b) < 12:
            continue
        first = a['c'].iloc[-1] - a['o'].iloc[0]
        rest = b['c'].iloc[-1] - b['o'].iloc[0]
        rows.append(dict(day=day, first=first, rest=rest,
                         year=day.year,
                         atr=g['rng'].mean() * 12))
    N = pd.DataFrame(rows)
    N = N[N['atr'] > 0]
    same = (np.sign(N['first']) == np.sign(N['rest'])).mean() * 100
    cont = (N['rest'] * np.sign(N['first']) / N['atr'])
    se = cont.std() / np.sqrt(len(cont))
    print(f"   NFP өдөр: {len(N)}")
    print(f"   Эхний 15 мин ба дараагийн хэсэг ИЖИЛ чиглэлтэй: {same:.1f}%")
    print(f"   Эхний чиглэлийг дагавал: {cont.mean():>+.3f} ±{se:.3f}"
          f"{'  ✓' if abs(cont.mean()) > 2 * se else '  ✗'}")
    print("   (50% ба 0.000 бол мэдээлэл алга — эргэх ч үгүй, "
          "үргэлжлэх ч үгүй)")

    print("\n   Хугацаагаар:")
    for yl, yh, tag in ((2005, 2017, '2005–2016'), (2017, 2026, '2017–2025')):
        s = N[(N['year'] >= yl) & (N['year'] < yh)]
        if len(s) < 25:
            continue
        sm = (np.sign(s['first']) == np.sign(s['rest'])).mean() * 100
        c = s['rest'] * np.sign(s['first']) / s['atr']
        print(f"      {tag}  n={len(s):>3}  ижил {sm:>5.1f}%  "
              f"{c.mean():>+.3f} ±{c.std() / np.sqrt(len(c)):.3f}")

    print("\n\n── 4. Эхний хөдөлгөөний ХЭМЖЭЭ чухал уу ──")
    print("   Том догшин хөдөлгөөн илүү эргэдэг гэж үздэг.\n")
    N['sz'] = N['first'].abs() / N['atr']
    print(f"   {'':<26}{'n':>5}{'ижил %':>9}{'дараагийн':>11}")
    print("   " + "─" * 52)
    for lo, hi, lbl in ((0, 0.15, 'эхний хөдөлгөөн жижиг'),
                        (0.15, 0.35, 'дунд'),
                        (0.35, 99, 'том (>0.35 ATR)')):
        s = N[(N['sz'] >= lo) & (N['sz'] < hi)]
        if len(s) < 20:
            print(f"   {lbl:<26}{len(s):>5}  (цөөн)")
            continue
        sm = (np.sign(s['first']) == np.sign(s['rest'])).mean() * 100
        c = s['rest'] * np.sign(s['first']) / s['atr']
        print(f"   {lbl:<26}{len(s):>5}{sm:>8.1f}%{c.mean():>+10.3f} "
              f"±{c.std() / np.sqrt(len(c)):.3f}")

    print("\n\n── 5. ГАРАГААР ──")
    print("   Өдрийн өгөөжийг тухайн өдрийн МУЖААР хувааж хэвийн болгов.\n")
    dd = D.groupby('day').agg(dow=('dow', 'first'), o=('o', 'first'),
                              c=('c', 'last'), hi=('h', 'max'), lo=('l', 'min'))
    dd['span'] = dd['hi'] - dd['lo']
    # Маш нимгэн өдөр (амралт, хагас өдөр) хуваахад хязгааргүй гаргана
    dd = dd[dd['span'] > dd['span'].median() * 0.1]
    dd['ret'] = (dd['c'] - dd['o']) / dd['span']
    NM = ['Даваа', 'Мягмар', 'Лхагва', 'Пүрэв', 'Баасан']
    print(f"   {'гараг':<12}{'n':>6}{'өгөөж':>10}{'±SE':>9}")
    print("   " + "─" * 40)
    for k in range(5):
        s = dd[dd['dow'] == k]['ret']
        if len(s) < 25:
            continue
        se = s.std() / np.sqrt(len(s))
        print(f"   {NM[k]:<12}{len(s):>6}{s.mean():>+10.3f} ±{se:.3f}"
              f"{'  ✓' if abs(s.mean()) > 2 * se else ''}")

    print("\n\n── 6. МЭДЭЭНИЙ ЦОНХЫГ ХАСВАЛ САЙЖРАХ УУ ──")
    print("   Энэ л цорын ганц ҮЙЛДЭЛД хөрвөх шалгалт.")
    print("   a4/a5-ийн цэвэрлэгээг оролтын минутаар нь хуваая.\n")
    try:
        import a5_shinj as S
        F = S.collect()
        m = F['t'].dt.hour * 60 + F['t'].dt.minute
        print(f"   {'':<34}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
        print("   " + "─" * 66)
        news = (m >= 15 * 60 + 25) & (m < 16 * 60)
        print("   " + stat(F['R'].values, 'бүгд'))
        print("   " + stat(F[news]['R'].values, 'мэдээний цонхонд орсон'))
        print("   " + stat(F[~news]['R'].values, 'мэдээний цонхыг хассан'))
        late = (m >= 18 * 60)
        print("   " + stat(F[~news & ~late]['R'].values,
                           'мэдээ БА оройн цагийг хассан'))
    except Exception as e:
        print(f"   (a5-ийг ачаалж чадсангүй: {e})")
