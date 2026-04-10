
import sys, os, shutil, tempfile, time, traceback
from datetime import datetime
from collections import deque

def hata(et, ev, etb):
    print("\n"+"="*55+"\nHATA:")
    traceback.print_exception(et, ev, etb)
    print("="*55)
    input("Enter...")
sys.excepthook = hata

import cv2
import numpy as np

print("="*55)
print("  LunaScan V13 - Laptop Test  v4")
print(f"  OpenCV: {cv2.__version__}")

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "LunaScan_Kayitlar")
os.makedirs(SAVE_DIR, exist_ok=True)
print(f"  Kayitlar: {SAVE_DIR}")
print("="*55)

FONT  = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0,255,0); YELLOW=(0,255,255); WHITE=(255,255,255)
RED   = (0,0,255); ORANGE=(0,140,255); GRAY=(110,110,110)
CYAN  = (255,200,0); TEAL=(160,200,0); BLUE=(200,100,0)


def load_c(name):
    src = None
    for p in [os.path.join(cv2.data.haarcascades, name),
               os.path.join(os.path.dirname(cv2.__file__),"data",name)]:
        if os.path.exists(os.path.normpath(p)):
            src = os.path.normpath(p); break
    if src is None:
        import urllib.request
        url = ("https://raw.githubusercontent.com/opencv/opencv"
               "/master/data/haarcascades/"+name)
        src = os.path.join(tempfile.gettempdir(), name)
        urllib.request.urlretrieve(url, src)
    safe = os.path.join(tempfile.gettempdir(),"ls_"+name)
    shutil.copy2(src, safe)
    c = cv2.CascadeClassifier(safe)
    if c.empty(): raise RuntimeError(f"Bos: {safe}")
    print(f"  [OK] {name}")
    return c

print("\n[1/3] Cascade yukleniyor...")
FACE  = load_c("haarcascade_frontalface_default.xml")
FACE2 = load_c("haarcascade_frontalface_alt2.xml")
LEYE  = load_c("haarcascade_lefteye_2splits.xml")
REYE  = load_c("haarcascade_righteye_2splits.xml")
EYEG  = load_c("haarcascade_eye_tree_eyeglasses.xml")


print("[2/3] Kamera aciliyor...")
cap = None
for bk in [cv2.CAP_DSHOW, cv2.CAP_ANY]:
    c = cv2.VideoCapture(0, bk)
    if c.isOpened():
        ret,t = c.read()
        if ret and t is not None:
            c.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
            c.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            c.set(cv2.CAP_PROP_FPS, 30)
            cap = c; print(f"  [OK] 640x480"); break
        c.release()
if cap is None:
    print("[HATA] Kamera acilamadi!"); input("Enter..."); sys.exit()

print("[3/3] Pencere aciliyor...")
WIN = "LunaScan V13"
cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WIN, 960, 600)

print("\n"+"="*55)
print("  HAZIR!")
print("  Kameraya bakin, 5-10 saniye bekleyin.")
print("  Veri toplandikca gosterge dolacak.")
print("  [S] Analiz+Kaydet   [Q]/ESC Cikis")
print("="*55+"\n")


def goz_bul(gray_face, bgr_face, fw, fh, fx, fy):
    gozler = []
    ey_min = int(fh*0.18)
    ey_max = int(fh*0.58)
    rg = gray_face[ey_min:ey_max, :]
    rb = bgr_face [ey_min:ey_max, :]

    ls = LEYE.detectMultiScale(rg, 1.04, 3, minSize=(14,14))
    for (ex,ey,ew,eh) in ls[:1]:
        gozler.append((fx+ex, fy+ey_min+ey, ew, eh, 'L'))

    rs = REYE.detectMultiScale(rg, 1.04, 3, minSize=(14,14))
    for (ex,ey,ew,eh) in rs[:1]:
        if not any(abs((fx+ex)-g[0])<20 for g in gozler):
            gozler.append((fx+ex, fy+ey_min+ey, ew, eh, 'R'))

    if len(gozler) < 2:
        gs = EYEG.detectMultiScale(rg, 1.04, 3, minSize=(14,14))
        for (ex,ey,ew,eh) in gs[:2]:
            if not any(abs((fx+ex)-g[0])<20 for g in gozler):
                gozler.append((fx+ex, fy+ey_min+ey, ew, eh, 'G'))

    
    if len(gozler) == 0:
        ew2 = fw//4; eh2 = int(fh*0.13)
        ey_abs = fy + int(fh*0.33)
        gozler.append((fx+int(fw*0.12), ey_abs, ew2, eh2, 'F'))
        gozler.append((fx+int(fw*0.56), ey_abs, ew2, eh2, 'F'))

    return gozler[:2]



def pupil_ve_reflex(eye_bgr, ox=0, oy=0):
    """
    Goz ROI icinde:
    - Pupil (koyu daire)
    - Kornea yansimasi / Purkinje (parlak nokta)
    Doner: (pupil_cx, pupil_cy, pupil_r, reflex_cx, reflex_cy) veya None
    """
    if eye_bgr is None or eye_bgr.size == 0:
        return None
    h, w = eye_bgr.shape[:2]
    if h < 8 or w < 8:
        return None

    g = cv2.cvtColor(eye_bgr, cv2.COLOR_BGR2GRAY)

  
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(4,4))
    g_eq  = clahe.apply(g)
    blur  = cv2.GaussianBlur(g_eq, (5,5), 1.2)

    
    mn = max(3, int(min(h,w)*0.12))
    mx = max(10, int(min(h,w)*0.45))
    circles = cv2.HoughCircles(
        blur, cv2.HOUGH_GRADIENT, 1.1, max(w//2,1),
        param1=40, param2=14, minRadius=mn, maxRadius=mx)

    pcx=pcy=pr = None
    if circles is not None:
        for cx,cy,r in np.round(circles[0]).astype(int)[:1]:
            x1,x2 = max(0,cx-r), min(w,cx+r)
            y1,y2 = max(0,cy-r), min(h,cy+r)
            if x2>x1 and y2>y1:
                mean_in  = np.mean(blur[y1:y2,x1:x2])
                mean_all = np.mean(blur)
                if mean_in < mean_all * 0.82:
                    pcx,pcy,pr = cx,cy,r; break

    if pcx is None:
        return None


    sr   = int(pr * 2.5)
    rx1  = max(0, pcx-sr); rx2 = min(w, pcx+sr)
    ry1  = max(0, pcy-sr); ry2 = min(h, pcy+sr)
    if rx2 <= rx1 or ry2 <= ry1:
        return (pcx+ox, pcy+oy, pr, None, None)

    roi_bright = g[ry1:ry2, rx1:rx2]
    _, maxval, _, maxloc = cv2.minMaxLoc(roi_bright)

    rcx = rcy = None
    if maxval > 180:  
        rcx = maxloc[0] + rx1 + ox
        rcy = maxloc[1] + ry1 + oy

    return (pcx+ox, pcy+oy, pr, rcx, rcy)



BUFFER_SIZE = 45  
MIN_SAMPLES = 20   


data_buffer = deque(maxlen=BUFFER_SIZE)


def analiz_et(buf, face_w_px):
    """
    buf: [(diam_mm, dx, dy, found), ...]
    Doner: (tani, renk, detay, guven_pct)
    """
    if len(buf) < MIN_SAMPLES:
        return ("VERI TOPLANIYOR...",
                GRAY,
                f"Ornek: {len(buf)}/{MIN_SAMPLES}",
                int(len(buf)/MIN_SAMPLES*50))

    diams   = [d[0] for d in buf]
    dxs     = [d[1] for d in buf if d[3]]  
    found_r = [d[3] for d in buf]

    avg_diam   = float(np.mean(diams))
    std_diam   = float(np.std(diams))
    reflex_orani = sum(found_r) / len(found_r)

    
    puan = 0.0  

    
    if len(dxs) >= 5:
        mean_dx = float(np.mean(dxs))
        std_dx  = float(np.std(dxs))
        if std_dx < 8 and abs(mean_dx) > 3:
            ofset_agirligi = min(abs(mean_dx)/10.0, 1.0)
            puan += np.sign(mean_dx) * ofset_agirligi * 0.5
    else:
        mean_dx = 0.0; std_dx = 99.0

    if avg_diam > 7.5:          # sadece cok belirgin buyukluk
        puan -= 0.2             # miyopi yonunde hafif katkı
    elif avg_diam < 2.5:        # cok dar
        puan += 0.2             # hipermetropi yonunde hafif katkı

    stabilite = max(0.0, 1.0 - std_diam/3.0)

    guven = int(
        reflex_orani * 40 +          # max 40 puan
        stabilite    * 30 +          # max 30 puan
        min(len(buf)/BUFFER_SIZE, 1) * 30  # max 30 puan
    )

    if guven < 55:
        return ("YETERSIZ VERI",
                GRAY,
                f"Guven dusuk: %{guven}  "
                f"Diam:{avg_diam:.1f}mm  Reflex:%{int(reflex_orani*100)}",
                guven)

    if abs(puan) < 0.15:
        tani = "NORMAL / EMETROPI"
        renk = GREEN
        det  = (f"Anlamli sapma yok  "
                f"Diam:{avg_diam:.1f}mm  Ofset:{mean_dx:.1f}px")

    elif puan < -0.15:
        tani = "MIYOPI SUPHESI"
        renk = ORANGE
        det  = (f"Iceri ofset tespit edildi  "
                f"Diam:{avg_diam:.1f}mm  Ofset:{mean_dx:.1f}px")

    else:
        tani = "HIPERMETROPI SUPHESI"
        renk = YELLOW
        det  = (f"Disa ofset tespit edildi  "
                f"Diam:{avg_diam:.1f}mm  Ofset:{mean_dx:.1f}px")

    return (tani, renk, det, guven)


def kaydet(frame, pupils_data, tani, renk, det, guven, buf):
    now    = datetime.now()
    ts_str = now.strftime("%Y-%m-%d %H:%M:%S")
    ts_f   = now.strftime("%Y%m%d_%H%M%S")
    img_p  = os.path.join(SAVE_DIR, f"lunascan_{ts_f}.png")
    txt_p  = os.path.join(SAVE_DIR, f"lunascan_{ts_f}.txt")

    diams = [d[0] for d in buf] if buf else []
    avg_d = float(np.mean(diams)) if diams else 0.0

    rpt = [
        "="*50,
        "  LUNASCAN V13 - ANALIZ RAPORU",
        f"  {ts_str}",
        "="*50,
        f"\n  Ornek sayisi : {len(buf)}",
        f"  Ort. pupil   : {avg_d:.2f} mm",
        f"  Guven        : %{guven}",
        "\n  "+"-"*44,
        "  SONUC",
        "  "+"-"*44,
        f"  Tani   : {tani}",
        f"  Detay  : {det}",
        "\n  UYARI: Bu sonuc simülasyondur.",
        "  650nm LED olmadigi icin gercek",
        "  eksantrik fotorefraksiyon yapilamamistir.",
        "  Kesin tani icin goz hekiminize basvurun.",
        "\n"+"="*50,
    ]
    rapor = "\n".join(rpt)

    out = frame.copy()
    fh, fw = out.shape[:2]
    cv2.rectangle(out,(0,fh-85),(fw,fh),(5,5,5),-1)
    cv2.putText(out, f"ANALIZ: {tani}", (10,fh-55),FONT,0.70,renk,2)
    cv2.putText(out, det[:60],          (10,fh-28),FONT,0.38,WHITE,1)
    cv2.putText(out, f"Guven: %{guven} | {ts_str}",
                (10,fh-8),FONT,0.36,GRAY,1)
    cv2.putText(out,"SIMULASYON - Tibbi tani degildir",
                (fw-330,fh-8),FONT,0.34,ORANGE,1)

    for (pcx,pcy,pr,rcx,rcy) in pupils_data:
        cv2.circle(out,(pcx,pcy),pr+6,GREEN,1)
        cv2.circle(out,(pcx,pcy),pr,  GREEN,2)
        cv2.circle(out,(pcx,pcy),2,   GREEN,-1)
        if rcx is not None:
            cv2.circle(out,(rcx,rcy),5,CYAN,-1)
            cv2.circle(out,(rcx,rcy),9,CYAN,1)
            cv2.line(out,(pcx,pcy),(rcx,rcy),CYAN,1)

    cv2.imwrite(img_p, out)
    with open(txt_p,"w",encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print(f"  [PNG] {img_p}")
    print(f"  [TXT] {txt_p}\n")
    return img_p

face_rect      = None
face_lost_ctr  = 0
pupils_data    = []   # [(pcx,pcy,pr,rcx,rcy),...]
pupil_lost_ctr = 0
eye_rects      = []
gozler_son     = []
last_tani      = "VERI TOPLANIYOR..."
last_renk      = GRAY
last_det       = f"Kameraya bakin, {MIN_SAMPLES} ornek gerekli"
last_guven     = 0
frame_n        = 0
fps            = 0.0
t0             = time.time()
fc             = 0
flash          = 0.0
face_w_px      = 200   # varsayilan

while True:
    ret, raw = cap.read()
    if not ret or raw is None:
        time.sleep(0.03); continue

    frame_n += 1; fc += 1
    dt = time.time()-t0
    if dt >= 1.0:
        fps=fc/dt; fc=0; t0=time.time()

    frame    = cv2.resize(raw,(960,600))
    lab      = cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)
    l,a,b    = cv2.split(lab)
    l        = cv2.createCLAHE(2.0,(8,8)).apply(l)
    frame_eq = cv2.cvtColor(cv2.merge([l,a,b]),cv2.COLOR_LAB2BGR)
    gray     = cv2.cvtColor(frame_eq,cv2.COLOR_BGR2GRAY)
    h, w     = frame.shape[:2]

    if frame_n % 3 == 1:
        fs = FACE.detectMultiScale(gray,1.08,4,minSize=(70,70))
        if len(fs)==0:
            fs = FACE2.detectMultiScale(gray,1.08,3,minSize=(70,70))
        if len(fs)>0:
            face_rect     = tuple(max(fs,key=lambda f:f[2]*f[3]))
            face_w_px     = face_rect[2]
            face_lost_ctr = 0
        else:
            face_lost_ctr += 1
            if face_lost_ctr > 60: face_rect = None

    eye_rects  = []
    new_pupils = []

    if face_rect is not None:
        fx,fy,fw2,fh2 = face_rect
        fg = gray     [fy:fy+fh2, fx:fx+fw2]
        fb = frame_eq [fy:fy+fh2, fx:fx+fw2]

        gozler_son = goz_bul(fg, fb, fw2, fh2, fx, fy)

        for (gx,gy,gw,gh,tip) in gozler_son:
            gx1,gy1 = max(0,gx),    max(0,gy)
            gx2,gy2 = min(w,gx+gw), min(h,gy+gh)
            if gx2<=gx1 or gy2<=gy1: continue

            eye_rects.append((gx1,gy1,gw,gh,tip))
            roi = frame_eq[gy1:gy2,gx1:gx2]
            res = pupil_ve_reflex(roi, gx1, gy1)
            if res is not None:
                new_pupils.append(res)

    if len(new_pupils) > 0:
        pupils_data    = new_pupils
        pupil_lost_ctr = 0
    else:
        pupil_lost_ctr += 1
        if pupil_lost_ctr > 15:
            pupils_data = []

    px_mm = face_w_px / 150.0 if face_w_px > 0 else 5.0
    for (pcx,pcy,pr,rcx,rcy) in pupils_data:
        diam_mm   = (pr*2) / px_mm
        found_ref = (rcx is not None)
        dx = (rcx-pcx) if found_ref else 0
        dy = (rcy-pcy) if found_ref else 0
        data_buffer.append((diam_mm, dx, dy, found_ref))

    if frame_n % 5 == 0:
        last_tani, last_renk, last_det, last_guven = \
            analiz_et(list(data_buffer), face_w_px)

    disp = frame.copy()

    if face_rect is not None:
        fx,fy,fw2,fh2 = face_rect
        cv2.rectangle(disp,(fx,fy),(fx+fw2,fy+fh2),(40,70,40),1)

    for (ex,ey,ew,eh,tip) in eye_rects:
        col_e = (TEAL if tip in('L','R') else
                 YELLOW if tip=='G' else GRAY)
        cv2.rectangle(disp,(ex,ey),(ex+ew,ey+eh),col_e,1)
        cv2.putText(disp,tip,(ex+2,ey+10),FONT,0.28,col_e,1)

    for (pcx,pcy,pr,rcx,rcy) in pupils_data:
        cv2.circle(disp,(pcx,pcy),pr+5,GREEN,1)
        cv2.circle(disp,(pcx,pcy),pr,  GREEN,2)
        cv2.circle(disp,(pcx,pcy),2,   GREEN,-1)
        if rcx is not None:
            cv2.circle(disp,(rcx,rcy),5,CYAN,-1)
            cv2.circle(disp,(rcx,rcy),8,CYAN,1)
            cv2.line(disp,(pcx,pcy),(rcx,rcy),CYAN,1)
            dx = rcx-pcx; dy = rcy-pcy
            cv2.putText(disp,f"({dx:+d},{dy:+d})",
                        (rcx+6,rcy-4),FONT,0.28,CYAN,1)

    flash += 0.09
    li = int(160+90*np.sin(flash))
    cv2.circle(disp,(24,24),9,(0,0,li),-1)
    cv2.putText(disp,"650nm",(38,29),FONT,0.27,(0,50,li),1)

    n_p = len(pupils_data)
    sc  = (GREEN if n_p>0 else
           YELLOW if face_rect is not None else RED)
    cv2.putText(disp,
        f"Pupil:{n_p}  Goz:{len(eye_rects)}  "
        f"Yuz:{'VAR' if face_rect is not None else 'YOK'}  "
        f"Tampon:{len(data_buffer)}/{BUFFER_SIZE}  {fps:.0f}fps",
        (10,24),FONT,0.42,sc,1)

    bw = int((w-20) * last_guven/100)
    cv2.rectangle(disp,(10,32),(10+(w-20),40),(20,20,20),-1)
    bar_col = (GREEN if last_guven>70 else
               YELLOW if last_guven>50 else
               ORANGE if last_guven>30 else RED)
    if bw > 0:
        cv2.rectangle(disp,(10,32),(10+bw,40),bar_col,-1)
    cv2.putText(disp,f"Guven: %{last_guven}",
                (10,52),FONT,0.36,bar_col,1)

    cv2.rectangle(disp,(0,h-44),(w,h),(8,8,8),-1)
    cv2.putText(disp,f"{last_tani}",
                (10,h-22),FONT,0.62,last_renk,2)
    cv2.putText(disp,last_det[:65] if last_det else "",
                (10,h-6),FONT,0.34,WHITE,1)
    cv2.putText(disp,"[S] Kaydet  [Q] Cikis",
                (w-210,h-6),FONT,0.36,GRAY,1)

    cv2.imshow(WIN, disp)

    key = cv2.waitKey(1) & 0xFF
    if key in (ord('q'),27):
        print("[CIKIS]"); break

    elif key == ord('s'):
        print("[ANALIZ KAYDEDILIYOR]")
        kaydet(frame, pupils_data,
               last_tani, last_renk, last_det, last_guven,
               list(data_buffer))
        onay = disp.copy()
        cv2.rectangle(onay,(w//2-270,h//2-40),(w//2+270,h//2+44),
                      (8,8,8),-1)
        cv2.rectangle(onay,(w//2-270,h//2-40),(w//2+270,h//2+44),
                      last_renk,2)
        cv2.putText(onay,f"KAYDEDILDI: {last_tani}",
                    (w//2-250,h//2+10),FONT,0.60,last_renk,2)
        cv2.putText(onay,f"Guven: %{last_guven}",
                    (w//2-60,h//2+34),FONT,0.42,WHITE,1)
        cv2.imshow(WIN,onay)
        cv2.waitKey(1800)

cap.release()
cv2.destroyAllWindows()
print(f"\nKayitlar: {SAVE_DIR}")
input("Cikis icin Enter'a basin...")