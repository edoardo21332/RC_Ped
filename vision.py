# Importiamo le librerie necessarie     //we import the libraries
from keras.models import load_model  # TensorFlow è richiesto per far funzionare Keras // TensorFlow is used for getting Keras to work properly
import cv2  # Installare opencv-python  //we install and import opencv-python
import numpy as np
import serial
import Led
# Definiamo una funzione che acquisisce un flusso video dalla telecamera e classifica gli oggetti rilevati  //we create a function for detecting and classifying different objects present in the video footage
def view(_class):
    i = 0
    np.set_printoptions(suppress=True)
    # Carichiamo il modello di rete neurale già addestrato      //we upload our trained neural network model
    model = load_model("keras_model.h5", compile=False)
    # Carichiamo i nomi delle classi dal file "labels.txt"      //we upload the names of the various classes off the "labels.txt" file
    class_names = open("labels.txt", "r").readlines()
    # Inizializziamo la telecamera                              //we initialize the webcam
    camera = cv2.VideoCapture(0)
    Led.blue()
    # Ciclo while che acquisisce immagini dalla telecamera e le classifica      //while cicle used for acquiring and classifying images off our footage
    while i < 3:  # La classificazione viene eseguita per 5 volte consecutive
        # Acquisiamo un'immagine dalla telecamera
        ret, image = camera.read()
        Led.green()
        # Ridimensioniamo l'immagine a 224x224 pixel
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Convertiamo l'immagine in un array numpy di tipo float32 e la modifichiamo per soddisfare le esigenze del modello
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalizziamo i valori dei pixel dell'immagine
        image = (image / 127.5) - 1
        # Classifichiamo l'immagine utilizzando il modello di rete neurale
        prediction = model.predict(image)
        # Determiniamo la classe predetta
        index = np.argmax(prediction)
        class_name = class_names[index]
        # Determiniamo il punteggio di confidenza della classe predetta
        confidence_score = prediction[0][index]
        # Stampiamo il nome della classe e il punteggio di confidenza
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        # Se la classe predetta corrisponde alla classe cercata, incrementiamo il contatore
        if _class in class_name:
            i += 1
            Led.turnOff()
            Led.green()
        # Altrimenti, se la classe predetta non corrisponde alla classe cercata, azzera il contatore
        else:
            i = 0
    # Chiudiamo la connessione con la telecamera
    camera.release()
    Led.red()
    Led.turnOff()
    # Chiudiamo le finestre di visualizzazione dell'immagine
    cv2.destroyAllWindows()

