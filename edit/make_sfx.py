"""코드로 만든 오리지널 효과음과 파라파라용 유로비트 (저작권 걱정 없음)."""
import numpy as np, wave, os
SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx")

def save(name, x):
    x = np.clip(x / (np.max(np.abs(x)) + 1e-9) * 0.9, -1, 1)
    st = np.stack([x, x], 1)
    with wave.open(f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

t = lambda d: np.arange(int(SR * d)) / SR
env = lambda d, k: np.exp(-t(d) * k)

# 시계 초침: 1초마다 '틱'
tick = np.sin(2 * np.pi * 3200 * t(0.03)) * env(0.03, 220) + np.random.randn(len(t(0.03))) * 0.3 * env(0.03, 400)
clock = np.zeros(int(SR * 13))
for s in range(13):
    i = int(s * SR); clock[i:i + len(tick)] += tick * (1 if s % 2 == 0 else 0.7)
save("clock", clock)

# 전기 스파크: 지직거리는 잡음 + 위로 솟는 충전음
d = 1.6; n = np.random.randn(len(t(d)))
crackle = n * (np.random.rand(len(n)) > 0.85) * env(d, 2.5)
chirp = np.sin(2 * np.pi * np.cumsum(300 + 1800 * t(d) / d) / SR) * 0.4 * (t(d) > 0.5)
save("spark", crackle + chirp)

# 유로비트 155bpm, 8마디 (약 12.4초): 킥 4박, 오프비트 하이햇, 옥타브 베이스, 톱니 리드
bpm = 155; beat = 60 / bpm; bars = 8; L = int(SR * beat * 4 * bars)
mix = np.zeros(L)
def place(sig, sec, g=1.0):
    i = int(sec * SR); j = min(L, i + len(sig)); mix[i:j] += sig[: j - i] * g
kick = np.sin(2 * np.pi * np.cumsum(50 + 120 * np.exp(-t(0.25) * 30)) / SR) * env(0.25, 9)
hat = np.random.randn(len(t(0.05))) * env(0.05, 90)
saw = lambda f, d: (2 * ((f * t(d)) % 1) - 1)
prog = [57, 53, 55, 52]  # Am F G Em (MIDI 근음)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
for b in range(bars * 4):
    s = b * beat
    place(kick, s, 1.0); place(hat, s + beat / 2, 0.35)
    root = prog[(b // 4) % 4] - 24
    for k in range(2):
        f = mid(root + 12 * k); place(saw(f, beat / 2) * env(beat / 2, 6), s + k * beat / 2, 0.35)
arp = [0, 3, 7, 12, 7, 3, 7, 10]
for b in range(bars * 4 * 2):
    s = b * beat / 2; root = prog[(b // 8) % 4] + 12
    f = mid(root + arp[b % 8]); d = beat / 2
    v = saw(f, d) + saw(f * 1.006, d) + saw(f * 0.994, d)
    place(v * env(d, 4) * 0.25, s, 0.5)
save("eurobeat", np.tanh(mix * 1.2))
print("ok")

# ---- v5 추가 효과음 ----
def bell(f, d, k=3):
    tt = t(d); return sum(np.sin(2*np.pi*f*m*tt)*np.exp(-tt*k*m)/m for m in (1, 2.01, 3.03))
_c = bell(1568, 1.2); _d = np.pad(bell(2093, 1.0), (int(SR*0.12), 0)); _c[:len(_d)] += _d[:len(_c)]; save("chime", _c)
nz = np.random.randn(int(SR*0.5))
sw = np.convolve(nz, np.ones(30)/30, "same") * np.sin(np.pi*np.linspace(0, 1, len(nz)))**2
save("whoosh", sw)
tt = t(0.6); save("impact", np.sin(2*np.pi*np.cumsum(90*np.exp(-tt*6)+40)/SR)*np.exp(-tt*5) + np.random.randn(len(tt))*np.exp(-tt*30)*0.6)
tt = t(0.45); sc = np.random.randn(len(tt)) * np.exp(-tt*4); sc *= np.sin(2*np.pi*np.cumsum(30+400*(1-tt/0.45))/SR) > 0
save("scratch", sc)
notes = [523, 659, 784, 1047, 1319]
save("item", np.concatenate([np.sin(2*np.pi*f*t(0.09))*env(0.09, 15) for f in notes] + [bell(1568, 0.8, 4)]))
tt = t(1.2); save("riser", np.sin(2*np.pi*np.cumsum(200+1400*(tt/1.2)**2)/SR)*0.5*(tt/1.2))
save("ding", bell(1760, 0.9, 5))
save("quest", np.concatenate([np.sin(2*np.pi*f*t(0.12))*env(0.12, 12) for f in (392, 523, 784)] + [bell(1047, 0.6)]))
# 가벼운 피치카토 BGM (100bpm, 16마디)
bpmb = 100; bt = 60/bpmb; L2 = int(SR*bt*4*16); bgm = np.zeros(L2)
scale_ = [0, 2, 4, 7, 9, 12, 9, 7]
for b in range(16*4*2):
    s = b*bt/2; f = mid(60 + scale_[(b*3) % 8] + (0 if (b//16) % 2 == 0 else -5))
    i = int(s*SR); sig = np.sin(2*np.pi*f*t(0.25))*env(0.25, 14); j = min(L2, i+len(sig)); bgm[i:j] += sig[:j-i]*0.5
    if b % 4 == 0:
        sig = np.sin(2*np.pi*mid(36+scale_[(b//8) % 4])*t(0.5))*env(0.5, 5); j = min(L2, i+len(sig)); bgm[i:j] += sig[:j-i]*0.6
save("bgm_pluck", bgm)
print("v5 sfx ok")
