import pyttsx3 as pyt
import speech_recognition as sr
from googlesearch import search
import webbrowser
import os
import requests
import wikipedia
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import smtplib

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

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('ur___@gmail.com','ur____Password')
    server.sendmail('ur___@gmail.com',to,content)
    server.close()

if __name__ == "__main__":
    notifier.show_toast("Starting Voice Assitance....")
    mail_dict={'gaurav pandey':'gauravpan420@gmail.com'}
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


        elif 'open' in query:
            if 'notepad' in query:
                os.startfile('C:\\Program Files (x86)\\Notepad++\\notepad++.exe')
            elif 'microsoft' in query:
                if 'word' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Word 2007')
                elif 'excel' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Excel 2007')
                elif 'power' and 'point' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office PowerPoint 2007')

        elif 'play' in query:
            if 'song' in query:
                query=query.replace('bye','')
                query=query.replace('play','')
                query=query.replace('song','')
                query=query.replace('in','')
                play_audio(query)

        elif 'send' in query:
            if 'email' in query:
                query = query.replace('send','')
                query = query.replace('email','')
                query = query.replace('to','')
                query=query.strip()
                if query not in mail_dict:
                    notifier.show_toast('Sorry we do not have this contact')
                else:
                    to = mail_dict[query]
                    notifier.show_toast('send mail to ' + to)
                    try:
                        notifier.show_toast('Speak the content')
                        content=takecommand()
                        sendEmail(to,content)
                        notifier.show_toast('Email has been sent')
                    except Exception as e:
                        speak("Sorry,I can't send the mail to "+query)


