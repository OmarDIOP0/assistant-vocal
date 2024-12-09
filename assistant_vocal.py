import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
from youtube_search import YoutubeSearch
import webbrowser

# Initialiser la synthèse vocale
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Fonction pour parler (synthèse vocale)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Fonction pour écouter et reconnaître la voix
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Parlez Maintenant')
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language='fr-FR')
            print(f"Vous avez dit: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Je n'ai pas compris")
            return ""
        except sr.RequestError:
            speak("Erreur de connexion")
            return ""

# Fonction pour exécuter une commande
def execute_commande():
    command = recognize_speech()
    if "joue" in command:
        song_name = command.replace("joue", "").strip()
        speak(f"Recherche {song_name} sur Youtube")
        # Recherche sur Youtube
        results = YoutubeSearch(song_name, max_results=1).to_dict()
        if results:
            video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
            speak(f"Lecture de {results[0]['title']} sur Youtube")
            webbrowser.open(video_url)
        else:
            speak("Aucune vidéo trouvée")
    elif "ouvre youtube" in command:
        speak("Ouverture de YouTube")
        webbrowser.open('https://www.youtube.com/')
    elif "fermer" in command:
        speak("Fermeture de l'application")
        app.quit()
    else:
        speak("Commande non reconnue")

# Initialisation du design avec tkinter
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

app = ctk.CTk()
app.title('Bienvenue à DIOP vocal')
app.geometry('500x400')

label = ctk.CTkLabel(app, text="Cliquez sur le bouton pour écouter une commande", font=("Helvetica", 16))
label.pack(pady=30)

# Bouton pour activer la commande vocale
ecoute_button = ctk.CTkButton(app, command=execute_commande, text='Écouter', font=('Helvetica', 16), height=50, width=200)
ecoute_button.pack(pady=20)

# Bouton pour fermer la commande vocale
fermer_button = ctk.CTkButton(app, command=app.quit, text='Fermer', font=('Helvetica', 16), height=50, width=200, fg_color='red')
fermer_button.pack(pady=20)

app.mainloop()
