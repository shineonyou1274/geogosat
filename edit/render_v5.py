"""거고 74기 수능 응원 영상 v5 렌더러.

컷은 0.5~1.5초 단위로 바뀌고, 모든 컷에 카메라 움직임(밀기, 당기기, 펀치, 흔들림)을 준다.
자막과 움직이는 글자(키네틱 타이포), 게임 UI, 불꽃 게이지, 폴라로이드 사진을 프레임마다 그린다.

사용법: python3 render_v5.py <노래.wav> <1080p 클립 폴더> <실제 짤 폴더> <사진 폴더> <출력 폴더>
"""
import math
import os
import random
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

SONG, HD, REAL, PHOTO, OUT = sys.argv[1:6]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K1, K2, KV = f"{ROOT}/keyframes/part1/", f"{ROOT}/keyframes/part2/", f"{ROOT}/keyframes/v2/"
SCH = f"{ROOT}/school/"
VO = f"{ROOT}/voice/v5/final/"
SFX = f"{ROOT}/edit/sfx/"
FONT = f"{ROOT}/edit/fonts/BlackHanSans-Regular.ttf"
W, H, FPS = 1920, 1080, 24
os.makedirs(OUT, exist_ok=True)

GOLD, RED, BLUE, GREEN, PINK, WHITE = (242, 165, 65), (229, 72, 77), (110, 180, 255), (61, 220, 132), (255, 105, 180), (255, 255, 255)

P = {  # 학생 사진
    "p01": "0a3850cc", "p02": "54680b5d", "p03": "4590df0d", "p04": "2a3f03fa", "p05": "58fde188",
    "p06": "30db9161", "p07": "c1679f4d", "p08": "e7268ac0", "p09": "f474d317", "p10": "23f407c4",
    "p11": "ae2dea64", "p12": "46525f61", "p13": "bfbc0a85", "p14": "b08ddb14",
}


def ph(k):
    return f"{PHOTO}/{P[k]}-image.jpg"


# ---------------------------------------------------------------- 시간표
SHOTS = []   # (start, kind, src, opts)
OV = []      # 겹쳐 그릴 요소
AU = []      # (file, at, vol, maxdur)


def shot(t, kind, src, **o):
    SHOTS.append((t, kind, src, o))


def ov(t0, t1, kind, **o):
    OV.append(dict(t0=t0, t1=t1, kind=kind, **o))


def au(f, at, vol=1.0, maxd=None):
    AU.append((f, at, vol, maxd))


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


# ===== 1부 =====
au(SFX + "clock.wav", 0.0, 0.35, 9.4)
au(VO + "S.wav", 0.6)
shot(0.0, "vid", "1-1", s=0.0, m="push", tint="blue")
shot(1.1, "img", K1 + "1-2.png", m="punch", tint="blue")
shot(1.7, "img", KV + "1-3.png", m="push", tint="blue")
shot(2.9, "vid", "1-1", s=2.0, m="panr", tint="blue")
shot(3.8, "img", KV + "1-3.png", m="pull", focus=(0.5, 0.6), tint="blue")
shot(4.6, "vid", "1-1", s=3.6, m="push", tint="blue")
shot(5.6, "img", K2 + "S-04.png", m="push", tint="blue")
shot(6.6, "img", KV + "1-3.png", m="punch", focus=(0.5, 0.55), tint="blue")
ov(0.6, 8.7, "gauge", v0=0.01, v1=0.01, label="멘탈 잔량", blink=True)
ov(0.6, 2.8, "big", text="멘탈 잔량 1%", color=RED, y=0.45, size=150)
ov(3.4, 5.9, "sub", text="수능 한파보다 무서운 건...")
ov(6.0, 8.6, "sub", text="자꾸 [얼어붙는] 내 마음이다.", hl=BLUE)

shot(8.7, "real", "R1_tteollimnida", m="none")
ov(8.7, 9.7, "label", text="실제 상황 (최강록 셰프)")

au(SFX + "chime.wav", 9.7, 0.7)
au(SFX + "bgm_pluck.wav", 9.7, 0.16, 84.3 - 9.7)
shot(9.7, "vid", "1-4", s=1.2, m="push", flash=True)
ov(10.0, 11.3, "tag", text="조림 셰프 등장", sub="거고 교사 | 약불 전문")

C1 = 11.4
au(VO + "C1.wav", C1)
shot(11.3, "vid", "1-5", s=0.0, m="push")
shot(12.5, "img", KV + "1-5.png", m="punch", focus=(0.5, 0.35))
shot(13.6, "img", K1 + "1-9.png", m="push", focus=(0.55, 0.35))
shot(14.9, "vid", "1-5", s=3.0, m="pull")
shot(15.7, "vid", "1-4", s=3.6, m="push")
shot(16.55, "img", KV + "1-5.png", m="slam", focus=(0.5, 0.3), bw=True, flash=True)
ov(C1, C1 + 0.95, "sub", text="오늘 요리는요...")
ov(C1 + 0.96, C1 + 4.2, "big", text="거고 74기 수능", color=WHITE, y=0.4, size=130)
ov(C1 + 4.34, C1 + 5.1, "sub", text="근데 이제...")
ov(C1 + 5.18, 19.4, "big", text="만점을 곁들인.", color=GOLD, y=0.45, size=190, slam=True)
au(SFX + "impact.wav", C1 + 5.18, 0.9)

C2 = 19.6
au(VO + "C2.wav", C2)
shot(19.4, "img", K1 + "1-6.png", m="push")
shot(20.6, "img", KV + "1-3.png", m="pull", tint="blue")
shot(21.6, "vid", "1-5", s=1.5, m="push")
shot(22.6, "img", KV + "1-8.png", m="none", focus=(0.5, 0.4), zoom=1.25, tint="blue", still=True)
shot(23.6, "img", K1 + "1-9.png", m="pull", focus=(0.55, 0.35))
shot(24.6, "img", K1 + "1-6.png", m="punch", focus=(0.6, 0.6))
shot(25.8, "img", KV + "1-7.png", m="push")
shot(27.0, "vid", "1-7", s=0.0, m="push")
shot(28.4, "img", K1 + "1-6.png", m="slam", focus=(0.62, 0.62), glow=True)
ov(C2, C2 + 2.6, "sub", text="재료가 얼어 있으면요...")
ov(C2 + 2.7, C2 + 6.0, "sub", text="레시피가 아무리 좋아도... 맛이 안 나요.")
ov(C2 + 6.1, C2 + 8.7, "sub", text="일단 이걸로...")
ov(C2 + 8.8, C2 + 10.3, "sub", text="마음부터 [데우세요].", hl=GOLD)
ov(28.6, 31.6, "item", title="전설 아이템 획득!", name="불안 해방 핫팩",
   desc="효과: 얼어붙은 손과 마음을 녹임 | 멘탈 +99%")
au(SFX + "item.wav", 28.6, 0.8)

shot(29.8, "vid", "1-7", s=2.3, m="shake", flash=True)
au(SFX + "spark.wav", 29.9, 0.9)
au(SFX + "riser.wav", 30.2, 0.6)
ov(29.8, 32.4, "gauge", v0=0.01, v1=1.0, a0=30.2, a1=31.4, label="멘탈 잔량")
ov(31.4, 32.4, "big", text="약불 점화!", color=GOLD, y=0.62, size=120, slam=True)
au(SFX + "ding.wav", 31.4, 0.7)
shot(32.4, "img", KV + "1-8.png", m="punch", focus=(0.5, 0.35))
ov(32.4, 33.3, "big", text="멘탈 100%", color=GREEN, y=0.15, size=110)

C3 = 33.4
au(VO + "C3.wav", C3)
shot(33.3, "img", K1 + "1-9.png", m="push", focus=(0.55, 0.35))
shot(34.4, "img", KV + "1-5.png", m="panl")
shot(35.5, "img", KV + "1-3.png", m="push", tint="blue")
shot(36.35, "img", K2 + "S-04.png", m="shake", tint="red", flash=True)
shot(37.3, "vid", "S-01", s=0.4, m="push", tint="red")
shot(38.6, "img", KV + "S-12.png", m="push", focus=(0.75, 0.6))
shot(40.2, "img", K1 + "1-9.png", m="pull", focus=(0.55, 0.35))
shot(41.4, "vid", "S-01", s=2.4, m="push")
shot(42.6, "img", K2 + "S-18.png", m="push")
ov(C3, C3 + 2.9, "sub", text="수험생은요...")
ov(C3 + 2.98, C3 + 5.6, "big", text="불안이라는 센 불", color=RED, y=0.42, size=150, slam=True, shake=True)
au(SFX + "impact.wav", C3 + 2.98, 0.7)
ov(C3 + 4.6, C3 + 6.6, "sub", text="에 올리면... 타요.")
ov(C3 + 6.7, C3 + 9.4, "sub", text="[약한 불]에서 오래 두면...", hl=BLUE)
ov(C3 + 9.6, 45.0, "big", text="잘 졸여집니다.", color=GOLD, y=0.45, size=170, slam=True)

shot(45.0, "real", "R4_joryeosseumnida", m="none")
ov(45.0, 45.9, "label", text="실제 상황 (최강록 셰프)")

# --- 쇼츠 구간 (세로 화면) ---
au(SFX + "whoosh.wav", 45.85, 0.8)
au(SFX + "quest.wav", 46.0, 0.7)
ov(46.0, 48.2, "quest", text="퀘스트 발견!  최종 보스 '수능'")
C4 = 46.2
au(VO + "C4.wav", C4)
for t0, z, f in [(45.9, 1.0, (0.5, 0.4)), (47.4, 1.15, (0.5, 0.3)), (48.6, 1.35, (0.5, 0.28)), (50.0, 1.05, (0.5, 0.4)),
                 (51.4, 1.3, (0.5, 0.3)), (52.6, 1.1, (0.5, 0.35))]:
    shot(t0, "vimg", K1 + "3-1.png", m="hand", zoom=z, focus=f)
shot(54.0, "vid", "S-12", s=1.0, m="push")
shot(55.2, "vimg", K1 + "3-1.png", m="hand", zoom=1.4, focus=(0.5, 0.28))
ov(46.4, 56.3, "tag", text="거고 교사", sub="조림 전문가 | 약불 담당")
ov(C4, C4 + 3.6, "tik", text="안녕하세요, 저 거고 교사인데요.")
ov(C4 + 3.7, C4 + 6.2, "tik", text="제 직업을 [불법]으로 말해 볼게요.", hl=RED)
ov(C4 + 6.3, C4 + 7.8, "tik", text="저는 매일 아침 74기를")
ov(C4 + 7.86, 56.4, "tik", text="[약불]에 졸이는 사람입니다.", hl=GOLD)

C5 = 56.6
au(VO + "C5.wav", C5)
shot(56.4, "img", K1 + "1-9.png", m="slam", bw=True, flash=True, focus=(0.55, 0.35))
ov(56.5, 59.2, "bwtitle", text="수험표의 사생활")
au(SFX + "impact.wav", 56.5, 0.7)
shot(58.0, "vimg", K1 + "3-1.png", m="hand", zoom=1.2, focus=(0.5, 0.3))
shot(59.2, "img", K2 + "S-02.png", m="push", ticket=True)
shot(61.4, "img", K2 + "S-02.png", m="punch", ticket=True, focus=(0.5, 0.5))
shot(62.6, "vimg", K1 + "3-1.png", m="hand", zoom=1.35, focus=(0.5, 0.28))
shot(63.8, "img", K2 + "S-02.png", m="pull", ticket=True, bag=True)
ov(C5 + 3.6, C5 + 6.6, "sub", text="얘는요... 시험 전날 밤에 [제일 외로워요].", hl=BLUE)
ov(C5 + 6.7, C5 + 9.6, "sub", text="꼭... [가방에 넣어 주세요].", hl=GOLD)

M0 = 66.4
au(VO + "M.wav", M0)
for t0, z, f in [(66.2, 1.0, (0.5, 0.35)), (67.5, 1.2, (0.5, 0.3)), (68.8, 1.05, (0.5, 0.4)), (70.1, 1.4, (0.5, 0.28)),
                 (71.3, 1.1, (0.5, 0.35)), (72.6, 1.3, (0.5, 0.3))]:
    shot(t0, "vimg", K1 + "3-2.png", m="hand", zoom=z, focus=f)
ov(66.4, 73.8, "tag", text="수학 교사", sub="1분 컷 비법 유출")
ov(M0, M0 + 3.1, "tik", text="저 수학 교사인데요, 비법 유출합니다.")
ov(M0 + 3.2, M0 + 4.6, "tik", text="쉬운 문제 다시 보는 1분이,")
ov(M0 + 4.28, M0 + 5.6, "big", text="1분", color=GOLD, y=0.3, size=220, slam=True)
ov(M0 + 4.7, M0 + 6.3, "tik", text="[킬러 한 문제]보다", hl=RED, strike=True)
ov(M0 + 6.4, 73.9, "tik", text="점수를 지켜요.")

E1 = 74.0
au(VO + "E1.wav", E1)
for t0, z, f in [(73.8, 1.0, (0.5, 0.35)), (75.2, 1.25, (0.5, 0.3)), (76.6, 1.05, (0.5, 0.4)), (78.2, 1.3, (0.5, 0.3))]:
    shot(t0, "vimg", K1 + "3-3.png", m="hand", zoom=z, focus=f)
ov(74.0, 80.1, "tag", text="영어 교사", sub="역접의 마술사")
ov(E1 + 0.44, E1 + 2.4, "big", text="But", color=WHITE, y=0.32, size=260, slam=True)
ov(E1, E1 + 2.5, "tik", text="지문에 But이 나오면요...")
ov(E1 + 2.6, 80.1, "tik", text="그 뒤에서 정답이 말을 걸어요.")

shot(80.2, "real", "R2_naya_deulgireum", m="none")
ov(80.2, 81.9, "label", text="실제 상황 (최강록 셰프)")
E2 = 82.0
au(VO + "E2.wav", E2)
shot(81.9, "vimg", K1 + "3-3.png", m="slam", zoom=1.35, focus=(0.5, 0.3), bw=True, flash=True)
ov(E2, 84.2, "big", text="나야, 정답.", color=GOLD, y=0.6, size=200, slam=True)
au(SFX + "impact.wav", E2, 0.7)

# --- 파라파라 ---
au(SFX + "scratch.wav", 84.25, 0.9)
C6 = 85.2
au(VO + "C6.wav", C6)
shot(84.3, "img", K1 + "4-1.png", m="push", flash=True)
shot(86.0, "img", KV + "1-5.png", m="punch", focus=(0.5, 0.3))
shot(87.2, "img", K1 + "4-1.png", m="none", zoom=1.25, focus=(0.5, 0.45), still=True)
shot(88.0, "img", K1 + "4-1.png", m="none", zoom=1.55, focus=(0.5, 0.4), still=True)
shot(88.8, "img", K1 + "4-1.png", m="none", zoom=2.0, focus=(0.5, 0.38), still=True)
shot(89.6, "img", K1 + "4-1.png", m="shake", zoom=2.4, focus=(0.5, 0.36))
ov(C6, C6 + 0.9, "sub", text="음...")
ov(C6 + 0.92, C6 + 2.2, "sub", text="자습 감독은 안 하고...")
ov(C6 + 2.26, 91.3, "big", text="갑자기 파라파라?!", color=PINK, y=0.45, size=170, slam=True, shake=True)

EB = 91.3
au(SFX + "eurobeat.wav", EB, 0.6, 101.6 - EB)
beat = 60 / 155 * 2
seq = [("vid", "4-2", 0.0), ("vimg", K1 + "3-2.png", 0), ("vid", "4-2", 0.8), ("vimg", K1 + "3-3.png", 0),
       ("vid", "4-2", 1.6), ("vid", "4-3", 0.0), ("vid", "4-2", 2.4), ("vimg", K1 + "3-1.png", 0),
       ("vid", "4-2", 3.2), ("vid", "4-3", 0.8), ("vid", "4-2", 4.0), ("vid", "4-3", 1.2)]
for i, (k, s, so) in enumerate(seq):
    t0 = EB + i * beat
    if t0 >= 96.0:
        break
    tint = "pink" if i % 2 == 0 else "cyan"
    if k == "vid":
        shot(t0, k, s, s=so, m="beat", tint=tint, flash=True, crop=1.18 if s == "4-2" else 1.0)
    else:
        shot(t0, k, s, m="beat", zoom=1.2, tint=tint, flash=True)
ALL = 96.2
shot(96.0, "vid", "4-3", s=1.6, m="push", crop=1.0)
au(VO + "ALL.wav", ALL)
for i, (tx, dt) in enumerate([("거고 74기!", 0.0), ("수능 대박!", 1.75), ("대학 합격!", 3.5)]):
    ov(ALL + dt, ALL + dt + 1.7 if i < 2 else 101.7, "big", text=tx, color=[GOLD, PINK, GREEN][i], y=0.42, size=200, slam=True)
    au(SFX + "impact.wav", ALL + dt, 0.6)
shot(101.0, "freeze", "4-3", s=4.9)
shot(101.7, "color", (0, 0, 0))

# ===== 2부: 노래 =====
SA = 102.7
au(SONG, SA, 1.0)


def st(x):
    return SA + x


shot(st(0.0), "vid", "S-01", s=0.0, m="push")
shot(st(5.0), "img", K2 + "S-05c.png", m="push")
ov(st(0.8), st(6.8), "title", text="So Long, So Good", sub="거고 74")

LY = [  # (시작, 끝, 가사)
    (2.2, 4.8, "거고 74, so long"),
    (6.84, 9.4, "새벽 세 시까지 붙잡던 문제집"), (9.4, 11.92, "몇 번이고 날 흔들던 모의고사 점수"),
    (11.92, 13.8, "믿었다가 무너졌던 그 많은 밤"), (13.8, 15.72, "이제는 내가 먼저 등을 돌리지"),
    (15.72, 17.4, "Same desk, same chair"), (17.4, 19.3, "그런데 거울 속엔 다른 얼굴"),
    (20.0, 21.8, "불안은 아직 어제에 머물고"), (21.8, 23.62, "나는 벌써 다음 장을 넘기지"),
    (23.62, 26.5, "So long, so good"), (26.5, 29.42, "So long, so good"),
    (31.7, 34.86, "시험 끝나면"), (35.62, 37.6, "웃으며 안녕"), (37.6, 39.48, "So long, so good"),
    (39.48, 42.2, "나를 시험한 건 문제가 아니라"), (42.2, 45.04, "할 수 있을까 묻던 내 마음이었어"),
    (45.04, 47.0, "좋은 날은 소리 없이 와서"), (47.0, 48.94, "조용히 내 손을 잡아 줘"),
    (48.94, 50.7, "Don't panic, don't rush"), (50.7, 52.5, "아는 만큼 써 내려가"),
    (52.5, 54.4, "가장 시원한 마무리는"), (54.4, 56.34, "끝까지 나를 믿는 것"),
    (56.34, 59.2, "So long, so good"), (59.2, 62.26, "So long, so good"),
    (63.88, 66.5, "시험 끝나면"), (68.52, 70.4, "웃으며 안녕"), (70.5, 72.5, "So long, so good"),
    (73.04, 75.56, "I don't fear you"), (75.56, 77.44, "I just don't need you"), (77.44, 79.4, "(이제 내 차례야)"),
    (80.24, 83.36, "11월 19일, 그날 아침엔"), (83.36, 85.3, "삼 년의 무게도 가볍게"),
    (85.3, 88.1, "So long, so good"), (88.1, 90.96, "So long, so good"),
    (92.32, 95.5, "시험 끝나면"), (96.98, 98.64, "웃으며 안녕"), (98.64, 101.08, "So long, so good"),
    (101.08, 104.5, "거고 74, so long"), (108.9, 111.4, "so good"),
]
KEY = {"끝까지 나를 믿는 것", "나를 시험한 건 문제가 아니라", "할 수 있을까 묻던 내 마음이었어", "I just don't need you",
       "11월 19일, 그날 아침엔"}
for a, b, tx in LY:
    hook = tx.lower().startswith("so long") or tx in ("시험 끝나면", "웃으며 안녕")
    ov(st(a), st(b), "lyric", text=tx, hook=hook, key=tx in KEY)

V1 = [(6.84, "img", K2 + "S-02.png"), (8.12, "photo", "p12"), (9.4, "img", K2 + "S-03.png"), (10.66, "photo", "p02", "1학년"),
      (11.92, "img", K2 + "S-04.png"), (12.86, "photo", "p11", "1학년"), (13.8, "img", KV + "1-3.png"),
      (14.76, "photo", "p13", "1학년"), (15.72, "img", K2 + "S-05a.png"), (16.28, "img", K2 + "S-05b.png"),
      (16.84, "img", K2 + "S-05c.png"), (17.4, "img", KV + "S-06a.png"), (18.35, "photo", "p01", "2학년"),
      (19.3, "photo", "p03"), (20.0, "img", K2 + "S-08.png"), (20.9, "photo", "p05"), (21.8, "img", K2 + "S-06b.png"),
      (22.7, "photo", "p04", "3학년")]
moves = ["push", "panl", "pull", "panr"]
for i, it in enumerate(V1):
    if it[1] == "photo":
        shot(st(it[0]), "photo", it[2], stamp=it[3] if len(it) > 3 else None, seed=i)
    else:
        shot(st(it[0]), "img", it[2], m=moves[i % 4])
shot(st(23.62), "vid", "S-07", s=0.0, m="push")
shot(st(27.62), "photo", "p07", seed=21)
shot(st(28.62), "photo", "p06", seed=22)
shot(st(29.62), "img", KV + "S-07.png", m="push")
shot(st(30.62), "photo", "p10", seed=23)
shot(st(31.7), "vid", "S-07", s=2.5, m="pull")
shot(st(33.4), "photo", "p09", seed=24)
shot(st(34.5), "photo", "p14", seed=25)
shot(st(35.6), "img", KV + "S-07.png", m="punch", focus=(0.75, 0.4))
shot(st(36.6), "collage", ["p01", "p02", "p03", "p04", "p05", "p06", "p07", "p09", "p10", "p11", "p12", "p14"])
V2 = [(39.48, K2 + "S-08.png", "push"), (40.84, K2 + "S-04.png", "pull"), (42.2, KV + "1-3.png", "push"),
      (43.62, K2 + "S-08.png", "punch"), (45.04, K2 + "S-09.png", "push"), (46.02, K1 + "1-6.png", "punch"),
      (47.0, K2 + "S-09.png", "pull"), (47.97, KV + "1-7.png", "push"), (48.94, K2 + "S-10.png", "push"),
      (49.82, K2 + "S-10.png", "punch"), (50.7, K2 + "S-02.png", "panr"), (51.6, K2 + "S-10.png", "pull"),
      (52.5, K2 + "S-11.png", "push"), (53.45, KV + "S-06a.png", "push"), (54.4, K2 + "S-11.png", "punch"),
      (55.37, KV + "S-14.png", "push")]
for a, f, m in V2:
    shot(st(a), "img", f, m=m)
shot(st(56.34), "vid", "S-12", s=0.0, m="push")
H2 = [(61.34, "img", KV + "S-12.png"), (62.34, "photo", "p05"), (63.34, "photo", "p04"), (64.34, "img", KV + "1-5.png"),
      (65.34, "photo", "p07"), (66.34, "photo", "p06"), (67.34, "vid", "S-12"), (68.54, "photo", "p11"),
      (69.54, "photo", "p02"), (70.54, "img", K2 + "E-1.png"), (71.54, "photo", "p13")]
for i, it in enumerate(H2):
    if it[1] == "photo":
        shot(st(it[0]), "photo", it[2], seed=40 + i)
    elif it[1] == "vid":
        shot(st(it[0]), "vid", it[2], s=2.0, m="pull")
    else:
        shot(st(it[0]), "img", it[2], m=moves[i % 4])
shot(st(72.5), "vid", "S-13", s=0.0, m="push")
shot(st(77.5), "img", KV + "S-14.png", m="push")
shot(st(79.0), "img", SCH + "garden_real.png", m="push", flash=True)
ov(st(80.24), st(83.3), "big", text="11월 19일", color=WHITE, y=0.38, size=180, slam=True)
shot(st(82.0), "vimg", SCH + "hallway_real.png", m="push", zoom=1.0)
shot(st(83.36), "img", KV + "1-8.png", m="punch", focus=(0.5, 0.35))
ov(st(83.36), st(84.33), "gauge", v0=1.0, v1=1.0, label="멘탈 잔량")
shot(st(84.33), "img", K2 + "S-15.png", m="push")
shot(st(85.3), "vid", "S-16", s=0.0, m="push")
shot(st(90.3), "img", KV + "S-16.png", m="push")
b1 = 60 / 117.45
for i, k in enumerate(["p01", "p02", "p03", "p04", "p05", "p06", "p07", "p09", "p10", "p11", "p12", "p13", "p14"]):
    shot(st(91.3 + i * b1), "photo", k, seed=70 + i, fast=True)
shot(st(91.3 + 13 * b1), "photo", "p08", seed=99, big=True)
shot(st(101.08), "img", K2 + "S-18.png", m="push", flash=True)
ov(st(101.3), st(104.6), "big", text="거고 74", color=(255, 244, 224), y=0.42, size=230)
shot(st(104.6), "photo", "p08", seed=98, big=True, pull=True)
shot(st(108.9), "fadeblack", "p08")
SE = SA + 111.6

# ===== 마무리 =====
R3 = SE + 0.2
shot(SE, "color", (0, 0, 0))
shot(R3, "real", "R3_eomma", m="none")
ov(R3, R3 + 5.4, "label", text="실제 상황 (최강록 셰프)")
C7 = R3 + 5.6
au(VO + "C7.wav", C7)
shot(C7 - 0.2, "vid", "E-1", s=0.0, m="push")
shot(C7 + 3.0, "photo", "p08", seed=97, big=True)
shot(C7 + 4.4, "vid", "E-1", s=1.4, m="push")
shot(C7 + 6.6, "img", K2 + "E-1.png", m="push", focus=(0.5, 0.35))
ov(C7, C7 + 3.0, "sub", text="거고 74기, 3년 동안 고생 많았습니다.")
ov(C7 + 4.84, C7 + 5.6, "sub", text="흔들리지 말고...")
ov(C7 + 5.66, C7 + 9.2, "sub", text="끝까지... 잘 [졸여져서] 나오세요.", hl=GOLD)
FIN = C7 + 9.4
shot(FIN, "endcard", K2 + "S-18.png")
ov(FIN + 0.2, FIN + 4.2, "big", text="완성: 거고 74기", color=GOLD, y=0.36, size=150, slam=True)
ov(FIN + 0.9, FIN + 4.2, "sub", text="3년 동안 약한 불에서 졸였습니다.", y=0.58)
ov(FIN + 1.4, FIN + 4.2, "credit", text="음악: So Long, So Good (거고 74)   |   © shiny-peace")
au(SFX + "impact.wav", FIN + 0.2, 0.6)
COOK = FIN + 4.4
shot(COOK, "vid", "E-1", s=3.4, m="push")
ov(COOK + 0.6, COOK + 1.8, "sub", text="(다시 천장)", y=0.85)
TOTAL = COOK + 1.8
shot(TOTAL, "end", None)

# ---------------------------------------------------------------- 그리기 도구
FONTS = {}


def font(sz):
    if sz not in FONTS:
        FONTS[sz] = ImageFont.truetype(FONT, sz)
    return FONTS[sz]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def parse_hl(text):
    parts, cur, on = [], "", False
    for ch in text:
        if ch == "[":
            if cur:
                parts.append((cur, False))
            cur, on = "", True
        elif ch == "]":
            parts.append((cur, True))
            cur, on = "", False
        else:
            cur += ch
    if cur:
        parts.append((cur, on))
    return parts


def text_img(text, size, color=WHITE, hl=None, stroke=8, strike=False):
    f = font(size)
    parts = parse_hl(text)
    widths = [f.getlength(p) for p, _ in parts]
    tw = int(sum(widths)) + stroke * 4
    th = int(size * 1.35) + stroke * 2
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = stroke * 2
    for (p, on), w in zip(parts, widths):
        c = (hl or color) if on else color
        d.text((x, stroke), p, font=f, fill=c + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        if strike and on:
            d.line([(x, th * 0.5), (x + w, th * 0.5)], fill=RED + (255,), width=max(6, size // 10))
        x += w
    return im


def paste_center(frame, im, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def rounded_box(w, h, fill, r=24, outline=None, ow=4):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=fill, outline=outline, width=ow)
    return im


CACHE = {}


def cached(key, fn):
    if key not in CACHE:
        CACHE[key] = fn()
    return CACHE[key]


def draw_ov(frame, o, t):
    k = o["kind"]
    lt = t - o["t0"]
    left = o["t1"] - t
    fade = min(1.0, left / 0.12) if left < 0.12 else 1.0
    if k in ("sub", "tik"):
        size = 64 if k == "sub" else 70
        im = cached(("t", o["text"], size, o.get("hl")), lambda: text_img(o["text"], size, WHITE, o.get("hl"), 8, o.get("strike", False)))
        s = 1.0 + 0.25 * (1 - ease(lt / 0.18))
        y = o.get("y", 0.86 if k == "sub" else 0.72) * H
        paste_center(frame, im, W / 2, y, s, min(1.0, lt / 0.08) * fade)
    elif k == "big":
        im = cached(("b", o["text"], o["size"], o["color"]), lambda: text_img(o["text"], o["size"], o["color"], None, 12))
        if o.get("slam"):
            s = 1.0 + 0.9 * (1 - ease(lt / 0.16))
        else:
            s = 0.6 + 0.4 * ease(lt / 0.2)
        s *= 1.0 + 0.04 * lt
        dx = dy = 0
        if o.get("shake"):
            dx, dy = random.uniform(-10, 10), random.uniform(-8, 8)
        paste_center(frame, im, W / 2 + dx, o["y"] * H + dy, s, min(1.0, lt / 0.06) * fade)
    elif k == "label":
        im = cached(("l", o["text"]), lambda: label_img(o["text"]))
        frame.alpha_composite(im, (40, 40))
    elif k == "tag":
        im = cached(("tag", o["text"], o["sub"]), lambda: tag_img(o["text"], o["sub"]))
        x = int(-im.width + (im.width + 60) * ease(lt / 0.3))
        a = fade
        paste_center(frame, im, x + im.width / 2, H * 0.2, 1.0, a)
    elif k == "item":
        im = cached(("item", o["name"]), lambda: item_img(o["title"], o["name"], o["desc"]))
        s = 0.5 + 0.5 * ease(lt / 0.25)
        glow = 0.85 + 0.15 * math.sin(lt * 10)
        paste_center(frame, im, W / 2, H * 0.24, s * glow ** 0.1, min(1.0, lt / 0.1) * fade)
    elif k == "quest":
        im = cached(("q", o["text"]), lambda: quest_img(o["text"]))
        y = -im.height + (im.height + 70) * ease(lt / 0.3)
        paste_center(frame, im, W / 2, y + im.height / 2, 1.0, fade)
    elif k == "gauge":
        if "a0" in o:
            v = o["v0"] + (o["v1"] - o["v0"]) * ease((t - o["a0"]) / (o["a1"] - o["a0"]))
        else:
            v = o["v0"]
        draw_gauge(frame, v, o["label"], blink=o.get("blink") and int(t * 3) % 2 == 0)
    elif k == "bwtitle":
        im = cached(("bw", o["text"]), lambda: bwtitle_img(o["text"]))
        s = 1.0 + 0.6 * (1 - ease(lt / 0.18))
        paste_center(frame, im, W / 2, H * 0.5, s, min(1.0, lt / 0.06) * fade)
    elif k == "lyric":
        hook, key = o.get("hook"), o.get("key")
        size = 96 if hook else 64
        col = GOLD if key else WHITE
        im = cached(("ly", o["text"], size, col), lambda: text_img(o["text"], size, col, None, 6 if not hook else 9))
        if hook:
            s = 1.0 + 0.35 * (1 - ease(lt / 0.2)) + 0.03 * lt
            y = H * 0.8
        else:
            s = 1.0
            y = H * 0.86 - 18 * (1 - ease(lt / 0.25))
        paste_center(frame, im, W / 2, y, s, min(1.0, lt / 0.15) * fade)
    elif k == "title":
        im = cached(("title", o["text"]), lambda: text_img(o["text"], 150, WHITE, None, 6))
        sub = cached(("titles", o["sub"]), lambda: text_img(o["sub"], 70, GOLD, None, 5))
        sp = 1.0 + 0.05 * lt
        paste_center(frame, im, W / 2, H * 0.42, sp, min(1.0, lt / 0.6) * fade)
        paste_center(frame, sub, W / 2, H * 0.56, 1.0, min(1.0, max(0, lt - 0.6) / 0.4) * fade)
    elif k == "credit":
        im = cached(("cr", o["text"]), lambda: text_img(o["text"], 34, (220, 220, 220), None, 3))
        paste_center(frame, im, W / 2, H * 0.9, 1.0, min(1.0, lt / 0.4) * fade)


def label_img(text):
    tx = text_img(text, 40, (255, 230, 120), None, 0)
    box = rounded_box(tx.width + 40, tx.height + 16, (0, 0, 0, 190), 14)
    box.alpha_composite(tx, (20, 6))
    return box


def tag_img(name, sub):
    a = text_img(name, 64, WHITE, None, 0)
    b = text_img(sub, 40, GOLD, None, 0)
    w = max(a.width, b.width) + 70
    box = rounded_box(w, a.height + b.height + 40, (15, 15, 20, 215), 20, GOLD + (255,), 4)
    box.alpha_composite(a, (35, 12))
    box.alpha_composite(b, (35, 14 + a.height))
    return box


def item_img(title, name, desc):
    t1 = text_img(title, 56, GOLD, None, 0)
    t2 = text_img(name, 96, WHITE, None, 6)
    t3 = text_img(desc, 40, (200, 230, 255), None, 0)
    w = max(t1.width, t2.width, t3.width) + 120
    h = t1.height + t2.height + t3.height + 70
    box = rounded_box(w, h, (30, 18, 60, 225), 26, (255, 210, 90, 255), 6)
    y = 18
    for im in (t1, t2, t3):
        box.alpha_composite(im, ((w - im.width) // 2, y))
        y += im.height + 8
    glow = box.filter(ImageFilter.GaussianBlur(18))
    out = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    g = Image.new("RGBA", glow.size, (255, 200, 80, 0))
    g.putalpha(glow.getchannel("A").point(lambda v: int(v * 0.8)))
    out.alpha_composite(g, (40, 40))
    out.alpha_composite(box, (40, 40))
    return out


def quest_img(text):
    tx = text_img(text, 58, (255, 240, 180), None, 4)
    box = rounded_box(tx.width + 80, tx.height + 30, (90, 10, 20, 230), 16, (255, 200, 80, 255), 5)
    box.alpha_composite(tx, (40, 15))
    return box


def bwtitle_img(text):
    tx = text_img(text, 150, (0, 0, 0), None, 0)
    box = Image.new("RGBA", (tx.width + 120, tx.height + 60), (255, 255, 255, 240))
    box.alpha_composite(tx, (60, 30))
    return box


def draw_gauge(frame, v, label, blink=False):
    d = ImageDraw.Draw(frame)
    x0, y0, w, h = W // 2 - 330, 40, 660, 56
    d.rounded_rectangle([x0 - 6, y0 - 6, x0 + w + 6, y0 + h + 6], 18, fill=(0, 0, 0, 170))
    col = RED if v < 0.3 else (GOLD if v < 0.9 else GREEN)
    if not blink:
        d.rounded_rectangle([x0, y0, x0 + max(14, int(w * v)), y0 + h], 14, fill=col + (255,))
    f = font(40)
    txt = f"{label} {int(round(v * 100))}%"
    d.text((x0 + w / 2, y0 + h / 2), txt, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0, 255))
    flame = "🔥"
    del flame


# ---------------------------------------------------------------- 배경 컷 만들기
def cover(im, w, h):
    return ImageOps.fit(im.convert("RGB"), (w, h), Image.LANCZOS)


def vertical_comp(path):
    im = Image.open(path).convert("RGB")
    bg = cover(im, W, H).filter(ImageFilter.GaussianBlur(30))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.35)
    fg = im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, 0))
    return bg


def polaroid(path, seed, big=False):
    rnd = random.Random(seed)
    im = Image.open(path).convert("RGB")
    im = ImageOps.exif_transpose(im)
    bg = cover(im, W, H).filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (20, 14, 8)), 0.45)
    maxw, maxh = (int(W * 0.8), int(H * 0.8)) if big else (int(W * 0.62), int(H * 0.68))
    sc = min(maxw / im.width, maxh / im.height)
    ph_ = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    pad, bot = 22, 70
    card = Image.new("RGBA", (ph_.width + pad * 2, ph_.height + pad + bot), (250, 248, 240, 255))
    card.paste(ph_, (pad, pad))
    ang = 0 if big else rnd.uniform(-6, 6)
    card = card.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sh.putalpha(card.getchannel("A").point(lambda v: int(v * 0.5)))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    return bg, card, sh


def ticket_img():
    w, h = 520, 330
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(248, 244, 232, 255), outline=(60, 60, 60, 255), width=5)
    d.rectangle([28, 70, 170, 260], outline=(80, 80, 80, 255), width=4)
    d.text((99, 165), "사진", font=font(34), fill=(120, 120, 120, 255), anchor="mm")
    d.text((w / 2 + 70, 48), "수 험 표", font=font(56), fill=(20, 20, 20, 255), anchor="mm")
    d.text((200, 110), "2027학년도 대학수학능력시험", font=font(26), fill=(40, 40, 40, 255))
    d.text((200, 160), "수험번호  74-0000", font=font(32), fill=(40, 40, 40, 255))
    d.text((200, 210), "거고 74기", font=font(40), fill=(180, 60, 40, 255))
    return c


class Shot:
    def __init__(self, t0, t1, kind, src, o):
        self.t0, self.t1, self.kind, self.src, self.o = t0, t1, kind, src, o
        self.frames = None
        self.base = None

    def prep(self):
        k, o = self.kind, self.o
        n = int(round((self.t1 - self.t0) * FPS)) + 2
        if k in ("vid", "real", "freeze"):
            path = f"{HD}/{self.src}.mp4" if k != "real" else f"{REAL}/{self.src}.mp4"
            s = o.get("s", 0.0)
            avail = max(0.2, dur(path) - s)
            want = self.t1 - self.t0
            speed = 1.0 if k == "real" else max(1.0, want / avail)
            if k == "freeze":
                speed, n = 1.0, 1
            vf = f"setpts={speed}*(PTS-STARTPTS),fps={FPS},scale={W}:{H}"
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(s), "-i", path, "-vf", vf, "-frames:v", str(n),
                                  "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
            self.frames = [Image.fromarray(a) for a in arr]
        elif k == "img":
            self.base = cover(Image.open(self.src), W, H)
            if o.get("ticket"):
                self.ticket = ticket_img()
        elif k == "vimg":
            self.base = vertical_comp(self.src)
        elif k == "photo":
            self.bg, self.card, self.sh = polaroid(ph(self.src), o.get("seed", 0), o.get("big", False))
            if o.get("stamp"):
                self.stamp = text_img(o["stamp"], 120, RED, None, 8).rotate(-12, expand=True, resample=Image.BICUBIC)
        elif k == "collage":
            ims = [cover(ImageOps.exif_transpose(Image.open(ph(p))), 640, 400) for p in self.src]
            big = Image.new("RGB", (640 * 4, 400 * 3), (0, 0, 0))
            for i, im in enumerate(ims[:12]):
                big.paste(im, ((i % 4) * 640, (i // 4) * 400))
            self.base = big.resize((W, int(W * 1200 / 2560)), Image.LANCZOS)
            self.base = cover(self.base, W, H)
        elif k in ("endcard",):
            self.base = Image.blend(cover(Image.open(self.src), W, H).filter(ImageFilter.GaussianBlur(14)),
                                    Image.new("RGB", (W, H), (0, 0, 0)), 0.55)
        elif k == "fadeblack":
            self.bg, self.card, self.sh = polaroid(ph(self.src), 98, True)

    def frame(self, t):
        k, o = self.kind, self.o
        lt = t - self.t0
        D = max(0.01, self.t1 - self.t0)
        p = lt / D
        if k == "color":
            return Image.new("RGB", (W, H), self.src)
        if k in ("vid", "real", "freeze"):
            i = min(len(self.frames) - 1, int(lt * FPS)) if self.frames else 0
            img = self.frames[i] if self.frames else Image.new("RGB", (W, H))
            if o.get("crop", 1.0) != 1.0:
                c = o["crop"]
                img = img.crop((int(W * (1 - 1 / c) / 2), int(H * (1 - 1 / c) / 2), int(W * (1 + 1 / c) / 2), int(H * (1 + 1 / c) / 2))).resize((W, H))
            img = move(img, o.get("m", "push"), p, lt, o, video=True)
        elif k in ("img", "vimg", "endcard"):
            img = move(self.base, o.get("m", "push"), p, lt, o)
            if o.get("ticket"):
                img = img.convert("RGBA")
                tk = self.ticket
                bob = 8 * math.sin(lt * 3)
                if o.get("bag"):
                    sc = 1.0 - 0.6 * ease(lt / D)
                    paste_center(img, tk, W / 2, H * 0.48 + 260 * ease(lt / D), sc, 1.0 - 0.7 * ease(lt / D))
                else:
                    paste_center(img, tk, W / 2, H * 0.45 + bob, 1.0 + 0.04 * lt)
                img = img.convert("RGB")
        elif k in ("photo", "fadeblack"):
            z = 1.0 + 0.06 * p
            bg = zoom_img(self.bg, z, (0.5, 0.5))
            frame = bg.convert("RGBA")
            if k == "photo":
                drop = 1 - ease(lt / (0.12 if o.get("fast") else 0.22))
                sc = (1.0 + 0.04 * p) if not o.get("pull") else (1.08 - 0.08 * p)
                cy = H / 2 - 120 * drop
                paste_center(frame, self.sh, W / 2 + 14, cy + 22, sc, 1 - drop)
                paste_center(frame, self.card, W / 2, cy, sc * (1 + 0.15 * drop), 1 - drop * 0.7)
                if o.get("stamp") and lt > 0.15:
                    paste_center(frame, self.stamp, W * 0.78, H * 0.25, 1 + 0.6 * (1 - ease((lt - 0.15) / 0.12)))
            else:
                paste_center(frame, self.sh, W / 2 + 14, H / 2 + 22, 1.0)
                paste_center(frame, self.card, W / 2, H / 2, 1.0 - 0.1 * p)
                frame = Image.alpha_composite(frame, Image.new("RGBA", (W, H), (0, 0, 0, int(255 * ease(p)))))
            img = frame.convert("RGB")
        elif k == "collage":
            img = move(self.base, "push", p, lt, o)
        else:
            img = Image.new("RGB", (W, H))
        tint = o.get("tint")
        if tint:
            col = {"blue": (40, 80, 160), "red": (180, 40, 20), "pink": (200, 40, 140), "cyan": (20, 160, 200)}[tint]
            img = Image.blend(img, Image.new("RGB", (W, H), col), 0.22)
        if o.get("bw"):
            img = ImageOps.autocontrast(img.convert("L"), cutoff=1).convert("RGB")
        if o.get("glow"):
            img = Image.blend(img, img.filter(ImageFilter.GaussianBlur(20)), 0.35 + 0.15 * math.sin(lt * 12))
        if o.get("flash") and lt < 0.12:
            img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.85 * (1 - lt / 0.12))
        return img


def zoom_img(img, z, focus):
    if z <= 1.0001:
        return img
    cw, chh = W / z, H / z
    fx, fy = focus
    x = min(max(fx * W - cw / 2, 0), W - cw)
    y = min(max(fy * H - chh / 2, 0), H - chh)
    return img.crop((int(x), int(y), int(x + cw), int(y + chh))).resize((W, H), Image.BILINEAR)


def move(img, m, p, lt, o, video=False):
    focus = o.get("focus", (0.5, 0.5))
    z0 = o.get("zoom", 1.0)
    if m == "push":
        z = z0 * (1.0 + 0.12 * p)
    elif m == "pull":
        z = z0 * (1.12 - 0.12 * p)
    elif m == "punch":
        z = z0 * (1.18 + 0.06 * p)
    elif m == "slam":
        z = z0 * (1.0 + 0.5 * (1 - ease(lt / 0.15)) + 0.08 * p) if z0 == 1.0 else z0 * (1 + 0.4 * (1 - ease(lt / 0.15)))
    elif m in ("panl", "panr"):
        z = z0 * 1.12
        dx = (0.5 - p) * 0.08 if m == "panl" else (p - 0.5) * 0.08
        focus = (focus[0] + dx, focus[1])
    elif m == "beat":
        z = z0 * (1.12 - 0.1 * ease(lt / 0.2))
    elif m in ("shake", "hand"):
        z = z0 * (1.06 + (0.03 * p if m == "hand" else 0.0))
        amp = 0.012 if m == "shake" else 0.004
        focus = (focus[0] + random.uniform(-amp, amp), focus[1] + random.uniform(-amp, amp))
    else:
        z = z0 * (1.0 + (0.0 if o.get("still") else 0.02 * p))
    return zoom_img(img, max(1.0, z), focus)


# ---------------------------------------------------------------- 렌더
def build_shots():
    s = sorted(SHOTS, key=lambda x: x[0])
    out = []
    for i in range(len(s) - 1):
        t0, k, src, o = s[i]
        out.append(Shot(t0, s[i + 1][0], k, src, o))
    return out


def render_chunk(args):
    ci, f0, f1 = args
    random.seed(ci)
    shots = [sh for sh in build_shots() if sh.t1 > f0 / FPS and sh.t0 < f1 / FPS]
    path = f"{OUT}/chunk{ci:02d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", path],
                          stdin=subprocess.PIPE)
    cur = None
    for fi in range(f0, f1):
        t = fi / FPS
        while shots and t >= shots[0].t1:
            shots.pop(0)
            cur = None
        sh = shots[0]
        if cur is not sh:
            sh.prep()
            cur = sh
        fr = sh.frame(t).convert("RGBA")
        for o in OV:
            if o["t0"] <= t < o["t1"]:
                draw_ov(fr, o, t)
        pr.stdin.write(fr.convert("RGB").tobytes())
    pr.stdin.close()
    pr.wait()
    return path


def mix_audio(total):
    ins, fc, labs = [], [], []
    for k, (f, at, vol, maxd) in enumerate(AU):
        ins += ["-i", f]
        tr = f"atrim=0:{maxd}," if maxd else ""
        ms = int(at * 1000)
        fc.append(f"[{k}]{tr}aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[a{k}]")
        labs.append(f"[a{k}]")
    # 실제 짤 소리
    n = len(AU)
    for sh in build_shots():
        if sh.kind == "real":
            ins += ["-i", f"{REAL}/{sh.src}.mp4"]
            ms = int(sh.t0 * 1000)
            fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.0,adelay={ms}|{ms}[a{n}]")
            labs.append(f"[a{n}]")
            n += 1
    fc.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0:duration=longest,apad,atrim=0:{total},alimiter=limit=0.89[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[out]",
                    "-c:a", "pcm_s16le", f"{OUT}/audio.wav"], check=True)


if __name__ == "__main__":
    nf = int(round(TOTAL * FPS))
    only = os.environ.get("ONLY")  # "시작초-끝초" 로 일부만 미리보기
    if only:
        a, b = map(float, only.split("-"))
        r = [(0, int(a * FPS), int(b * FPS))]
        print(render_chunk(r[0]))
        sys.exit()
    nch = 0 if os.environ.get("MIXONLY") else 8
    if nch:
      bounds = [int(nf * i / nch) for i in range(nch + 1)]
      with Pool(4) as pool:
        paths = pool.map(render_chunk, [(i, bounds[i], bounds[i + 1]) for i in range(nch)])
      with open(f"{OUT}/list.txt", "w") as f:
        f.writelines(f"file '{p}'\n" for p in paths)
      subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/list.txt", "-c", "copy", f"{OUT}/video.mp4"], check=True)
    mix_audio(TOTAL)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video.mp4", "-i", f"{OUT}/audio.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{OUT}/geogo74_v5.mp4"], check=True)
    print("done", f"{OUT}/geogo74_v5.mp4", "total", round(TOTAL, 1))
