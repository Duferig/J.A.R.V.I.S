from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import speech_recognition as sr
import re
import keyboard

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

def adjust_volume(volume, change_percentage):
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    new_volume = current_volume + change_percentage
    if new_volume > 100:
        volume.SetMasterVolumeLevelScalar(1.0, None)
    elif new_volume < 0:
        volume.SetMasterVolumeLevelScalar(0.0, None)
    else:
        volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
    return new_volume

def process_command(command):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    change_percentage = 0

    match = re.search(r'\d+', command)
    if match:
        change_percentage = int(match.group())

    if any(phrase in command for phrase in ["увелич", "добав", "громче", "прибав"]):
        new_volume = adjust_volume(volume, change_percentage)
        print("Volume increased to:", new_volume)
    elif any(phrase in command for phrase in ["уменьш", "тише", "убав"]):
        new_volume = adjust_volume(volume, -change_percentage)
        print("Volume decreased to:", new_volume)
    elif any(phrase in command for phrase in ["выключ", "убери", "убрать"]):
        volume.SetMasterVolumeLevelScalar(0.0, None)
        print("Volume set to 0%")
    elif "включи" in command:
        volume.SetMasterVolumeLevelScalar(1.0, None)
        print("Volume set to 100%")

# Флаг для определения, нужно ли прослушивать микрофон
mic_enabled = True

while True:
    if mic_enabled:
        command = get_command()
        if command:
            process_command(command)
            mic_enabled = False  # Блокируем прослушивание микрофона после выполнения команды
    else:
        keyboard.wait('enter')  # Ожидаем нажатия клавиши Enter для разблокировки микрофона
        mic_enabled = True
        