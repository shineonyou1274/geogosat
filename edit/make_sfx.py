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
