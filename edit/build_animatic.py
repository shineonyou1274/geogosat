"""거고 74기 수능 응원 영상 가편집본을 만든다.

사용법: python3 build_animatic.py <노래.wav> <1080p 클립 폴더> <출력 폴더>
노래와 1080p 클립은 저장소에 넣지 않으므로 경로를 인자로 받는다.
"""
import os
import subprocess
import sys

SONG, HD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K1 = f"{ROOT}/keyframes/part1/"
K2 = f"{ROOT}/keyframes/part2/"
KV = f"{ROOT}/keyframes/v2/"
FONT = f"{ROOT}/edit/fonts/BlackHanSans-Regular.ttf"
W, H, FPS = 1920, 1080, 24
os.makedirs(OUT, exist_ok=True)

RED, GREEN, WHITE, GOLD = "0xE5484D", "0x3DDC84", "white", "0xF2A541"


def txt(text, y, size, color=WHITE, t0=0, t1=999, x="(w-text_w)/2", box=False):
    return dict(text=text, y=y, size=size, color=color, t0=t0, t1=t1, x=x, box=box)


# (종류, 원본, 길이, 표시, 옵션)
# 종류: vid(1080p 클립) / img(정지 그림, 천천히 다가감) / vimg(세로 그림) / col(단색)
T = [
    ("vid", "1-1", 5, "1-1", {}),
    ("img", K1 + "1-2.png", 2, "1-2", {}),
    ("img", KV + "1-3.png", 6, "1-3", {"txt": [txt("1%", 120, 90, RED)]}),
    ("vid", "1-4", 4, "1-4", {}),
    ("vid", "1-5", 6, "1-5", {}),
    ("img", KV + "1-5.png", 5, "1-5", {}),
    ("img", K1 + "1-6.png", 2, "1-6", {}),
    ("vid", "1-7", 5, "1-7", {"txt": [txt("100%", 90, 90, GREEN, 3.2)]}),
    ("img", KV + "1-8.png", 2, "1-8", {"txt": [txt("100%", 60, 80, GREEN)]}),
    ("img", K1 + "1-9.png", 6, "1-9", {}),
    ("img", KV + "1-8.png", 5, "1-8", {"txt": [txt("100%", 60, 80, GREEN)]}),
    ("vimg", K1 + "3-1.png", 9, "3-1", {"txt": [txt("퀘스트 발견: 최종 보스 '수능'", 70, 64, GOLD, box=True)]}),
    ("vimg", K1 + "3-2.png", 7.5, "3-2", {}),
    ("vimg", K1 + "3-3.png", 8.5, "3-3", {}),
    ("img", K1 + "4-1.png", 8, "4-1", {}),
    ("vid", "4-2", 4, "4-2", {"crop": 1.18}),
    ("vid", "4-3", 4, "4-3", {"start": 1}),
    ("col", "black", 2, "", {}),
    ("vid", "S-01", 8, "S-1", {"txt": [txt("So Long, So Good", "(h-text_h)/2", 110, WHITE, 3.5)]}),
    ("img", K2 + "S-02.png", 3, "S-2", {}),
    ("img", K2 + "S-03.png", 3, "S-3", {}),
    ("img", K2 + "S-04.png", 3, "S-4", {}),
    ("img", K2 + "S-05a.png", 1.34, "S-5", {}),
    ("img", K2 + "S-05b.png", 1.33, "S-5", {}),
    ("img", K2 + "S-05c.png", 1.33, "S-5", {}),
    ("img", KV + "S-06a.png", 2, "S-6", {}),
    ("img", K2 + "S-06b.png", 2, "S-6", {}),
    ("vid", "S-07", 10, "S-7", {}),
    ("img", KV + "S-07.png", 6, "S-7", {}),
    ("img", K2 + "S-08.png", 4, "S-8", {"txt": [txt("나를 시험한 건 문제가 아니라", "h-260", 64, WHITE, box=True),
                                                 txt("할 수 있을까 묻던 내 마음이었어", "h-170", 64, WHITE, 1.5, box=True)]}),
    ("img", K2 + "S-09.png", 4, "S-9", {}),
    ("img", K2 + "S-10.png", 4, "S-10", {}),
    ("img", K2 + "S-11.png", 4, "S-11", {"txt": [txt("가장 시원한 마무리는", "h-260", 64, WHITE, box=True),
                                                  txt("끝까지 나를 믿는 것", "h-170", 64, GOLD, 1.5, box=True)]}),
    ("vid", "S-12", 10, "S-12", {}),
    ("img", KV + "S-12.png", 7, "S-12", {}),
    ("vid", "S-13", 5, "S-13", {}),
    ("img", KV + "S-14.png", 3, "S-14", {}),
    ("img", f"{ROOT}/school/garden_real.png", 4, "S-15", {"txt": [txt("11월 19일", "(h-text_h)/2", 120, WHITE, 0.5)]}),
    ("vid", "S-16", 10, "S-16", {}),
    ("img", KV + "S-16.png", 3, "S-16", {}),
    ("col", "white", 3, "", {}),
    ("img", K2 + "S-18.png", 10, "S-18", {"txt": [txt("거고 74", "(h-text_h)/2", 180, "0xFFF4E0", 1.0)]}),
    ("vid", "E-1", 11, "E-1", {"txt": [txt("완성: 거고 74기", "h-230", 76, WHITE, 7, box=True),
                                        txt("3년 동안 약한 불에서 졸였습니다.", "h-140", 52, WHITE, 7.5, box=True),
                                        txt("음악: So Long, So Good (거고 74)   © shiny-peace", "h-60", 28, "0xDDDDDD", 8)]}),
]


def text_filters(items, idx):
    out = []
    for j, t in enumerate(items):
        tf = f"{OUT}/t{idx:02d}_{j}.txt"
        open(tf, "w", encoding="utf-8").write(t["text"])
        box = ":box=1:boxcolor=black@0.45:boxborderw=18" if t["box"] else ":shadowcolor=black@0.7:shadowx=3:shadowy=3"
        out.append(f"drawtext=fontfile={FONT}:textfile={tf}:expansion=none:fontsize={t['size']}:fontcolor={t['color']}"
                   f":x={t['x']}:y={t['y']}{box}:enable='between(t,{t['t0']},{t['t1']})'")
    return out


def label(text):
    if not text:
        return []
    return [f"drawtext=fontfile={FONT}:text='{text}':x=24:y=24:fontsize=26:fontcolor=white@0.6"]


segs = []
for i, (kind, src, dur, lab, opt) in enumerate(T):
    o = f"{OUT}/seg{i:02d}.mp4"
    n = int(round(dur * FPS))
    post = text_filters(opt.get("txt", []), i) + label(lab)
    if kind == "img":
        vf = [f"scale=3840:-2,zoompan=z='1+0.08*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"] + post
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-vf", ",".join(vf), "-frames:v", str(n)]
    elif kind == "vimg":
        fc = (f"[0]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24,eq=brightness=-0.25[bg];"
              f"[0]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0" + "".join("," + p for p in post))
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-filter_complex", fc, "-frames:v", str(n), "-r", str(FPS)]
    elif kind == "vid":
        start = opt.get("start", 0)
        avail = 5.04 - start
        speed = max(dur / avail, 1.0)
        c = opt.get("crop", 1.0)
        vf = [f"setpts={speed}*(PTS-STARTPTS)", f"scale={int(W * c)}:{int(H * c)}", f"crop={W}:{H}", f"fps={FPS}"] + post
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-i", f"{HD}/{src}.mp4", "-vf", ",".join(vf), "-frames:v", str(n)]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color={src}:s={W}x{H}:r={FPS}"]
        if post:
            cmd += ["-vf", ",".join(post)]
        cmd += ["-frames:v", str(n)]
    cmd += ["-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-an", o]
    subprocess.run(cmd, check=True)
    segs.append(o)

with open(f"{OUT}/list.txt", "w") as f:
    f.writelines(f"file '{s}'\n" for s in segs)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/list.txt", "-c", "copy", f"{OUT}/video.mp4"], check=True)
# 오디오: 컷 시작 시각을 계산해 대사, 효과음, 유로비트, 노래를 배치한다.
starts, acc = {}, 0.0
for kind, src, dur, lab, opt in T:
    starts.setdefault(lab, acc)
    acc += dur
TOTAL = acc
SONG_AT = starts["S-1"]
V = f"{ROOT}/voice/final/"
S = f"{ROOT}/edit/sfx/"
# (파일, 시작 초, 음량, 최대 길이)
EV = [
    (S + "clock.wav", 0.0, 0.35, starts["1-4"] - 0.2),
    (V + "01_student_1-3.wav", 2.0, 1.0, None),
    (V + "02_chef_1-5.wav", starts["1-5"] + 0.6, 1.0, None),
    (S + "spark.wav", starts["1-7"] + 2.4, 0.8, None),
    (V + "03_chef_1-9.wav", starts["1-9"] + 0.4, 1.0, None),
    (V + "04_chef_3-1.wav", starts["3-1"] + 0.2, 1.0, None),
    (V + "05_math_3-2.wav", starts["3-2"] + 0.2, 1.0, None),
    (V + "06_eng_3-3.wav", starts["3-3"] + 0.3, 1.0, None),
    (V + "07_chef_4-1.wav", starts["4-1"] + 1.0, 1.0, None),
    (S + "eurobeat.wav", starts["4-2"], 0.55, starts["S-1"] - 2 - starts["4-2"]),
    (V + "08_chorus.wav", starts["4-3"] + 0.4, 1.0, None),
    (SONG, SONG_AT, 1.0, None),
    (V + "12_chef_E-1.wav", starts["E-1"] + 0.4, 1.0, None),
]
inputs, fc, labels = [], [], []
for k, (f, at, vol, maxd) in enumerate(EV):
    inputs += ["-i", f]
    trim = f"atrim=0:{maxd}," if maxd else ""
    ms = int(at * 1000)
    fc.append(f"[{k + 1}]{trim}aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[a{k}]")
    labels.append(f"[a{k}]")
fc.append("".join(labels) + f"amix=inputs={len(EV)}:normalize=0:duration=longest,atrim=0:{TOTAL}[aout]")
NAME = f"{OUT}/geogo74_animatic_v3.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video.mp4", *inputs,
                "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", NAME], check=True)
print("done", NAME, "song starts at", SONG_AT, "total", TOTAL)
