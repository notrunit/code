import cv2
import face_recognition
import numpy as np
import os
import threading
import requests
import time
import simplejson

# Charger les visages de référence
KNOWN_FACES_DIR = "faces"
TOLERANCE = 0.6
MODEL = "hog"  # ou "cnn" pour plus de précision (mais plus lent)
def send_discord(webhook_url=str,content=str,title=str) -> str: 
    """send embed discord message to a webhook"""
    payload = {"content": ""}
    headers = {
        "Content-Type": "application/json"
            }
    payload["embeds"] = [
                {
                    "description" : content,
                    "title" : title}]
    for _ in range(10):
        response = requests.post(webhook_url, data=simplejson.dumps(payload), headers=headers)
        if response.status_code == 200 or 204:
            return "message sent succesfullly !"
        else:
            time.sleep(1)
    return "failed to send message !"
known_faces = []
known_names = []
def process(faces,names,url):
   

    # Ouvrir la webcam ou un flux vidéo
    video = cv2.VideoCapture(url)  # Remplace 0 par une URL RTSP ou HTTP si nécessaire
    
    if not video.isOpened():
        print(f"❌ Caméra inaccessible : {url}")
        return
    else:
        print(f"{url} is open")
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Convertir l'image en RGB pour face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb_frame, model=MODEL)
        encodings = face_recognition.face_encodings(rgb_frame, locations)

        for encoding, location in zip(encodings, locations):
            matches = face_recognition.compare_faces(faces, encoding, TOLERANCE)
            name = "Inconnu"

            if True in matches:
                match_index = matches.index(True)
                name = names[match_index]
            print(f'{name} a été détécté par {url}')
            send_discord("https://discord.com/api/webhooks/1331666441832763452/W4mBLPwUgVwlxtk-_IfW7L8O2XygNLZb8C3CNSAmJIZWQcnPwNpqwWmxhtseKjY8ylRK",f'{name} a été détécté par {url}','GOD\'S EYE')
            
    video.release()
urls = open('valids.txt','r').readlines()
for name in os.listdir(KNOWN_FACES_DIR):
    img_path = os.path.join(KNOWN_FACES_DIR, name)
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)[0]
    
    known_faces.append(encoding)
    known_names.append(os.path.splitext(name)[0])

print(f'{len(known_names)} visages chargés !')

for i,url in enumerate(urls):
    print(f'début de la surveillance de {i+1} caméras',end="\r")
    thread = threading.Thread(target=process, args=(known_faces, known_names, url.strip()))
    thread.daemon = True  # Permet d’arrêter les threads lorsque le programme se termine
    thread.start()

# Empêcher la fin immédiate du script
while True:
    try:
        pass  # Boucle infinie pour empêcher la fermeture immédiate
    except KeyboardInterrupt:
        print("\n🔴 Interruption par l'utilisateur. Fermeture des caméras...")
        break
