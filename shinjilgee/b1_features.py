"""b1. Өдрийн шинж чанарын багц — GOLD_Features загвараар.

Гаднаас ирсэн `GOLD_Features_Sample.csv` (30 мөр, 2020-01-02 … 2020-02-13)
нь 90 баганатай ч зөвхөн ДЭЭЖ байсан. Түүний БҮТЦИЙГ баримтлан, манай
өөрийн XAU 1 цагийн өгөгдлөөс (2004 → 2026) бүтэн хугацааны багцыг энд
угсарна.

Томьёог таамаглаагүй — дээжийн өөрийнх нь `price_close` баганаар тулгаж
баталгаажуулав. Яг таарсан нь:

    ema_20, ema_20_dist, bollinger_pos, bollinger_bw, sma_5, sma_20,
    sma_5_dist, roc_5/10/20, return_1/3/5/10/20d, log_return_1d,
    dist_high_10/20d, dist_low_10/20d, vol_5/10/20d, streak

RSI ба MACD нь дээж дээр зөрсөн боловч энэ нь АЛДАА БИШ: дээж 2020 оны
1-р сарын 2-оос эхэлдэг ч тэдний жинхэнэ цуваа түүнээс өмнө эхэлсэн тул
экспоненциал дулаацуулалт нь өөр байрнаас эхэлсэн. Энд бид 2004 оноос
бодож, шаардлагатай хугацаагаар дулаацуулна.

Дээжээс СЭРГЭЭГДЭЭГҮЙ гурван багана (утга нь хэтэрхий цөөн байсан) —
эдгээрийг ЭНД тодорхойлов, тэдний утгатай яг ижил гэж бүү ойлгоорой:

    tech_momentum_quality — roc_10 / (vol_10d · √10). Тэдний багантай
                            0.98 хамааралтай ч ЯГ ижил биш.
    tech_bollinger_squeeze — зурвасын өргөн сүүлийн 120 хоногийн доод
                            20 хувьд орвол 1.
    vol_of_vol_20d / vol_regime — хэлбэлзлийн хэлбэлзэл ба түүний гурван
                            дэглэм (0 нам / 1 дунд / 2 өндөр).

Гаднын эх сурвалж шаардсан 41 багана (sent_*, news_*, macro_*, mkt_*,
options_*) энд БАЙХГҮЙ — тэдгээрийг үнийн өгөгдлөөс гаргах боломжгүй.

    python3 b1_features.py [--out GOLD_Features_2020_2026.csv]
"""
import argparse
import os
import numpy as np
import pandas as pd
from core import load, DATA

# Дээжийн хугацаа. Өмнө нь 2019 оноос дулаацуулна — 20 хоногийн цонх,
# MACD-ийн 26+9 бар зэрэг нь эхний мөрүүдээ хоосон орхихгүйн тулд.
WARMUP = '2019-06-01'
# Өдрийн хил — доорх daily()-ийн тайлбарт хэмжилтийн үндэслэл бий
DAY_CLOSE_HOUR = 18
FLAT = 0.30      # |өгөөж| энэ хувиас бага бол FLAT (дээжээс хэмжсэн босго)


def daily(name='XAU_1h_data.csv', close_hour=DAY_CLOSE_HOUR):
    """1 цагийн барнаас ӨДРИЙН бар.

    `close_hour` нь ӨДРИЙН ХИЛ — алт бараг 24 цаг арилждаг тул «өдрийн
    хаалт» гэдэг нь ТОХИРОЛЦОО, өгөгдөлд бичээстэй байдаггүй. Түүнийг
    таамаглалгүйгээр ХЭМЖИВ: гаднаас ирсэн дээжийн 30 өдрийн үнэтэй
    тулгаж, хилийг 0-23 цагаар гүйлгэн шалгахад —

        шөнө дунд : үнийн зөрүү $2.62,  чиглэл таарсан 20/30
        17:00     : $2.66,             27/30
        18:00     : $1.27,             29/30   ← сонгосон
        19:00     : $1.32,             29/30

    18:00 нь Нью-Йоркийн 17:00 хаалт (серверийн цагийн зөрүү +1). Тэдний
    эх сурвалж тэгж тасалдаг нь эндээс батлагдав.

    Энэ сонголт ЧУХАЛ: хил нэг цагаар хөдлөхөд оройн том хөдөлгөөн хөрш
    өдөр рүү шилжиж, 1 хоногийн чиглэлийн шошго хөрвөдөг. Өөрийн арилжаа
    өөр цагт хаагддаг бол `--close-hour`-оор солино.
    """
    h = load(name)
    if close_hour is None:
        key = h.index.normalize()
    else:
        # close_hour-аас ХОЙШХИ бар нь ДАРААГИЙН арилжааны өдөрт тооцогдоно.
        # Индексийг шилжүүлж resample хийвэл амралтын өдрийн бар тусдаа
        # хоног болж хуваагдан, илүү мөр үүсгэдэг — тиймээс шууд бүлэглэнэ.
        key = h.index.normalize() + pd.to_timedelta(
            (h.index.hour > close_hour).astype(int), unit='D')
        # Баасан гарагийн оройн бар (зах зээл хаагдахын өмнөх) ийнхүү
        # БЯМБА гараг руу шилжинэ. Тэр нь тусдаа хоног болвол 7 хоног
        # бүрд нэг хиймэл мөр нэмэгдэнэ — дараагийн ДАВАА руу нийлүүлнэ.
        key = pd.DatetimeIndex(key)
        wd = key.dayofweek
        key = key + pd.to_timedelta(np.where(wd == 5, 2, np.where(wd == 6, 1, 0)),
                                    unit='D')
    d = h.groupby(key).agg(open=('open', 'first'), high=('high', 'max'),
                           low=('low', 'min'), close=('close', 'last'),
                           volume=('volume', 'sum'))
    d.index.name = 'date'
    return d.dropna(subset=['close'])


def rsi(c, n=14):
    delta = c.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def adx(h, l, c, n=14):
    """Wilder-ийн ADX. Дээжид байсан ч сэргээх боломжгүй байсан (High/Low
    нь дээжид ороогүй) — энд манай OHLC-оос стандарт аргаар бодов."""
    up, dn = h.diff(), -l.diff()
    plus = np.where((up > dn) & (up > 0), up, 0.0)
    minus = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()],
                   axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / n, adjust=False).mean()
    pdi = 100 * pd.Series(plus, index=h.index).ewm(alpha=1/n, adjust=False).mean() / atr
    mdi = 100 * pd.Series(minus, index=h.index).ewm(alpha=1/n, adjust=False).mean() / atr
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(alpha=1 / n, adjust=False).mean()


def build(d):
    """Өдрийн OHLC → шинж чанарын хүснэгт."""
    c, hi, lo = d.close, d.high, d.low
    r = c.pct_change() * 100
    f = pd.DataFrame(index=d.index)

    f['year'] = d.index.year
    f['day_of_week'] = d.index.day_name()
    f['price_close'] = c

    # ── Үнэ ──────────────────────────────────────────────────────────
    for k in (1, 3, 5, 10, 20):
        f[f'price_return_{k}d'] = (c / c.shift(k) - 1) * 100
    f['price_log_return_1d'] = np.log(c / c.shift(1))
    for k in (10, 20):
        f[f'price_dist_high_{k}d'] = (c / c.rolling(k).max() - 1) * 100
        f[f'price_dist_low_{k}d'] = (c / c.rolling(k).min() - 1) * 100

    # ── Техник ───────────────────────────────────────────────────────
    f['tech_rsi_14'] = rsi(c)
    for k in (5, 20):
        sma = c.rolling(k).mean()
        f[f'tech_sma_{k}'] = sma
        f[f'tech_sma_{k}_dist'] = (c / sma - 1) * 100
    e20 = c.ewm(span=20, adjust=False).mean()
    f['tech_ema_20'] = e20
    f['tech_ema_20_dist'] = (c / e20 - 1) * 100

    s20, sd = c.rolling(20).mean(), c.rolling(20).std()
    f['tech_bollinger_pos'] = (c - (s20 - 2 * sd)) / (4 * sd)
    bw = 4 * sd / s20 * 100
    f['tech_bollinger_bw'] = bw
    # Шахалт: зурвас сүүлийн 120 хоногийн доод 20 хувьд
    f['tech_bollinger_squeeze'] = (
        bw <= bw.rolling(120, min_periods=40).quantile(.20)).astype(float)

    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    sig = macd.ewm(span=9, adjust=False).mean()
    f['tech_macd'], f['tech_macd_signal'], f['tech_macd_hist'] = macd, sig, macd - sig
    f['tech_adx'] = adx(hi, lo, c)
    for k in (5, 10, 20):
        f[f'tech_roc_{k}'] = (c / c.shift(k) - 1) * 100
        f[f'tech_vol_{k}d'] = r.rolling(k).std()

    sgn = np.sign(r)
    f['tech_streak'] = (sgn.groupby((sgn != sgn.shift()).cumsum()).cumcount() + 1) * sgn
    # Моментийн ЧАНАР: нэгж эрсдэлд ногдох хөдөлгөөн. Дээжийнхтэй 0.98
    # хамааралтай ч ЯГ ижил биш — тэдний томьёо сэргээгдээгүй.
    f['tech_momentum_quality'] = f['tech_roc_10'] / (f['tech_vol_10d'] * np.sqrt(10))

    # ── Хэлбэлзлийн дэглэм ───────────────────────────────────────────
    vv = f['tech_vol_20d'].rolling(20).std()
    f['vol_of_vol_20d'] = vv
    q = f['tech_vol_20d'].rolling(250, min_periods=60)
    f['vol_regime'] = np.select(
        [f['tech_vol_20d'] <= q.quantile(.33), f['tech_vol_20d'] >= q.quantile(.67)],
        [0.0, 2.0], default=1.0)
    f.loc[f['tech_vol_20d'].isna(), 'vol_regime'] = np.nan

    # ── Шошго: ИРЭЭДҮЙ рүү (t+k), энэ нь ЗӨВ — таамаглах зүйл ────────
    for k in (1, 3, 5):
        fut = (c.shift(-k) / c - 1) * 100
        f[f'label_return_{k}d'] = fut
        f[f'label_dir_{k}d'] = np.where(fut.isna(), None,
                                        np.where(fut.abs() < FLAT, 'FLAT',
                                                 np.where(fut > 0, 'UP', 'DOWN')))
    f['label_flat_1d'] = (f['label_dir_1d'] == 'FLAT').astype(float)
    f.loc[f['label_return_1d'].isna(), 'label_flat_1d'] = np.nan
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', default='2020-01-01')
    ap.add_argument('--end', default=None)
    ap.add_argument('--out', default='GOLD_Features_2020_2026.csv')
    ap.add_argument('--close-hour', type=int, default=DAY_CLOSE_HOUR,
                    help=f'Өдрийн хил 0-23 (анхдагч {DAY_CLOSE_HOUR}). '
                         'Шөнө дунд бол -1')
    a = ap.parse_args()

    d = daily(close_hour=None if a.close_hour < 0 else a.close_hour)
    print(f'Өдрийн бар: {len(d):,}   {d.index.min().date()} → {d.index.max().date()}')
    f = build(d[d.index >= WARMUP])
    out = f[f.index >= a.start]
    if a.end:
        out = out[out.index <= a.end]
    out = out.reset_index().rename(columns={'date': 'date'})
    out['date'] = out['date'].dt.strftime('%Y-%m-%d')

    path = os.path.join(DATA, a.out)
    out.to_csv(path, index=False)
    print(f'\n{a.out}: {len(out):,} мөр × {out.shape[1]} багана')
    print(f'  {out.date.iloc[0]} → {out.date.iloc[-1]}')
    empty = [c for c in out.columns if out[c].isna().all()]
    print(f'  бүрэн хоосон багана: {len(empty)} {empty}')
    nans = out.isna().sum()
    print(f'  цоорхойтой багана  : {int((nans > 0).sum())}'
          f'   хамгийн их дутуу: {int(nans.max())} мөр')
    print(f'\n  шошгын тархалт (1 хоног):')
    print('   ', out.label_dir_1d.value_counts(dropna=False).to_dict())


if __name__ == '__main__':
    main()
