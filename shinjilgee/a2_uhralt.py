"""2. Ухралт дээрх оролт — ШУУД орох vs БАТАЛГАА хүлээх.

Энэ бол бүх шинжилгээний хамгийн том олдвор:
    шууд орох   −0.299R
    баталгаатай +0.081R      ← 0.38R-ийн ялгаа

«Баталгаа» гэдэг нь: түвшинд хүрмэгц ордоггүй, тэр түвшнээс ДЭЭШ
бар хаагдтал хүлээдэг. Хоцорч ордог ч, унаж яваа хөдөлгөөнд
баригддаггүй.
"""
import numpy as np
from core import load, resample, zigzag, confirm_index, stat

d = resample(load(start='2005-01-01', end='2025-09-12'), '4h')
hi, lo, cl = d['high'].values, d['low'].values, d['close'].values

def test(mode, r, k, pct=0.01, maxbars=250, spread=0.0):
    """mode: 'shuud' = түвшинд хүрмэгц | 'batalgaa' = дээш хаагдтал хүлээнэ"""
    piv = zigzag(d, pct); out = []
    for j in range(1, len(piv)):
        (ai,av,ad), (bi,bv,bd) = piv[j-1], piv[j]
        if ad == bd: continue
        up = bd == 1; leg = abs(bv-av)
        ci = confirm_index(d, bi, bv, bd, pct)
        if ci is None or leg <= 0: continue
        L = bv - r*leg if up else bv + r*leg      # оролтын түвшин
        stop = av                                  # Эллиотын 1-р дүрэм эвдрэх цэг
        tgt  = bv + k*leg if up else bv - k*leg
        entry = ei = None; touched = False; dead = False
        for i in range(ci, min(ci+maxbars, len(d))):
            if mode == 'shuud':
                # Стоп нь оролтоос цаана тул үнэ ЗААВАЛ оролтоор дайрна
                if (up and lo[i] <= L) or ((not up) and hi[i] >= L):
                    entry, ei = L, i; break
            else:
                if (up and lo[i] <= stop) or ((not up) and hi[i] >= stop):
                    dead = True; break            # бүтэц эвдэрсэн — арилжаа байхгүй
                if (up and lo[i] <= L) or ((not up) and hi[i] >= L): touched = True
                if touched and ((up and cl[i] > L) or ((not up) and cl[i] < L)):
                    entry, ei = cl[i], i; break
        if entry is None or dead: continue
        e = entry + spread if up else entry - spread
        risk, rew = abs(e-stop), abs(tgt-e)
        if risk <= 0 or rew <= 0: continue
        # Оролтын бар дотор стоп ч хүрсэн бол алдагдал (дарааллыг мэдэх аргагүй)
        if mode == 'shuud' and ((up and lo[ei] <= stop) or ((not up) and hi[ei] >= stop)):
            out.append(-1.0); continue
        R = None
        for i in range(ei+1, min(ci+maxbars, len(d))):
            if up:
                if lo[i] <= stop: R = -1.0; break
                if hi[i] >= tgt:  R = rew/risk; break
            else:
                if hi[i] >= stop: R = -1.0; break
                if lo[i] <= tgt:  R = rew/risk; break
        out.append(R if R is not None else 0.0)
    return out

if __name__ == '__main__':
    print("4 цаг · ZigZag 1% · Стоп = 1-р давалгааны эхлэл · 2005–2025\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─"*62)
    for k in (0.618, 1.618):
        print(f"   ── Target = B + {k}×(B−A) ──")
        for r in (0.5, 0.618, 0.786):
            print("   " + stat(test('shuud',    r, k), f"оролт {r} · шууд"))
            print("   " + stat(test('batalgaa', r, k), f"оролт {r} · БАТАЛГААТАЙ"))
        print()
