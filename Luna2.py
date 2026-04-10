import cv2
import numpy as np
import logging
import os
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime



@dataclass
class Config:

    CAM_W = 640
    CAM_H = 480

    WIN_W = 960
    WIN_H = 600

    BUFFER = 80
    MIN_SAMPLES = 30

    FACE_EVERY = 4

    MIN_PUPIL_RATIO = 0.12
    MAX_PUPIL_RATIO = 0.45

    SAVE_DIR = "LunaScan_Kayitlar"


cfg = Config()




logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.getLogger("LunaScan")




def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


ensure_dir(cfg.SAVE_DIR)




class Camera:

    def __init__(self):

        self.cap = None

    def start(self):

        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.CAM_W)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.CAM_H)

        if not self.cap.isOpened():
            raise RuntimeError("Camera not available")

        log.info("Camera ready")

    def read(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    def stop(self):

        if self.cap:
            self.cap.release()




class FaceEyeDetector:

    def __init__(self):

        casc = cv2.data.haarcascades

        self.face = cv2.CascadeClassifier(
            casc + "haarcascade_frontalface_default.xml")

        self.eye = cv2.CascadeClassifier(
            casc + "haarcascade_eye_tree_eyeglasses.xml")

    def detect_face(self, gray):

        faces = self.face.detectMultiScale(
            gray,
            1.08,
            4,
            minSize=(70, 70)
        )

        if len(faces) == 0:
            return None

        return max(faces, key=lambda f: f[2]*f[3])

    def detect_eyes(self, gray_face):

        eyes = self.eye.detectMultiScale(
            gray_face,
            1.05,
            3,
            minSize=(16,16)
        )

        return eyes[:2]




class PupilDetector:

    def __init__(self):

        self.clahe = cv2.createCLAHE(3.0,(4,4))

    def detect(self, eye, ox, oy):

        gray = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)

        g = self.clahe.apply(gray)

        blur = cv2.GaussianBlur(g,(5,5),1.2)

        h,w = blur.shape

        min_r = max(3,int(min(h,w)*cfg.MIN_PUPIL_RATIO))
        max_r = int(min(h,w)*cfg.MAX_PUPIL_RATIO)

        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            1.1,
            w//2,
            param1=40,
            param2=14,
            minRadius=min_r,
            maxRadius=max_r
        )

        if circles is None:
            return None

        cx,cy,r = np.round(circles[0][0]).astype(int)

        # Purkinje reflex

        sr = int(r*2.5)

        x1=max(0,cx-sr)
        x2=min(w,cx+sr)
        y1=max(0,cy-sr)
        y2=min(h,cy+sr)

        roi = gray[y1:y2,x1:x2]

        _,maxv,_,maxloc = cv2.minMaxLoc(roi)

        reflex=None

        if maxv>180:

            rx=maxloc[0]+x1+ox
            ry=maxloc[1]+y1+oy

            reflex=(rx,ry)

        return (cx+ox,cy+oy,r,reflex)




class Analyzer:

    def __init__(self):

        self.buf = deque(maxlen=cfg.BUFFER)

    def add(self,diam,dx,dy,ref):

        self.buf.append((diam,dx,dy,ref))

    def analyze(self):

        if len(self.buf)<cfg.MIN_SAMPLES:

            return "VERI TOPLANIYOR",0

        diams=[d[0] for d in self.buf]

        dxs=[d[1] for d in self.buf if d[3]]

        avg=np.mean(diams)
        std=np.std(diams)

        if len(dxs)>4:

            off=np.mean(dxs)
            var=np.std(dxs)

        else:

            off=0
            var=100

        score=0

        if abs(off)>4 and var<8:

            score+=np.sign(off)

        if avg>7:

            score-=0.2

        if avg<2.5:

            score+=0.2

        stability=max(0,1-std/3)

        confidence=int(
            stability*40+
            min(len(self.buf)/cfg.BUFFER,1)*30+
            (len(dxs)/len(self.buf))*30
        )

        if confidence<55:

            return "YETERSIZ VERI",confidence

        if abs(score)<0.3:

            return "NORMAL / EMETROPI",confidence

        if score<0:

            return "MIYOPI SUPHESI",confidence

        return "HIPERMETROPI SUPHESI",confidence




class Reporter:

    def save(self,frame,res,conf):

        ts=datetime.now().strftime("%Y%m%d_%H%M%S")

        img=os.path.join(cfg.SAVE_DIR,f"scan_{ts}.png")
        txt=os.path.join(cfg.SAVE_DIR,f"scan_{ts}.txt")

        cv2.imwrite(img,frame)

        with open(txt,"w",encoding="utf8") as f:

            f.write("LunaScan Report\n")
            f.write(f"Result: {res}\n")
            f.write(f"Confidence: {conf}\n")

        log.info("Saved report")


class LunaScan:

    def __init__(self):

        self.cam=Camera()
        self.det=FaceEyeDetector()
        self.pupil=PupilDetector()
        self.an=Analyzer()
        self.rep=Reporter()

        self.frame_id=0

    def run(self):

        self.cam.start()

        cv2.namedWindow("LunaScan",cv2.WINDOW_NORMAL)

        fps=0
        t0=time.time()
        fc=0

        while True:

            frame=self.cam.read()

            if frame is None:
                continue

            frame=cv2.resize(frame,(cfg.WIN_W,cfg.WIN_H))

            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            face=self.det.detect_face(gray)

            pupils=[]

            if face is not None:

                x,y,w,h=face

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                face_roi=frame[y:y+h,x:x+w]
                gray_face=gray[y:y+h,x:x+w]

                eyes=self.det.detect_eyes(gray_face)

                for (ex,ey,ew,eh) in eyes:

                    eye=face_roi[ey:ey+eh,ex:ex+ew]

                    res=self.pupil.detect(eye,x+ex,y+ey)

                    if res:

                        cx,cy,r,ref=res

                        pupils.append(res)

                        cv2.circle(frame,(cx,cy),r,(0,255,0),2)

                        if ref:

                            rx,ry=ref

                            cv2.circle(frame,(rx,ry),4,(255,255,0),-1)

                            dx=rx-cx
                            dy=ry-cy

                            self.an.add(r*2,dx,dy,True)

            result,conf=self.an.analyze()

            cv2.putText(frame,f"{result} | %{conf}",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(0,255,0),2)

            fc+=1
            if time.time()-t0>=1:

                fps=fc
                fc=0
                t0=time.time()

            cv2.putText(frame,f"{fps} FPS",
                        (20,70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,(0,255,255),2)

            cv2.imshow("LunaScan",frame)

            k=cv2.waitKey(1)&0xFF

            if k==ord("q"):
                break

            if k==ord("s"):
                self.rep.save(frame,result,conf)

        self.cam.stop()
        cv2.destroyAllWindows()



if __name__=="__main__":

    try:

        LunaScan().run()

    except Exception as e:

        log.exception("Fatal error")
