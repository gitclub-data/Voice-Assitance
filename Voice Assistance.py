import pyttsx3 as pyt
import speech_recognition as sr
from googlesearch import search
import webbrowser
import os
import requests
import wikipedia
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

engine=pyt.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
notifier=ToastNotifier()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # speak("Listening Now...")
        notifier.show_toast("Listening........")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        # speak("Recogninzing......")
        notifier.show_toast("Recogninzing......")
        query=r.recognize_google(audio,language='en-in')
        notifier.show_toast(f"User said: {query}\n")
    except Exception as e:
        notifier.show_toast("Say that again.....")
        return "None"
    return query

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def play_audio(song_name):
    song_name = song_name.replace(' ', '%20')
    url = 'https://gaana.com/search/{}'.format(song_name)
    source_code = requests.get(url)
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text, "html.parser")
    links = soup.findAll('a', {'class': 'rt_arw'})
    webbrowser.open(links[0]['href'])

if __name__ == "__main__":
    notifier.show_toast("Starting Voice Assitance....")
    while True:
        query=takecommand().lower()
        if 'search' in query:
            if 'google' in query:
                for link in search(query, num_results=5, lang="en-in"):
                    webbrowser.open_new_tab(link)
            elif 'wikipedia' in query:
                query=query.replace("wikipedia","")
                query=query.replace("search","")
                speak(f"searching {query} on wikipedia.......")
                responce=wikipedia.summary(query,sentences=10)
                speak("According to wikipedia...")
                notifier.show_toast(responce)
                speak(responce)


        if 'open' in query:
            if 'notepad' in query:
                os.startfile('C:\\Program Files (x86)\\Notepad++\\notepad++.exe')
            elif 'microsoft' in query:
                if 'word' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Word 2007')
                elif 'excel' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Excel 2007')
                elif 'power' and 'point' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office PowerPoint 2007')

        if 'play' in query:
            if 'song' in query:
                query=query.replace('bye','')
                query=query.replace('play','')
                query=query.replace('song','')
                query=query.replace('in','')
                play_audio(query)
