import cv2
import webbrowser
import time
import sys

# Classificador de olho
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera")
    sys.exit()

inicio_reconhecimento = None
tempo_limite = 5  # segundos
html_aberto = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar imagem")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar olhos
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eyes) > 0:
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        if inicio_reconhecimento is None:
            inicio_reconhecimento = time.time()

        tempo_passado = time.time() - inicio_reconhecimento

        cv2.putText(frame, f"Reconhecendo: {int(tempo_passado)}s",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        if tempo_passado >= tempo_limite and not html_aberto:
            print("Olho confirmado! Abrindo HTML...")
            webbrowser.open("file:///C:/Users/Aluno/Downloads/testegpsenai/oculos.html")
            html_aberto = True

            time.sleep(1)

            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

    else:
        inicio_reconhecimento = None

    cv2.imshow('Reconhecimento de Olho', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()