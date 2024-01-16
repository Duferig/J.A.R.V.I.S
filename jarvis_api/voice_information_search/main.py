import queue 
import sounddevice as sd 
import vosk 
import json 
import webbrowser 
import urllib.parse
import os
import keyboard
import pyautogui
import requests
from bs4 import BeautifulSoup
q = queue.Queue() 
model = vosk.Model('model_small') 
device = sd.default.device = 0, 4 
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate']) 
def open_second_link(query):
    # Выполните поиск в Bing
    url = "https://www.bing.com/search?q=" + urllib.parse.quote_plus(query)
    response = requests.get(url)

    # Проанализируйте результаты поиска
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('li', class_='b_algo')

    # Извлеките и откройте URL второго сайта
    if search_results and len(search_results) > 1:
        second_link = search_results[1].find('a')['href']
        # Укажите путь к исполняемому файлу Edge на вашем компьютере
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
        webbrowser.get('edge').open(second_link)

def open_first_link(query):
    # Выполните поиск в Bing
    url = "https://www.bing.com/search?q=" + urllib.parse.quote_plus(query)
    response = requests.get(url)

    # Проанализируйте результаты поиска
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('li', class_='b_algo')

    # Извлеките и откройте URL первого сайта
    if search_results:
        first_link = search_results[0].find('a')['href']
        # Укажите путь к исполняемому файлу Edge на вашем компьютере
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
        webbrowser.get('edge').open(first_link)

def close_edge():
    os.system("taskkill /f /im msedge.exe")

def callback(indata, frames, time, status): 
    q.put(bytes(indata)) 

def open_in_edge(): 
    webbrowser.open("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") 

def search_in_bing(query):
    url = "https://www.bing.com/search?q=" + query
    # Укажите путь к исполняемому файлу Edge на вашем компьютере
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
    webbrowser.get('edge').open(url)

# Set up the RawInputStream outside the callback 
with sd.RawInputStream(samplerate=samplerate, blocksize=48000, device=device[0], 
                       dtype="int16", channels=1, callback=callback): 

    rec = vosk.KaldiRecognizer(model, samplerate) 
    search_mode = False
    search_query = ""
    stop_phrases = ['заверши работу', 'останови', 'выключись', 'завершить работу']  # добавьте свои фразы здесь
    full_screen_phrases = ['сделай полноэкранный режим', 'сделай полна экрана режим', 'сделай полно экраны режим', 'сделай полно экранные режим' 'сделаю полна экраный режим' 'сделай фуу скрин' 'сделай полно экранной режим' 'сделай фул скрин']
    exit_full_screen_phrases = ['выключи полноэкранный режим', 'выключи полна экрана режим', 'выключи полна экраны режим', 'выключи полно экранные режим', 'выключу полна экраный режим', 'выключи фуу скрин', 'выключи полно экранной режим', 'выключи фул скрин']
    while True: 
        data = q.get() 
        if rec.AcceptWaveform(data): 
            result = json.loads(rec.Result()) 
            text = result['text'] 
            print(text) 

            if 'открой браузер' in text.lower(): 
                open_in_edge()
            elif 'закрой браузер' in text.lower():
                close_edge()
            elif 'произведи поиск' in text.lower():
                search_mode = True
                search_query = ""
            elif any(phrase in text.lower() for phrase in stop_phrases):
                break
            elif search_mode:
                search_query += text
                search_in_bing(search_query)
                search_mode = False
            elif any(phrase in text.lower() for phrase in full_screen_phrases):
                keyboard.press_and_release('f11')   
            elif 'закрой вкладку' in text.lower():
                keyboard.press_and_release('ctrl+w')
            elif 'сверни браузер' in text.lower():
                keyboard.press_and_release('win+d')
            elif any(phrase in text.lower() for phrase in exit_full_screen_phrases):
                keyboard.press_and_release('f11') 
            elif 'открой первый сайт' in text.lower() and search_query:
                open_first_link(search_query)
                search_query = ""    
            elif 'открой второй сайт' in text.lower() and search_query:
                open_second_link(search_query)
                search_query = ""