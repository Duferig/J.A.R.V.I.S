import pygetwindow as gw
import pyautogui
import time
import speech_recognition as sr

opened_window = None  # Переменная для запоминания открытого окна

def get_words_after_keywords(sentence):
    keywords = ["открой", "включи", "open"]
    words = sentence.split()
    result = []

    flag = False  # Флаг для обозначения, что находится слово после ключевого слова

    for word in words:
        if flag:
            result.append(word)
        if word.lower() in keywords:
            flag = True

    return ' '.join(result)

def get_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("How can I help you?")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='ru-RU')
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def open_window(window_title):
    global opened_window  # Используем глобальную переменную для запоминания открытого окна
    # Открываем меню "Пуск"
    pyautogui.press('win')
    time.sleep(1)  # Ждем, чтобы меню "Пуск" полностью открылось

    # Вводим название окна в поисковую строку
    pyautogui.write(window_title)
    time.sleep(1)  # Ждем, чтобы результаты поиска появились

    # Выбираем первое совпадение
    pyautogui.press('enter')
    time.sleep(5)
    opened_window = window_title  # Запоминаем открытое окно

def minimize_window():
    global opened_window
    if opened_window is not None:
        pyautogui.hotkey('winleft', 'd')

def maximize_window():
    global opened_window
    if opened_window is not None:
        pyautogui.hotkey('winleft', 'd')
        
def close_window():
    global opened_window
    if opened_window is not None:
        window = gw.getWindowsWithTitle(opened_window)[0]
        window.activate()
        window.close()

# Бесконечный цикл для прослушивания команд
starter = True
while starter:
    command = get_command()
    result_command = get_words_after_keywords(command.lower())
    open_file = result_command.strip()

    if "открой" in command.lower():
        open_window(open_file)
    elif "сверни" in command.lower() or "свернуть" in command.lower():
        minimize_window()
    elif "разверни" in command.lower() or "во весь экран" in command.lower():
        maximize_window()
    elif "закрой" in command.lower():
        close_window()
    elif "заверши" or "завершить" in command.lower():
        starter = False
        print("Завершение работы программы...")
        print("-" * 30)
        time.sleep(1)
        print("Работа программы завершена!")
        
        