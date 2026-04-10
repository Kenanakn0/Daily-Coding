"""
LunaScan V13 - Laptop Test
Kamera: idx=0, CAP_DSHOW, 640x480

[S] = Analiz et ve kaydet
[Q] veya ESC = Cikis
"""

import sys
import os
import shutil
import tempfile
import time
import traceback
from datetime import datetime

# ═══════════════════════════════════════════════════
# HATA YAKALAYICI — terminal kapanmasin
# ═══════════════════════════════════════════════════
def hata(et, ev, etb):
    print("\n" + "="*55)
    print("PROGRAM HATASI:")
    traceback.print_exception(et, ev, etb)
    print("="*55)
    input("\nEnter'a basin...")
sys.excepthook = hata

import cv2
import numpy as np

print("="*55)
print("  LunaScan V13 - Laptop Test")
print(f"  OpenCV: {cv2.__version__}")

# ── Kayit klasoru ────────────────────────────────
SAVE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "LunaScan_Kayitlar")
os.makedirs(SAVE_DIR, exist_ok=True)
print(f"  Kayitlar: {SAVE_DIR}")
print("="*55)

FONT   = cv2.FONT_HERSHEY_SIMPLEX
GREEN  = (0, 255, 0)
YELLOW = (0, 255, 255)
WHITE  = (255, 255, 255)
RED    = (0, 0, 255)
ORANGE = (0, 140, 255)
GRAY   = (110, 110, 110)
CYAN   = (255, 200, 0)

# ═══════════════════════════════════════════════════
# CASCADE — temp ASCII klasore kopyala
# ═══════════════════════════════════════════════════
def cascade_yukle(name):
    src = None
    for p in [
        os.path.join(cv2.data.haarcascades, name),
        os.path.join(os.path.dirname(cv2.__file__), "data", name),
    ]:
        if os.path.exists(os.path.normpath(p)):
            src = os.path.normpath(p)
            break
    if src is None:
        import urllib.request
        url = ("https://raw.githubusercontent.com/opencv/opencv"
               "/master/data/haarcascades/" + name)
        src = os.path.join(tempfile.gettempdir(), name)
        print(f"  [INDIRILIYOR] {name}")
        urllib.request.urlretrieve(url, src)
    safe = os.path.join(tempfile.gettempdir(), "ls_" + name)
    shutil.copy2(src, safe)
    clf = cv2.CascadeClassifier(safe)
    if clf.empty():
        raise RuntimeError(f"Cascade bos: {safe}")
    print(f"  [OK] {name}")
    return clf

print("\n[1/3] Cascade yukleniyor...")
FACE = cascade_yukle("haarcascade_frontalface_default.xml")
EYE  = cascade_yukle("haarcascade_eye.xml")

# ═══════════════════════════════════════════════════
# KAMERA — tani sonucu: idx=0, CAP_DSHOW
# ═══════════════════════════════════════════════════
print("[2/3] Kamera aciliyor (idx=0, DSHOW)...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("  DSHOW basarisiz, CAP_ANY deneniyor...")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[HATA] Kamera acilamadi!")
    input("Enter...")
    sys.exit()

# Cozunurluk ayarla
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Test karesi
ret, test = cap.read()
if not ret or test is None:
    print("[HATA] Kameradan kare alinamadi!")
    cap.release()
    input("Enter...")
    sys.exit()

rh, rw = test.shape[:2]
print(f"  [OK] Kamera acik: {rw}x{rh}")

# ═══════════════════════════════════════════════════
# PENCERE
# ═══════════════════════════════════════════════════
print("[3/3] Pencere aciliyor...")
WIN = "LunaScan V13"
cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WIN, 960, 600)

print("\n" + "="*55)
print("  HAZIR! Kameraya bakin.")
print("  [S]     Analiz et ve kaydet")
print("  [Q]/ESC Cikis")
print("="*55 + "\n")

# ═══════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════
def pupil_bul(eye_bgr, ox=0, oy=0):
    if eye_bgr is None or eye_bgr.size == 0:
        return []
    g = cv2.cvtColor(eye_bgr, cv2.COLOR_BGR2GRAY)
    h, w = g.shape
    g = cv2.equalizeHist(g)
    g = cv2.GaussianBlur(g, (7,7), 1.5)
    mn = max(4,  int(min(h,w)*0.10))
    mx = max(14, int(min(h,w)*0.42))
    crc = cv2.HoughCircles(
        g, cv2.HOUGH_GRADIENT, 1.2,
        max(w//2, 1), 50, 18, mn, mx)
    out = []
    if crc is not None:
        for cx,cy,r in np.round(crc[0]).astype(int)[:2]:
            x1,x2 = max(0,cx-r), min(w,cx+r)
            y1,y2 = max(0,cy-r), min(h,cy+r)
            if x2>x1 and y2>y1:
                if np.mean(g[y1:y2,x1:x2]) < np.mean(g)*0.76:
                    out.append((cx+ox, cy+oy, r))
    return out


def analiz_kaydet(frame, pupils, face_rect):
    now     = datetime.now()
    ts_str  = now.strftime("%Y-%m-%d %H:%M:%S")
    ts_file = now.strftime("%Y%m%d_%H%M%S")
    img_p   = os.path.join(SAVE_DIR, f"lunascan_{ts_file}.png")
    txt_p   = os.path.join(SAVE_DIR, f"lunascan_{ts_file}.txt")

    px_mm = (face_rect[2] / 150.0) if face_rect is not None else 5.0

    rpt = ["="*50,
           "  LUNASCAN V13 - ANALIZ RAPORU",
           f"  {ts_str}",
           "="*50]

    if len(pupils) == 0:
        diag, col = "TESPIT YOK", GRAY
        rpt += ["", "  Pupil bulunamadi.",
                "  - Kameraya daha yakin oturun",
                "  - Isigi artirin", ""]
    else:
        diams = [(pr*2)/px_mm for _,_,pr in pupils]
        avg   = float(np.mean(diams))
        for i,(px,py,pr) in enumerate(pupils):
            rpt += [f"", f"  Pupil #{i+1}",
                    f"    Konum : ({px},{py}) px",
                    f"    Cap   : {diams[i]:.2f} mm"]
        rpt += ["", f"  Ort. cap : {avg:.2f} mm",
                "  " + "-"*44,
                "  REFRAKSIYON TAHMINI (SIMULASYON)",
                "  !!! 650nm LED olmadan gercek tani degildir !!!",
                "  " + "-"*44]
        if avg > 6.0:
            diag,col = "MIYOPI SUPHESI", ORANGE
        elif avg < 3.0:
            diag,col = "HIPERMETROPI SUPHESI", YELLOW
        else:
            diag,col = "NORMAL / EMETROPI", GREEN
        rpt += [f"  Sonuc : {diag}",
                f"  Cap   : {avg:.2f} mm",
                "",
                "  Kesin tani icin goz hekiminize basvurun.", ""]
    rpt.append("="*50)
    rapor = "\n".join(rpt)

    # Goruntu uzerine yaz
    out = frame.copy()
    fh, fw = out.shape[:2]
    cv2.rectangle(out, (0,fh-80),(fw,fh),(5,5,5),-1)
    cv2.putText(out, f"ANALIZ: {diag}",
                (10,fh-50), FONT, 0.70, col, 2)
    cv2.putText(out, ts_str,
                (10,fh-20), FONT, 0.40, GRAY, 1)
    cv2.putText(out, "TARAMA - Tibbi tani degildir",
                (fw-310,fh-8), FONT, 0.36, ORANGE, 1)
    if len(pupils) > 0:
        cv2.putText(out,
            f"Pupil:{len(pupils)}  Cap:{np.mean(diams):.1f}mm",
            (fw//2-80, fh-50), FONT, 0.45, WHITE, 1)
    for (px,py,pr) in pupils:
        cv2.circle(out,(px,py),pr+5,GREEN,2)
        cv2.circle(out,(px,py),pr,  GREEN,3)
        cv2.circle(out,(px,py),2,   GREEN,-1)

    cv2.imwrite(img_p, out)
    with open(txt_p,"w",encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print(f"  [PNG] {img_p}")
    print(f"  [TXT] {txt_p}\n")
    return diag, col

# ═══════════════════════════════════════════════════
# ANA DONGU
# ═══════════════════════════════════════════════════
face_rect  = None
pupils     = []
eye_rects  = []
last_diag  = None
last_col   = GRAY
frame_n    = 0
fps        = 0.0
t0         = time.time()
fc         = 0
flash      = 0.0

while True:

    # ── Kare al ─────────────────────────────────────
    ret, raw = cap.read()
    if not ret or raw is None:
        # Kapanma yok — sadece bekle
        time.sleep(0.03)
        continue

    frame_n += 1
    fc      += 1
    dt = time.time() - t0
    if dt >= 1.0:
        fps = fc / dt
        fc  = 0
        t0  = time.time()

    frame = cv2.resize(raw, (960, 600))
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w  = frame.shape[:2]

    # ── Yuz tespiti (her 6 frame) ───────────────────
    if frame_n % 6 == 1:
        fs = FACE.detectMultiScale(gray,1.1,5,minSize=(80,80))
        if len(fs) > 0:
            face_rect = tuple(max(fs, key=lambda f: f[2]*f[3]))
        else:
            face_rect = None

    # ── Goz + pupil ─────────────────────────────────
    eye_rects = []
    pupils    = []
    if face_rect is not None:
        fx,fy,fw2,fh2 = face_rect
        fg = gray [fy:fy+fh2//2, fx:fx+fw2]
        fb = frame[fy:fy+fh2//2, fx:fx+fw2]
        es = EYE.detectMultiScale(fg,1.05,6,minSize=(20,20))
        for (ex,ey,ew,eh) in es[:2]:
            ax,ay = fx+ex, fy+ey
            eye_rects.append((ax,ay,ew,eh))
            roi = fb[ey:ey+eh, ex:ex+ew]
            pupils.extend(pupil_bul(roi, ax, ay))

    # ── Cizim ───────────────────────────────────────
    disp = frame.copy()

    if face_rect is not None:
        fx,fy,fw2,fh2 = face_rect
        cv2.rectangle(disp,(fx,fy),(fx+fw2,fy+fh2),(40,70,40),1)

    for (ex,ey,ew,eh) in eye_rects:
        cv2.rectangle(disp,(ex,ey),(ex+ew,ey+eh),(50,50,20),1)

    for (px,py,pr) in pupils:
        cv2.circle(disp,(px,py),pr+5,GREEN,1)
        cv2.circle(disp,(px,py),pr,  GREEN,2)
        cv2.circle(disp,(px,py),2,   GREEN,-1)

    # LED nabzi
    flash += 0.09
    li = int(170 + 85*np.sin(flash))
    cv2.circle(disp,(24,24),9,(0,0,li),-1)
    cv2.putText(disp,"650nm",(38,29),FONT,0.28,(0,50,li),1)

    # Durum
    sc = GREEN if len(pupils) > 0 else (YELLOW if face_rect is not None else RED)
    cv2.putText(disp,
        f"Pupil:{len(pupils)}  Yuz:{'VAR' if face_rect is not None else 'YOK'}  "
        f"{fps:.0f}fps",
        (10,24), FONT, 0.48, sc, 1)

    # Alt serit
    cv2.rectangle(disp,(0,h-38),(w,h),(8,8,8),-1)
    if last_diag:
        cv2.putText(disp, f"Son analiz: {last_diag}",
                    (10,h-12), FONT, 0.55, last_col, 2)
    cv2.putText(disp,"[S] Analiz+Kaydet   [Q] Cikis",
                (w-320,h-12), FONT, 0.40, GRAY, 1)

    cv2.imshow(WIN, disp)

    # ── Tus ─────────────────────────────────────────
    key = cv2.waitKey(1) & 0xFF

    if key in (ord('q'), 27):
        print("[CIKIS]")
        break

    elif key == ord('s'):
        print("[ANALIZ]")
        last_diag, last_col = analiz_kaydet(
            frame, pupils, face_rect)
        # Onay 1.5sn
        onay = disp.copy()
        cv2.rectangle(onay,(w//2-270,h//2-38),
                           (w//2+270,h//2+42),(8,8,8),-1)
        cv2.rectangle(onay,(w//2-270,h//2-38),
                           (w//2+270,h//2+42),last_col,2)
        cv2.putText(onay, f"KAYDEDILDI: {last_diag}",
                    (w//2-250,h//2+8),FONT,0.65,last_col,2)
        cv2.putText(onay,"Devam ediliyor...",
                    (w//2-90,h//2+34),FONT,0.40,GRAY,1)
        cv2.imshow(WIN, onay)
        cv2.waitKey(1500)

# ═══════════════════════════════════════════════════
# TEMIZLE
# ═══════════════════════════════════════════════════
cap.release()
cv2.destroyAllWindows()
print(f"\nKayitlar: {SAVE_DIR}")
input("Cikis icin Enter'a basin...")