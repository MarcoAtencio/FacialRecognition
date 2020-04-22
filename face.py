import cv2
from playsound import playsound

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
video = cv2.VideoCapture(0)
estadoanterior = ""
estadoactual = ""
mostrar=""
while video.isOpened():
    ret, frame = video.read()
    if frame is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hh, ww = gray.shape
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(frame, (int(ww / 3), 0), (int(ww / 3), hh), (0, 0, 255))
            cv2.line(frame, (int(ww*2 / 3), 0), (int(ww*2 / 3), hh), (0, 0, 255))
            if x <= ww / 3:
                estadoactual = "I"
                if not estadoactual == estadoanterior:
                    mostrar = "I: (" + str(x) + "," + str(y) + ")"
                    playsound("izquierdox.mp3")
                    estadoanterior = estadoactual

            elif x+w > ww * 2 /3:
                estadoactual = "D"
                if not estadoactual == estadoanterior:
                    mostrar = "D: (" + str(x) + "," + str(y) + ")"
                    playsound("derechox.mp3")
                    estadoanterior = estadoactual

            else :
                estadoactual = "C"
                if not estadoactual == estadoanterior:
                    mostrar = "C: (" + str(x) + "," + str(y) + ")"
                    playsound("espera.mp3")
                    estadoanterior = estadoactual

            cv2.putText(frame, mostrar, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
