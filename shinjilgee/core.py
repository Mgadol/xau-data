"""Нийтлэг хэрэгслүүд — бүх шинжилгээ эндээс эхэлнэ.

Өгөгдөл: ../XAU_1h_data.csv  ба  ../XAU_5m_data.csv
5 минутынх нь .rar дотор — эхлээд задлана:
    unrar x ../XAU_5m_data.rar ..
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.dirname(HERE)


def load(name='XAU_1h_data.csv', start=None, end=None):
    """CSV уншиж, огноогоор эрэмбэлж, индекс болгоно."""
    d = pd.read_csv(os.path.join(DATA, name), sep=';')
    d.columns = [c.strip().lower() for c in d.columns]
    d['date'] = pd.to_datetime(d['date'], format='%Y.%m.%d %H:%M')
    d = d.sort_values('date').set_index('date')
    if start: d = d[d.index >= start]
    if end:   d = d[d.index <= end]
    return d


def resample(d, rule):
    """Жижиг хугацаанаас том хугацаа үүсгэнэ (1ц → 4ц, өдөр, долоо хоног)."""
    if rule in ('1h', '5m'):
        return d
    return d.resample(rule).agg({'open': 'first', 'high': 'max', 'low': 'min',
                                 'close': 'last', 'volume': 'sum'}).dropna()


def zigzag(d, pct):
    """Хэлбэлзлийн эргэлтийн цэгүүд.  Буцаах: [(индекс, үнэ, чиглэл)]

    чиглэл: 1 = оргил, -1 = ёроол.
    Сүүл (high/low) ашиглана — жинхэнэ туйл тэнд байдаг.

    АНХААР: pct-ийг өөрчлөхөд бүх дүгнэлт өөрчлөгддөг. Нэг утгаар бус,
    хэд хэдэн утгаар шалгаж, үр дүн тогтвортой эсэхийг үргэлж хар.
    """
    hi, lo = d['high'].values, d['low'].values
    piv, dirn = [], 0
    ei, ep = 0, d['close'].values[0]
    for i in range(1, len(d)):
        if dirn >= 0:
            if hi[i] > ep or dirn == 0:
                if hi[i] > ep: ei, ep = i, hi[i]
            if lo[i] < ep * (1 - pct):
                piv.append((ei, ep, 1)); dirn = -1; ei, ep = i, lo[i]; continue
        if dirn <= 0:
            if lo[i] < ep or dirn == 0:
                if lo[i] < ep: ei, ep = i, lo[i]
            if hi[i] > ep * (1 + pct):
                piv.append((ei, ep, -1)); dirn = 1; ei, ep = i, hi[i]
    return piv


def confirm_index(d, pi, pv, pdir, pct):
    """Пивот ХЭДИЙД батлагдсан бэ — үнэ түүнээс pct хувь эргэсэн бар.

    Энэ функц ирээдүй харахаас хамгаална. Пивот үүссэн даруйдаа
    мэдэгддэггүй — эргэлт болсны дараа л мэдэгддэг. Тестэд ҮРГЭЛЖ
    энэ индексээс хойш ажиллана.
    """
    hi, lo = d['high'].values, d['low'].values
    for i in range(pi + 1, len(d)):
        if pdir == 1 and lo[i] < pv * (1 - pct): return i
        if pdir == -1 and hi[i] > pv * (1 + pct): return i
    return None


def bar_len(tf):
    """Нэг барын үргэлжлэх хугацаа. Баталгаа нь бар ХААГДАХАД мэдэгдэнэ.

    Энэ жижиг зүйл маш том алдаа үүсгэсэн. Эхэндээ би 5 минутын
    хайлтыг баталгааны бар НЭЭГДЭХ мөчөөс эхлүүлж байсан. Гэтэл тэр
    үед баталгаа хараахан болоогүй — 4 цагийн бар хаагдаж байж л
    мэдэгддэг. Улмаас эхний 48 ширхэг 5м бар нь ИРЭЭДҮЙН мэдээлэл
    ашигласан болж, «шинэ түвшин хамгийн хүчтэй» гэсэн ХУДАЛ олдвор
    гаргаж байв (+0.790R). Залруулсны дараа тэр алга болсон.
    """
    return pd.Timedelta({'4h': '4h', '1h': '1h', '1D': '1D',
                         '1W': '7D', '5m': '5min'}.get(tf, tf))


def stat(R, label='', rr_hint=None):
    """R-ийн жагсаалтаас статистик. ✓ = тэгээс 2 стандарт алдаагаар дээш."""
    R = np.asarray(R, float)
    R = R[~np.isnan(R)]
    if len(R) < 25:
        return f"{label:<30}{len(R):>6}  (цөөн)"
    se = R.std() / np.sqrt(len(R))
    ok = '  ✓' if R.mean() > 2 * se else '  ✗'
    return (f"{label:<30}{len(R):>6} {(R > 0).mean() * 100:>6.1f}% "
            f"{R.mean():>+8.3f}R ±{se:.3f}{ok}")
