import webbrowser
import pyttsx3
import speech_recognition as sr

def open_in_edge():
    webbrowser.open("https://www.bing.com")

def search_in_bing(query):
    url = "https://www.bing.com/search?q=" + query
    # Укажите путь к исполняемому файлу Edge на вашем компьютере
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
    webbrowser.get('edge').open(url)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_to_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Говорите команду:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Распознаю команду...")
        command = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Речь не распознана")
        return ""
    except sr.RequestError as e:
        print(f"Ошибка запроса к сервису распознавания: {e}")
        return ""

if __name__ == "__main__":
    speak("Говорите 'Открой браузер' для начала.")
    
    while True:
        command = listen_to_command()

        if "открой браузер" in command:
            speak("Открываю браузер.")
            open_in_edge()

            speak("Что вы хотите найти?")
            query = listen_to_command()

            if query:
                speak(f"Ищу в Bing по запросу: {query}")
                search_in_bing(query)
        elif "завершить" in command:
            speak("Программа завершена.")
            break
