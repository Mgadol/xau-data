"""3. Нээлтийн мужийн эвдрэл (ORB) — Нью-Йоркийн нээлт.

Нээлтийн муж: 16:30–16:45 брокерийн цаг = 21:30–21:45 Улаанбаатар
                                         = 09:30–09:45 Нью-Йорк

Үр дүн: давуу талгүй.

    TP 1:1 · спредгүй    3112   48.9%   −0.020R ±0.017
    TP 1:2 · спредгүй    3112   38.0%   +0.003R ±0.023
    TP 1:3 · спредгүй    3112   35.1%   +0.015R ±0.026
    TP 1:3 · спред $0.3  3112   32.9%   −0.095R ±0.024

Спредгүй ч тэг. Спред $0.3 нэмэхэд тодорхой сөрөг — ORB-ийн стоп
нарийн (нээлтийн 15 минутын муж) тул спред харьцангуй их иддэг.
"""
import numpy as np, pandas as pd
from core import load, resample, zigzag, confirm_index

def trend4h(pct=0.01):
    """4 цагийн Dow бүтэц. 16:45-аас өмнө хаагдсан баруудаар л тооцно."""
    f = resample(load(start='2004-01-01'), '4h')
    piv = zigzag(f, pct); tr = pd.Series(0, index=f.index); His=[]; Los=[]
    for (pi,pv,pd_) in piv:
        (His if pd_==1 else Los).append(pv)
        if len(His)>=2 and len(Los)>=2:
            up = His[-1]>His[-2] and Los[-1]>Los[-2]
            dn = His[-1]<His[-2] and Los[-1]<Los[-2]
            tr.iloc[pi:] = 1 if up else (-1 if dn else 0)
    s = tr.copy(); s.index = s.index + pd.Timedelta(hours=4)   # хаагдах мөч
    return s.sort_index()

def run(rr=3.0, cut='23:00', spread=0.0):
    d5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12').reset_index()
    d5['day']=d5['date'].dt.date; d5['t']=d5['date'].dt.strftime('%H:%M')
    trs = trend4h(); out=[]
    for day, g in d5.groupby('day', sort=True):
        g = g.reset_index(drop=True)
        orb = g[g['t'].isin(['16:30','16:35','16:40'])]
        if len(orb)!=3: continue
        hi_, lo_ = orb['high'].max(), orb['low'].min()
        if hi_<=lo_: continue
        co = pd.Timestamp(day)+pd.Timedelta(hours=16,minutes=45)
        pv = trs[trs.index<=co]
        t = int(pv.iloc[-1]) if len(pv) else 0
        if t==0: continue
        a = g[(g['t']>'16:40')&(g['t']<=cut)]
        if a.empty: continue
        H,L,C = a['high'].values, a['low'].values, a['close'].values
        up = t==1
        for i in range(len(a)):
            e = hi_ if up else lo_
            if not (H[i]>=e if up else L[i]<=e): continue
            e = e+spread if up else e-spread
            s = lo_ if up else hi_
            risk = abs(e-s)
            if risk<=0: break
            tp = e+rr*risk if up else e-rr*risk
            if (up and L[i]<=s) or ((not up) and H[i]>=s):
                out.append(-1.0); break
            R=None
            for j in range(i+1,len(a)):
                if up:
                    if L[j]<=s: R=-1.0; break
                    if H[j]>=tp: R=rr; break
                else:
                    if H[j]>=s: R=-1.0; break
                    if L[j]<=tp: R=rr; break
            out.append(R if R is not None else ((C[-1]-e) if up else (e-C[-1]))/risk)
            break
    return np.array(out)

if __name__ == '__main__':
    from core import stat
    print("ORB · 4 цагийн чиг хандлагын дагуу · 2005–2025\n")
    for rr in (1.0, 2.0, 3.0):
        print("   " + stat(run(rr), f"TP 1:{rr:.0f} · спредгүй"))
    print()
    print("   " + stat(run(3.0, spread=0.3), "TP 1:3 · спред $0.3"))
