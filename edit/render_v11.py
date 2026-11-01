"""거고 74기 수능 응원 영상 v8 렌더러.

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


# ===== 1부: 숫자와 코드 모션그래픽 =====
NP = {"n1": "0ee495e2", "n2": "03e166a8", "n3": "97df74aa", "n4": "89776413", "n5": "de1f8d72"}
P.update(NP)
V3 = ROOT + "/keyframes/v3/"
au(SFX + "bgm_pluck.wav", 3.0, 0.14, 30.0 - 3.0)
shot(0.0, "code", None, dense=0.3)
ov(0.4, 3.2, "type", text="C:\\거창고\\74기> run 거고74_조림레시피.exe", y=0.45, size=70)
au(SFX + "typing.wav", 0.4, 0.6)
ov(3.2, 4.6, "progress", label="74기 재료 데이터 불러오는 중")
au(SFX + "riser.wav", 3.3, 0.5)
STATS = [
    (1.6, ("태어난 지", 0, 6897, "일", "2008.01.01 ~ 2026.11.19")),
    (1.4, ("사랑받은 시간", 0, 165528, "시간", "하루도 빠짐없이")),
    (1.4, ("심장이 뛴 횟수", 0, 794534400, "번", "1분에 80번씩, 쉬지 않고")),
    (1.7, ("거고에 입학한 지", 0, 993, "일", ""), ("학교에 간 날", 0, 530, "일+", "")),
    (1.7, ("거고 급식 (점심만)", 0, 530, "끼+", ""), ("삼시 세끼 함께 먹은 밥", 0, 1590, "끼", "")),
    (1.7, ("동고동락한 시간", 0, 12720, "시간", ""), ("8교시 같이 수업한 시간", 0, 4240, "교시", "")),
    (1.25, ("공부한 시간", 0, 9930, "시간", "1만 시간의 법칙, 거의 다 왔다")),
    (1.15, ("모의고사", 0, 30, "회+", "이제 진짜 한 번 남았다")),
    (2.5, ("Peace쌤이 너희를 지켜보고 사랑한 시간", 0, 23832, "시간", "특히 23비둘기, 사랑해"), "pink"),
    (2.4, ("이제 헤어질 시간", 23832, 984, "시간", "2026.12.30 졸업까지 (수능 날부터)"), "blue"),
]
t0 = 4.6
for i, row in enumerate(STATS):
    d_ = row[0]
    shot(t0, "code", None, dense=0.25 + 0.05 * (i % 3), flash=True, red=False)
    if len(row) == 3 and isinstance(row[2], tuple):
        ov(t0, t0 + d_, "pair", a=row[1], b=row[2])
    else:
        lab, v0, val, unit, sub = row[1]
        sc = {"pink": PINK, "blue": BLUE}.get(row[2]) if len(row) == 3 else None
        ov(t0, t0 + d_, "counter", label=lab, v0=v0, value=val, unit=unit, sub=sub, subcol=sc, big_sub=sc is not None)
    au(SFX + "whoosh.wav", t0, 0.45)
    au(SFX + "blip.wav", t0 + min(0.8, d_ * 0.55), 0.5)
    t0 += d_
shot(t0, "code", None, dense=0.45, red=True)
ov(t0, t0 + 2.0, "big", text="흘린 한숨: 측정 불가", color=(170, 170, 170), y=0.47, size=120, slam=True)
ov(t0, t0 + 2.0, "glitch")
au(SFX + "glitch.wav", t0, 0.7)
t0 += 2.0
shot(t0, "code", None, dense=0.6, red=True, flash=True)
ov(t0, t0 + 2.4, "big", text="WARNING: 불안 감지", color=RED, y=0.42, size=150, slam=True, shake=True)
ov(t0 + 0.5, t0 + 2.4, "sub", text="불안 지수 99%  |  손끝 온도 급하강", y=0.62)
ov(t0, t0 + 2.4, "glitch")
au(SFX + "alarm.wav", t0, 0.5)
t0 += 2.4
shot(t0, "popup", "C1_tteollimnida", red=True)
t0 += 1.25
shot(t0, "code", None, dense=0.3)
ov(t0, t0 + 1.4, "type", text="> 해결사 호출 중...", y=0.45, size=80)
au(SFX + "typing.wav", t0, 0.6, 1.3)
t0 += 1.4
shot(t0, "img", ROOT + "/keyframes/v4/c5_entrance.png", m="slam", flash=True)
ov(t0, t0 + 0.35, "glitch")
ov(t0 + 0.1, t0 + 1.4, "item", title="히어로 소환!", name="조림 셰프 등판", desc="스킬: 약불 조절  |  불안 졸이기")
au(SFX + "glitch.wav", t0, 0.6)
au(SFX + "impact.wav", t0, 0.8)
t0 += 1.4
MEME = t0
au(REAL + "/joryeoya.wav", MEME, 1.0)
shot(MEME, "vid", "dance", s=0.0, m="beat")
WORDS = [(0.0, "넌 졸여야 돼"), (0.9, "넌 졸여야 돼"), (1.9, "넌 졸여야 돼"), (2.8, "넌 졸여야 돼"),
         (3.7, "촉촉 졸여야 돼"), (4.6, "넌 졸여야 돼"), (5.6, "그냥 조림으로 자꾸 가는 것 같애")]
cols = [GOLD, PINK, GREEN, BLUE, GOLD, PINK, WHITE]
for k, (dt, w) in enumerate(WORDS):
    end = WORDS[k + 1][0] if k + 1 < len(WORDS) else 7.6
    ov(MEME + dt, MEME + end, "big", text=w, color=cols[k], y=0.18 if k % 2 == 0 else 0.82, size=110 if k < 6 else 80, slam=True)
for k, (dt, w) in enumerate([(7.6, "굽고!"), (8.4, "찌고!"), (9.3, "식혀서!"), (10.4, "졸인다!")]):
    shot(MEME + dt, "img", [ROOT + "/keyframes/v4/c1_grill.png", ROOT + "/keyframes/v4/c2_steam.png", ROOT + "/keyframes/v4/c3_cool.png", ROOT + "/keyframes/v4/c4_simmer.png"][k], m="slam",
         zoom=1.0, flash=True, tint=["pink", "cyan", "pink", None][k], focus=(0.5, 0.35))
    ov(MEME + dt, MEME + dt + (0.8 if k < 3 else 1.0), "big", text=w, color=[GOLD, PINK, GREEN, WHITE][k], y=0.45, size=220, slam=True)
t0 = MEME + 11.4
shot(t0, "code", None, dense=0.15)
ov(t0, t0 + 6.4, "recipe", title="Peace쌤의 특급 레시피", kicker="너희를 위한",
   lines=["주재료 | 거고 74기", "조리 시간 | 3년", "불 세기 | 약불", "비법 재료 | 주머니 속 핫팩 (손끝 해동, 멘탈 100%)", "완성 예정 | 2026.11.19"])
au(SFX + "item.wav", t0, 0.6)
t0 += 6.4
shot(t0, "popup", "C2_naya")
t0 += 1.75
shot(t0, "img", ROOT + "/keyframes/v4/c6_point.png", m="slam", flash=True)
ov(t0, t0 + 1.9, "big", text="나야, 정답.", color=GOLD, y=0.5, size=210, slam=True)
au(ROOT + "/voice/v8_shiny/E2.wav", t0 + 0.05, 1.0)
au(SFX + "ding.wav", t0, 0.8)
au(SFX + "impact.wav", t0, 0.6)
t0 += 1.9
# 음원 재생 버튼
shot(t0, "player", ROOT + "/keyframes/v4/c7_album.png")
CLICK = t0 + 1.6
au(SFX + "click.wav", CLICK, 1.0)
au(SFX + "confetti.wav", CLICK, 0.8)
t0 = CLICK + 0.35

# ===== 2부: 노래 (같은 그림은 한 번만) =====
SA = CLICK + 0.05
au(SONG, SA, 1.0)


def st(x):
    return SA + x


G = ROOT + "/keyframes/v4/"
for _k in ["11a2441c", "56122c47", "36f8738d", "e244d00d", "e06641a6", "fc6667ab", "b68dc109", "bcbf63d7", "c916195c",
           "0a3850cc", "54680b5d", "4590df0d", "2a3f03fa", "58fde188", "30db9161", "c1679f4d", "e7268ac0", "f474d317",
           "23f407c4", "ae2dea64", "46525f61", "bfbc0a85", "b08ddb14", "0ee495e2", "03e166a8", "89776413", "de1f8d72"]:
    P[_k] = _k
MV = ["push", "panl", "pull", "panr", "punch"]
_seed = [0]


def fill(a, b, items):
    n = len(items)
    for i, it in enumerate(items):
        t0 = st(a + (b - a) * i / n)
        _seed[0] += 1
        if it[0] == "photo":
            shot(t0, "photo", it[1], stamp=it[2] if len(it) > 2 else None, seed=_seed[0], fast=(b - a) / n < 1.2)
        else:
            shot(t0, "img", it[1], m=it[2] if len(it) > 2 else MV[_seed[0] % 5], xf=0.18 if _seed[0] % 3 == 0 else None)


shot(st(0.9), "vid", "S-01", s=0.0, m="push", flash=True)
ov(st(0.8), st(6.8), "title", text="So Long, So Good", sub="거고 74")
LY = [
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

# 1절
fill(6.84, 23.62, [("img", K2 + "S-02.png"), ("img", K2 + "S-03.png"), ("photo", "bfbc0a85", "1학년"),
                   ("img", K2 + "S-04.png"), ("img", KV + "1-3.png"), ("photo", "0a3850cc", "2학년"), ("img", K2 + "S-05a.png"),
                   ("img", K2 + "S-05b.png"), ("img", K2 + "S-05c.png"), ("img", KV + "S-06a.png"), ("photo", "de1f8d72", "3학년"),
                   ("img", K2 + "S-08.png"), ("img", K2 + "S-06b.png")])
# 첫 번째 훅
shot(st(23.62), "vid", "S-07", s=0.0, m="push")
fill(27.62, 39.48, [("photo", "11a2441c"), ("photo", "e244d00d"), ("photo", "e06641a6"),
                    ("photo", "b68dc109"), ("photo", "bcbf63d7"), ("photo", "4590df0d"), ("photo", "58fde188"),
                    ("photo", "46525f61"), ("photo", "b08ddb14"), ("photo", "c1679f4d")])
# 2절
fill(39.48, 56.34, [("img", G + "g08_dorm_night.png"), ("img", KV + "1-8.png"), ("img", G + "g01_ticket_night.png"),
                    ("img", K1 + "1-2.png"), ("img", K2 + "S-09.png"), ("img", K1 + "1-6.png"), ("img", G + "g03_lunchbox.png"),
                    ("photo", "36f8738d"), ("img", K2 + "S-10.png"), ("img", G + "g04_omr_pen.png"), ("img", G + "g09_bus_heart.png"),
                    ("img", G + "g06_laces.png"), ("img", K2 + "S-11.png"), ("img", G + "g07_hands.png"), ("img", KV + "S-14.png"),
                    ("img", G + "g10_calendar.png")])
# 두 번째 훅
shot(st(56.34), "vid", "S-12c", s=0.0, m="push")
fill(61.34, 72.5, [("img", G + "g12_hotpacks.png"), ("photo", "54680b5d"), ("img", G + "g13_snacks.png"), ("photo", "2a3f03fa"),
                   ("photo", "30db9161"), ("img", G + "g14_blanket.png"), ("photo", "f474d317"), ("photo", "23f407c4"),
                   ("img", G + "g15_chalk_heart.png"), ("photo", "ae2dea64"), ("photo", "0ee495e2")])
# 브리지
shot(st(72.5), "vid", "S-13", s=0.0, m="push")
shot(st(77.5), "vimg", SCH + "hallway_real.png", m="push", zoom=1.0)
shot(st(79.0), "img", G + "g05_alarm.png", m="push")
shot(st(79.9), "img", SCH + "garden_real.png", m="push", xf=0.3)
ov(st(80.24), st(81.6), "big", text="D-DAY", color=GOLD, y=0.38, size=180, slam=True)
shot(st(80.9), "img", K2 + "S-15.png", m="push")
shot(st(82.1), "img", G + "g02_gate_hifive.png", m="push")
shot(st(83.36), "img", G + "g11_gate_walk.png", m="push")
ov(st(83.36), st(85.3), "gauge", v0=1.0, v1=1.0, label="멘탈 잔량")
# 마지막 훅
shot(st(85.3), "vid", "S-16p", s=0.0, m="push", xf=0.5)
fill(90.3, 97.4, [("photo", "03e166a8"), ("photo", "89776413"), ("photo", "fc6667ab"), ("photo", "c916195c")])
shot(st(97.4), "img", G + "h2_huddle.png", m="push", xf=0.3)
ov(st(97.4), st(101.08), "bokeh")
shot(st(101.08), "img", G + "h3_jorim.png", m="push", flash=True)
ov(st(101.3), st(104.6), "big", text="거고 74", color=(255, 244, 224), y=0.3, size=230)
shot(st(104.6), "photo", "e7268ac0", seed=98, big=True, pull=True)
shot(st(108.9), "fadeblack", "e7268ac0")
ov(st(104.6), st(111.6), "bokeh")
SE = SA + 111.6

# ===== 마무리: Peace쌤의 진짜 목소리 =====
TC = ROOT + "/keyframes/teacher/"
M0 = SE + 0.8
shot(SE, "color", (0, 0, 0))
au(ROOT + "/voice/teacher/message.wav", M0, 1.0)
ov(SE + 0.1, M0 + 0.2, "hsub", text="Peace쌤이 74기에게", y=0.5, size=130)
SH = [  # (시작, 그림, 움직임, 확대, 초점)
    (0.0, "a1_night", "push", 1.0, (0.5, 0.5)), (3.4, "a1_night", "pull", 1.6, (0.15, 0.35)),
    (6.8, "a2_spring", "push", 1.0, (0.5, 0.5)), (9.6, "a2_spring", "push", 1.7, (0.45, 0.3)),
    (12.3, "a2_spring", "panr", 1.5, (0.8, 0.45)), (16.0, "a3_party", "push", 1.0, (0.5, 0.5)),
    (19.6, "a3_party", "pull", 1.5, (0.55, 0.3)), (23.5, "a3_party", "panl", 1.6, (0.25, 0.45)),
    (26.3, "a4_studyhall", "push", 2.2, (0.5, 0.2)), (30.1, "a4_studyhall", "pull", 2.6, (0.5, 0.17)),
    (34.6, "a5_tears", "push", 1.0, (0.5, 0.5)), (40.7, "a5_tears", "push", 1.5, (0.3, 0.45)),
    (44.4, "a5_tears", "push", 1.25, (0.8, 0.4)),
    (48.6, "a6_gate", "push", 1.0, (0.5, 0.5)), (51.5, "a6_gate", "push", 1.6, (0.62, 0.4)),
    (55.2, "a6_gate", "pull", 1.4, (0.3, 0.5)),
    (59.0, "a7_road", "push", 1.0, (0.5, 0.5)), (62.5, "a8_fighting", "push", 1.0, (0.55, 0.5)),
]
for t_, im_, m_, z_, f_ in SH:
    shot(M0 + t_, "img", TC + im_ + ".png", m=m_, zoom=z_, focus=f_, xf=0.35)
SUBS = [
    (0.0, 6.6, "안녕, 74기. 내일이 수능이라는 게 정말 믿어지지 않는 것 같아."),
    (6.8, 9.4, "너희들 1학년 들어왔을 때부터"),
    (9.5, 12.2, "\"너무너무 예쁘다, 너무너무 사랑스럽다\""),
    (12.3, 16.0, "그래서 내가 너희들 담임을 꼭 하고 싶었다고"),
    (16.0, 19.4, "늘 말했었잖아."),
    (19.6, 23.4, "그래서 작년에 좋은 기회가 있어서"),
    (23.5, 26.2, "좋은 아이들과 한 해 재밌게 보냈는데,"),
    (26.3, 30.0, "올해도 부담임으로서 3학년들 보면서"),
    (30.1, 33.8, "너무 행복하고 좋았던 것 같아."),
    (34.6, 37.6, "수능이라는 걸 생각하면"),
    (37.7, 40.6, "'아, 얘네들이 졸업을 앞두고 있구나' 이 생각이 먼저 들어."),
    (40.7, 44.3, "그래서... 짧았지만"),
    (44.4, 48.3, "너희들이 성장하는 걸 보면서 나는 너무 행복했고,"),
    (48.6, 51.4, "그렇기 때문에 결과가 어떻든 간에"),
    (51.5, 55.1, "중간에 용기 잃지 말고, 끝까지 잘 해내고"),
    (55.2, 58.8, "웃는 모습으로 만났으면 좋겠어."),
    (59.0, 61.5, "인생 긴 거 알지?"),
    (61.6, 62.4, "짧게 보지 말자."),
]
for a_, b_, tx in SUBS:
    ov(M0 + a_, M0 + b_, "hsub", text=tx, y=0.86, size=88)
ov(M0 + 40.7, M0 + 48.3, "hnote", text="(목이 메어서 갈라지는 중)")
ov(M0 + 62.5, M0 + 63.4, "big", text="파이팅!", color=GOLD, y=0.3, size=200, slam=True)
ov(M0 + 63.5, M0 + 67.6, "big", text="사랑해.", color=PINK, y=0.3, size=220, slam=True)
C7 = M0 + 67.8 - 13.2
PR = C7 + 13.2
shot(PR, "printer", None)
au(SFX + "typing.wav", PR, 0.5, 1.2)
au(SFX + "printer.wav", PR + 1.2, 0.7)
au(SFX + "confetti.wav", PR + 3.8, 0.8)
au(SFX + "ding.wav", PR + 3.8, 0.7)
FIN = PR + 6.5
shot(FIN, "color", (22, 16, 10))
ov(FIN, FIN + 4.2, "bokeh")
ov(FIN + 0.2, FIN + 4.0, "big", text="완성: 거고 74기", color=GOLD, y=0.36, size=150, slam=True)
ov(FIN + 0.9, FIN + 4.0, "sub", text="3년 동안 약한 불에서 졸였습니다.", y=0.58)
ov(FIN + 1.4, FIN + 4.0, "credit", text="음악: So Long, So Good (거고 74)   |   © shiny-peace")
au(SFX + "impact.wav", FIN + 0.2, 0.6)
COOK = FIN + 4.2
shot(COOK, "img", ROOT + "/keyframes/v4/c8_ceiling.png", m="slam", flash=True)
ov(COOK + 0.5, COOK + 1.9, "big", text="(다시 천장)", color=WHITE, y=0.82, size=90, slam=True)
au(SFX + "boing.wav", COOK + 0.5, 0.9)
TOTAL = COOK + 1.9
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


def text_img(text, size, color=WHITE, hl=None, stroke=8, strike=False, fontpath=None):
    f = font(size) if not fontpath else ImageFont.truetype(fontpath, size)
    parts = parse_hl(text)
    widths = [f.getlength(p) for p, _ in parts]
    pad = int(size * 0.3) + 6
    tw = int(sum(widths)) + pad * 2
    th = int(size * 1.35) + pad * 2
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = pad
    for (p, on), w in zip(parts, widths):
        c = (hl or color) if on else color
        d.text((x, pad), p, font=f, fill=c + (255,))
        if strike and on:
            d.line([(x, pad + size * 0.62), (x + w, pad + size * 0.62)], fill=RED + (255,), width=max(6, size // 10))
        x += w
    if stroke <= 0:
        return im
    a = im.getchannel("A")
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    for rad, op in ((max(6, size * 0.14), 0.75), (max(2, size * 0.03), 0.55)):
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(a.filter(ImageFilter.GaussianBlur(rad)).point(lambda v, op=op: min(255, int(v * op * 1.6))))
        out.alpha_composite(sh)
    out.alpha_composite(im)
    return out


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
        col = (255, 232, 170) if key else (255, 250, 240)
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


HAND = f"{ROOT}/edit/fonts/NanumPenScript-Regular.ttf"


def polaroid(path, seed, big=False, caption=None):
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
    if caption:
        hf = ImageFont.truetype(HAND, 64)
        ImageDraw.Draw(card).text((card.width - pad - 20, ph_.height + pad + bot / 2), caption, font=hf, fill=(40, 45, 80, 255), anchor="rm")
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
            self.bg, self.card, self.sh = polaroid(ph(self.src), o.get("seed", 0), o.get("big", False), o.get("stamp"))
            if False:
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
                if False:
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



# ---------------------------------------------------------------- v6 추가: 코드 화면, 카운터, 글리치, 레시피
MONO = f"{ROOT}/edit/fonts/JetBrainsMono-Bold.ttf"
_CODE = {}


def code_texture():
    if "tex" not in _CODE:
        rnd = random.Random(7)
        f = ImageFont.truetype(MONO, 26)
        tex = Image.new("L", (W, H * 2), 0)
        d = ImageDraw.Draw(tex)
        toks = ["0x74", "GEOGO", "if(anxiety)", "heat=LOW", "simmer();", "1019", "while(true)", "study++", "love+=1",
                "return 0;", "mock_exam", "D-18", "#74", "0110", "1001", "{ }", "&&", "=>", "kcal", "zzz"]
        for y in range(0, H * 2, 34):
            x = rnd.randint(-40, 0)
            while x < W:
                tk = rnd.choice(toks) if rnd.random() < 0.5 else "".join(rnd.choice("0123456789ABCDEF") for _ in range(rnd.randint(2, 8)))
                d.text((x, y), tk, font=f, fill=rnd.randint(40, 200))
                x += int(f.getlength(tk)) + rnd.randint(20, 90)
        _CODE["tex"] = tex
    return _CODE["tex"]


def code_frame(lt, dense, red):
    tex = code_texture()
    off = int((lt * 140) % H)
    g = tex.crop((0, off, W, off + H))
    g = g.point(lambda v: int(v * dense))
    col = (255, 60, 60) if red else (60, 255, 140)
    base = Image.new("RGB", (W, H), (6, 10, 8) if not red else (16, 4, 4))
    layer = Image.new("RGB", (W, H), col)
    img = Image.composite(layer, base, g)
    return img


_old_prep = Shot.prep
_old_frame = Shot.frame


def _prep(self):
    if self.kind == "code":
        return
    return _old_prep(self)


def _frame(self, t):
    if self.kind == "code":
        lt = t - self.t0
        img = code_frame(lt, self.o.get("dense", 0.3), self.o.get("red", False))
        if self.o.get("flash") and lt < 0.1:
            img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.3 * (1 - lt / 0.1))
        return img
    return _old_frame(self, t)


Shot.prep = _prep
Shot.frame = _frame
_old_draw = draw_ov


def fmt(v):
    return f"{int(v):,}"


def draw_ov(frame, o, t):
    k = o["kind"]
    lt = t - o["t0"]
    if k == "type":
        n = min(len(o["text"]), int(lt * 20) + 1)
        s = o["text"][:n]
        im = cached(("ty", s, o["size"]), lambda: text_img(s, o["size"], (120, 255, 150), None, 0))
        x, y = 160, int(o["y"] * H - im.height / 2)
        frame.alpha_composite(im, (x, y))
        if int(lt * 3) % 2 == 0:
            ImageDraw.Draw(frame).rectangle([x + im.width + 6, y + 14, x + im.width + 6 + o["size"] // 2, y + im.height - 14], fill=(120, 255, 150, 255))
    elif k == "progress":
        p = ease(lt / (o["t1"] - o["t0"] - 0.2))
        d = ImageDraw.Draw(frame)
        x0, y0, w, h = W // 2 - 500, H // 2, 1000, 40
        d.rectangle([x0, y0, x0 + w, y0 + h], outline=(120, 255, 150, 255), width=4)
        d.rectangle([x0 + 8, y0 + 8, x0 + 8 + int((w - 16) * p), y0 + h - 8], fill=(120, 255, 150, 255))
        lab = text_img(f"{o['label']}... {int(p * 100)}%", 52, (120, 255, 150), None, 0)
        frame.alpha_composite(lab, (x0, y0 - lab.height - 20))
    elif k == "counter":
        dur_ = o["t1"] - o["t0"]
        fade = min(1.0, (o["t1"] - t) / 0.15)
        p = ease(lt / 1.1)
        lab = cached(("cl", o["label"]), lambda: text_img(o["label"], 72, WHITE, None, 6))
        paste_center(frame, lab, W / 2, H * 0.28 - 20 * (1 - ease(lt / 0.25)), 1.0, min(1.0, lt / 0.15) * fade)
        num = text_img(fmt(o["value"] * p) + o["unit"], 210, GOLD, None, 12)
        sc = 1.0 + (0.08 if lt > 1.1 and lt < 1.3 else 0.0)
        paste_center(frame, num, W / 2, H * 0.5, sc, min(1.0, lt / 0.1) * fade)
        if lt > 1.1:
            sub = cached(("cs", o["sub"]), lambda: text_img(o["sub"], 50, (200, 220, 210), None, 4))
            paste_center(frame, sub, W / 2, H * 0.7, 1.0, min(1.0, (lt - 1.1) / 0.2) * fade)
    elif k == "glitch":
        if int(t * FPS) % 2 == 0:
            arr = np.array(frame)
            for _ in range(6):
                y = random.randint(0, H - 60)
                hh = random.randint(8, 60)
                arr[y:y + hh] = np.roll(arr[y:y + hh], random.randint(-80, 80), axis=1)
            arr[..., 0] = np.roll(arr[..., 0], 8, axis=1)
            arr[..., 2] = np.roll(arr[..., 2], -8, axis=1)
            frame.paste(Image.fromarray(arr), (0, 0))
    elif k == "recipe":
        card = cached(("rc", o["title"]), lambda: rounded_box(1100, 560, (250, 246, 236, 240), 30, GOLD + (255,), 6))
        y0 = H / 2 + 60 * (1 - ease(lt / 0.3))
        paste_center(frame, card, W / 2, y0, 1.0, min(1.0, lt / 0.2))
        tl = cached(("rt", o["title"]), lambda: text_img(o["title"], 66, (60, 30, 10), None, 0))
        frame.alpha_composite(tl, (int(W / 2 - tl.width / 2), int(y0 - 230)))
        for i, ln in enumerate(o["lines"]):
            a0 = 0.7 + i * 0.9
            if lt > a0:
                im = cached(("rl", ln), lambda: text_img(ln, 60, (40, 40, 40), None, 0))
                yy = int(y0 - 90 + i * 110)
                xx = int(W / 2 - 400 + 30 * (1 - ease((lt - a0) / 0.25)))
                ImageDraw.Draw(frame).rectangle([xx - 60, yy + 22, xx - 30, yy + 52], fill=RED + (255,))
                frame.alpha_composite(im, (xx, yy))
    else:
        _old_draw(frame, o, t)



# ---------------------------------------------------------------- v7 추가: 팝업 짤, 플레이어, 수험표 출력, 디졸브, 보케
_p6 = Shot.prep
_f6 = Shot.frame


def window_frame(w, h, title):
    bar = 54
    win = Image.new("RGBA", (w + 16, h + bar + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(win)
    d.rounded_rectangle([0, 0, w + 15, h + bar + 15], 22, fill=(245, 245, 248, 255), outline=(30, 30, 30, 255), width=3)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([24 + i * 34, 17, 46 + i * 34, 39], fill=c + (255,))
    tf = font(30)
    d.text(((w + 16) / 2, 28), title, font=tf, fill=(40, 40, 40, 255), anchor="mm")
    return win, bar


def _prep7(self):
    k = self.kind
    if k == "popup":
        path = f"{REAL}/{self.src}.mp4"
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", "scale=1280:720,fps=24", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        arr = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280, 3)
        self.frames = [Image.fromarray(a) for a in arr]
        self.win, self.bar = window_frame(1280, 720, "실제 상황.mp4  (최강록 셰프)")
        return
    if k == "player":
        self.art = cover(Image.open(self.src), 520, 520)
        return
    if k == "printer":
        self.ticket = boarding_pass()
        return
    return _p6(self)


def _frame7(self, t):
    k, o = self.kind, self.o
    lt = t - self.t0
    if k == "popup":
        bg = Image.blend(code_frame(lt, 0.25, o.get("red", False)).filter(ImageFilter.GaussianBlur(8)), Image.new("RGB", (W, H), (0, 0, 0)), 0.72)
        fr = bg.convert("RGBA")
        i = min(len(self.frames) - 1, int(lt * FPS))
        win = self.win.copy()
        win.paste(self.frames[i], (8, 8 + self.bar))
        s = 0.55 + 0.45 * ease(lt / 0.18)
        s *= 1.0 + 0.03 * lt
        paste_center(fr, win, W / 2, H / 2, s * 1.12, min(1.0, lt / 0.08))
        return fr.convert("RGB")
    if k == "player":
        return player_frame(self, lt)
    if k == "printer":
        return printer_frame(self, lt)
    return _f6(self, t)


Shot.prep = _prep7
Shot.frame = _frame7


def glass_bg(lt, hue=(30, 40, 60)):
    bg = Image.new("RGB", (W, H), hue)
    d = ImageDraw.Draw(bg)
    for i in range(6):
        x = (i * 397 + lt * 60 * (1 if i % 2 else -1)) % (W + 600) - 300
        d.ellipse([x - 300, 200 + (i % 3) * 220 - 300, x + 300, 200 + (i % 3) * 220 + 300],
                  fill=[(242, 165, 65), (255, 105, 180), (110, 180, 255)][i % 3])
    return bg.filter(ImageFilter.GaussianBlur(120))


def confetti(fr, lt, cx, cy, n=90, seed=1):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(fr)
    for _ in range(n):
        ang = rnd.uniform(0, 2 * math.pi)
        sp = rnd.uniform(400, 1300)
        x = cx + math.cos(ang) * sp * lt
        y = cy + math.sin(ang) * sp * lt + 900 * lt * lt
        c = rnd.choice([GOLD, PINK, GREEN, BLUE, WHITE])
        sz = rnd.randint(8, 18)
        if lt < 1.6:
            d.rectangle([x, y, x + sz, y + sz * 0.6], fill=c + (int(255 * max(0, 1 - lt / 1.6)),))


def player_frame(self, lt):
    CL = 1.6
    fr = glass_bg(lt).convert("RGBA")
    card = Image.new("RGBA", (1100, 760), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, 1099, 759], 40, fill=(255, 255, 255, 70), outline=(255, 255, 255, 160), width=3)
    card.paste(self.art, (60, 60))
    d = ImageDraw.Draw(card)
    d.text((620, 120), "So Long, So Good", font=font(50), fill=(255, 255, 255, 255))
    d.text((620, 210), "거고 74", font=font(48), fill=GOLD + (255,))
    played = max(0.0, lt - CL)
    d.rounded_rectangle([620, 330, 1040, 342], 6, fill=(255, 255, 255, 90))
    d.rounded_rectangle([620, 330, 620 + int(420 * min(1, played / 111.6 * 8)), 342], 6, fill=(255, 255, 255, 255))
    d.text((620, 356), f"0:0{int(played)}" if played < 10 else "0:10", font=font(30), fill=(255, 255, 255, 220))
    d.text((1040, 356), "1:51", font=font(30), fill=(255, 255, 255, 220), anchor="ra")
    bx, by = 830, 520
    pressed = CL <= lt < CL + 0.12
    r = 90 if not pressed else 80
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(255, 255, 255, 240))
    if lt < CL:
        d.polygon([(bx - 26, by - 40), (bx - 26, by + 40), (bx + 42, by)], fill=(30, 30, 40, 255))
    else:
        d.rectangle([bx - 30, by - 36, bx - 8, by + 36], fill=(30, 30, 40, 255))
        d.rectangle([bx + 8, by - 36, bx + 30, by + 36], fill=(30, 30, 40, 255))
    s = 0.9 + 0.1 * ease(lt / 0.35)
    cx, cy = W / 2, H / 2
    paste_center(fr, card, cx, cy + 40 * (1 - ease(lt / 0.35)), s, min(1.0, lt / 0.2))
    gx, gy = cx - 550 * s + bx * s, cy - 380 * s + by * s
    if lt >= CL:
        q = lt - CL
        dd = ImageDraw.Draw(fr)
        for j in range(2):
            rr = 60 + 700 * ease((q - j * 0.12) / 0.8) if q > j * 0.12 else 0
            if rr:
                dd.ellipse([gx - rr, gy - rr, gx + rr, gy + rr], outline=(255, 255, 255, int(220 * max(0, 1 - q / 0.9))), width=6)
        confetti(fr, q, gx, gy, 110, 3)
    # 커서
    p = ease(lt / (CL - 0.1))
    mx, my = W * 0.85 + (gx - W * 0.85) * p, H * 0.9 + (gy - H * 0.9) * p
    if lt >= CL and lt < CL + 0.15:
        mx += 2
        my += 2
    cur = [(mx, my), (mx, my + 52), (mx + 14, my + 40), (mx + 26, my + 64), (mx + 36, my + 59), (mx + 24, my + 36), (mx + 42, my + 36)]
    if lt < CL + 0.12:
        ImageDraw.Draw(fr).polygon(cur, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    img = fr.convert("RGB")
    if lt > CL + 0.5:
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), min(1.0, (lt - CL - 0.5) / 0.4) * 0.9)
    return img


def barcode(w, h, seed=74):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 0
    while x < w:
        bw = rnd.choice([3, 3, 5, 8])
        d.rectangle([x, 0, x + bw - 1, h], fill=(20, 20, 20, 255))
        x += bw + rnd.choice([3, 4, 6])
    return im


def boarding_pass():
    w, h = 1300, 520
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=(250, 246, 236, 255))
    d.rounded_rectangle([0, 0, w - 1, 90], 28, fill=(32, 92, 64, 255))
    d.rectangle([0, 60, w - 1, 90], fill=(32, 92, 64, 255))
    d.text((40, 45), "수험표  |  2027학년도 대학수학능력시험", font=font(40), fill=(255, 255, 255, 255), anchor="lm")
    d.text((w - 40, 45), "D-DAY", font=font(44), fill=GOLD + (255,), anchor="rm")
    d.text((50, 130), "FROM", font=font(28), fill=(120, 120, 120, 255))
    d.text((50, 165), "거고 74기", font=font(96), fill=(30, 30, 30, 255))
    d.text((520, 210), "->", font=font(80), fill=(32, 92, 64, 255))
    d.text((680, 130), "TO", font=font(28), fill=(120, 120, 120, 255))
    d.text((680, 165), "꿈꾸던 곳", font=font(96), fill=(30, 30, 30, 255))
    rows = [("시험일", "2026.11.19 (목)"), ("조리법", "약불에서 3년"), ("담당 셰프", "Peace쌤"), ("탑승 조건", "끝까지 나를 믿는 것")]
    for i, (a, b) in enumerate(rows):
        x = 50 + (i % 2) * 520
        y = 320 + (i // 2) * 90
        d.text((x, y), a, font=font(26), fill=(120, 120, 120, 255))
        d.text((x, y + 32), b, font=font(40), fill=(30, 30, 30, 255))
    d.line([(1060, 110), (1060, h - 20)], fill=(180, 180, 180, 255), width=3)
    c.alpha_composite(barcode(180, 300), (1090, 140))
    d.text((1180, 470), "74-1119", font=font(30), fill=(60, 60, 60, 255), anchor="mm")
    return c


def printer_frame(self, lt):
    fr = glass_bg(lt, (20, 40, 32)).convert("RGBA")
    d = ImageDraw.Draw(fr)
    tk = self.ticket
    slot_y = 200
    d.rounded_rectangle([W / 2 - 760, slot_y - 120, W / 2 + 760, slot_y + 10], 30, fill=(40, 40, 46, 255))
    d.rectangle([W / 2 - 700, slot_y - 6, W / 2 + 700, slot_y + 6], fill=(10, 10, 10, 255))
    lab = cached(("prl", 1), lambda: text_img("수험표 출력 중...", 46, (120, 255, 150), None, 0))
    if lt < 3.8:
        fr.alpha_composite(lab, (int(W / 2 - lab.width / 2), slot_y - 100))
    p = ease((lt - 1.2) / 2.4)
    show = int(tk.height * p)
    if show > 0:
        part = tk.crop((0, tk.height - show, tk.width, tk.height))
        fr.alpha_composite(part, (int(W / 2 - tk.width / 2), slot_y))
        # 인쇄 줄
        if p < 1:
            d.rectangle([W / 2 - tk.width / 2, slot_y + show - 4, W / 2 + tk.width / 2, slot_y + show], fill=(120, 255, 150, 180))
    if lt >= 3.8:
        q = lt - 3.8
        tilt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        confetti(fr, q, W / 2, H / 2, 120, 9)
        st_ = text_img("출력 완료!  잘 다녀와, 74기", 64, GOLD, None, 6)
        paste_center(fr, st_, W / 2, H * 0.9, 1 + 0.5 * (1 - ease(q / 0.2)), min(1, q / 0.1))
    return fr.convert("RGB")


_d6 = draw_ov


def draw_ov(frame, o, t):
    k = o["kind"]
    lt = t - o["t0"]
    if k == "counter":
        fade = min(1.0, (o["t1"] - t) / 0.15)
        p = ease(lt / 0.9)
        v = o.get("v0", 0) + (o["value"] - o.get("v0", 0)) * p
        lab = cached(("cl", o["label"]), lambda: text_img(o["label"], 68, WHITE, None, 6))
        paste_center(frame, lab, W / 2, H * 0.28 - 20 * (1 - ease(lt / 0.25)), 1.0, min(1.0, lt / 0.15) * fade)
        num = text_img(fmt(v) + o["unit"], 210, GOLD, None, 12)
        sc = 1.0 + (0.08 if 0.9 < lt < 1.1 else 0.0)
        paste_center(frame, num, W / 2, H * 0.5, sc, min(1.0, lt / 0.1) * fade)
        if lt > 0.9:
            big = o.get("big_sub")
            col = o.get("subcol") or (200, 220, 210)
            sub = cached(("cs", o["sub"], big), lambda: text_img(o["sub"], 80 if big else 50, col, None, 6))
            s = 1.0 + (0.5 * (1 - ease((lt - 0.9) / 0.2)) if big else 0)
            paste_center(frame, sub, W / 2, H * 0.72, s, min(1.0, (lt - 0.9) / 0.2) * fade)
    elif k == "recipe":
        card = cached(("rc7", o["title"]), lambda: rounded_box(1400, 820, (250, 246, 236, 240), 30, GOLD + (255,), 6))
        y0 = H / 2 + 60 * (1 - ease(lt / 0.3))
        paste_center(frame, card, W / 2, y0, 1.0, min(1.0, lt / 0.2))
        kk = cached(("rk", o["kicker"]), lambda: text_img(o["kicker"], 44, (150, 90, 40), None, 0))
        frame.alpha_composite(kk, (int(W / 2 - kk.width / 2), int(y0 - 370)))
        tl = cached(("rt7", o["title"]), lambda: text_img(o["title"], 80, (60, 30, 10), None, 0))
        frame.alpha_composite(tl, (int(W / 2 - tl.width / 2), int(y0 - 315)))
        for i, ln in enumerate(o["lines"]):
            a0 = 0.6 + i * 0.75
            if lt > a0:
                hot = "핫팩" in ln
                im = cached(("rl7", ln), lambda: text_img(ln, 54, (200, 70, 20) if hot else (40, 40, 40), None, 0))
                yy = int(y0 - 160 + i * 100)
                xx = int(W / 2 - 560 + 30 * (1 - ease((lt - a0) / 0.25)))
                ImageDraw.Draw(frame).rectangle([xx - 54, yy + 22, xx - 26, yy + 50], fill=RED + (255,))
                sc = 1.0 + (0.25 * (1 - ease((lt - a0) / 0.2)) if hot else 0)
                if sc != 1.0:
                    paste_center(frame, im, xx + im.width / 2, yy + im.height / 2, sc)
                else:
                    frame.alpha_composite(im, (xx, yy))
    elif k == "bokeh":
        rnd = random.Random(11)
        d = ImageDraw.Draw(frame)
        for _ in range(40):
            x = rnd.uniform(0, W) + 20 * math.sin(lt + rnd.uniform(0, 6))
            y = (rnd.uniform(0, H) - lt * rnd.uniform(10, 40)) % H
            r = rnd.uniform(8, 40)
            a = int(35 + 35 * math.sin(lt * 2 + rnd.uniform(0, 6)))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 220, 150, max(0, a)))
    else:
        _d6(frame, o, t)


_d7 = draw_ov


def draw_ov(frame, o, t):
    if o["kind"] != "pair":
        return _d7(frame, o, t)
    lt = t - o["t0"]
    fade = min(1.0, (o["t1"] - t) / 0.15)
    p = ease(lt / 0.8)
    for j, (row, cy) in enumerate(((o["a"], 0.3), (o["b"], 0.68))):
        lab, v0, val, unit, _ = row
        dl = 0.12 * j
        q = ease((lt - dl) / 0.8) if lt > dl else 0
        li = cached(("pl", lab), lambda: text_img(lab, 54, WHITE, None, 6))
        paste_center(frame, li, W / 2, H * cy - 105, 1.0, min(1.0, max(0, lt - dl) / 0.15) * fade)
        num = text_img(fmt(v0 + (val - v0) * q) + unit, 150, GOLD, None, 10)
        paste_center(frame, num, W / 2, H * cy + 20, 1.0, min(1.0, max(0, lt - dl) / 0.1) * fade)


_d8 = draw_ov
HANDF = f"{ROOT}/edit/fonts/NanumPenScript-Regular.ttf"


def draw_ov(frame, o, t):
    k = o["kind"]
    if k not in ("hsub", "hnote"):
        return _d8(frame, o, t)
    lt = t - o["t0"]
    fade = min(1.0, (o["t1"] - t) / 0.25, lt / 0.3)
    if k == "hsub":
        im = cached(("hs", o["text"], o["size"]), lambda: text_img(o["text"], o["size"], (255, 246, 228), None, 6, fontpath=HANDF))
        paste_center(frame, im, W / 2, o["y"] * H - 8 * (1 - ease(lt / 0.4)), 1.0, max(0, fade))
    else:
        im = cached(("hn", o["text"]), lambda: text_img(o["text"], 50, (200, 205, 220), None, 4, fontpath=HANDF))
        paste_center(frame, im, W / 2, H * 0.1, 1.0, max(0, fade) * (0.75 + 0.25 * math.sin(lt * 2)))


def render_chunk(args):
    ci, f0, f1 = args
    random.seed(ci)
    allsh = build_shots()
    shots = [sh for sh in allsh if sh.t1 > f0 / FPS and sh.t0 < f1 / FPS]
    path = f"{OUT}/chunk{ci:02d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", path],
                          stdin=subprocess.PIPE)
    cur, prev = None, None
    for fi in range(f0, f1):
        t = fi / FPS
        while shots and t >= shots[0].t1:
            prev = shots.pop(0)
            cur = None
        sh = shots[0]
        if cur is not sh:
            sh.prep()
            cur = sh
        fr = sh.frame(t)
        xf = sh.o.get("xf")
        if xf and prev is not None and t - sh.t0 < xf:
            a = ease((t - sh.t0) / xf)
            pf = prev.frame(t)
            z = 1.0 + 0.15 * a
            pf = zoom_img(pf, z, (0.5, 0.5))
            fr = Image.blend(pf, fr, a)
        if sh.o.get("dark"):
            fr = Image.blend(fr, Image.new("RGB", (W, H), (0, 0, 0)), 0.38)
        fr = fr.convert("RGBA")
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
    n = len(AU)
    for sh in build_shots():
        if sh.kind in ("real", "popup"):
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
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{OUT}/geogo74_v11.mp4"], check=True)
    print("done", f"{OUT}/geogo74_v11.mp4", "total", round(TOTAL, 1))
