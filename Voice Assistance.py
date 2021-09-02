from tkinter import filedialog
from tkinter import *
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
import PyPDF2
import random

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
root = Tk()
root.withdraw()
engine=pyt.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
notifier=ToastNotifier()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening Now...")
        notifier.show_toast("Listening........")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        speak("Recogninzing......")
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
    try:
        webbrowser.open(url)
    except:
        print("Sorry i can't")


#Enter Your Username and password in place of 'ur___@gmail.com' and 'ur____Password'
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('ur___@gmail.com','ur____Password')
    server.sendmail('ur___@gmail.com',to,content)
    server.close()

def googlesearch(query):
    query = query.replace(" ", "+")
    try:
        speak('finding it on google Please wait')
        url = f'https://www.google.com/search?q={query}&oq={query}&aqs=chrome..69i57j46j69i59j35i39j0j46j0l2.4948j0j7&sourceid=chrome&ie=UTF-8'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
    except:
        print("Make sure you have a internet connection")
    try:
        try:
            ans = soup.select('.RqBzHd')[0].getText().strip()
        except:
            try:
                title = soup.select('.AZCkJd')[0].getText().strip()
                try:
                    ans = soup.select('.e24Kjd')[0].getText().strip()
                except:
                    ans = ""
                ans = f'{title}\n{ans}'
            except:
                try:
                    ans = soup.select('.hgKElc')[0].getText().strip()
                except:
                    ans = soup.select('.kno-rdesc span')[0].getText().strip()
    except:
        ans = "can't find any proper explaination."
        speak(ans)
        speak('Here i am opening search result for u')
        webbrowser.open_new_tab(url)
        return
    print(ans)
    speak(ans)


if __name__ == "__main__":
    # notifier.show_toast("Starting Voice Assitance....")
    mail_dict={'gaurav pandey':'gauravpan420@gmail.com'}
    grettings=['hello','hii','am very happy to see you','Nice to meet you again']
    wishes=['good morning', 'good evening','good after noon']
    byewishing=['bye bye','Have a good day','I am happy to help you','see you again later','see you next time!farewell']
    while True:
        # query=takecommand().lower()
        query=input()
        checkgreet=query.split(" ")
        if any(item in checkgreet for item in (grettings or wishes)):
            greet=random.choice(tuple(grettings))
            speak(greet)
        elif 'search' in query:
            query = query.replace("search", "")
            if 'google' in query:
                query=query.replace('google','')
                for link in search(query, num_results=5, lang="en-in"):
                    webbrowser.open_new_tab(link)
            elif 'ganna' in query:
                speak('Searching on gaana')
                query=query.replace('bye','')
                query=query.replace('play','')
                query=query.replace('song','')
                query=query.replace('on','')
                query = query.replace('in', '')
                query = query.replace('ganna', '')
                play_audio(query)
            elif 'youtube' in query or 'you tube' in query:
                speak('searching on youtube')
                query=query.replace("youtube","")
                query = query.replace('on', '')
                query = query.replace('in', '')
                query= query.replace(" ","+")
                webbrowser.open_new_tab('https://www.youtube.com/results?search_query='+query)
            elif 'wikipedia' in query:
                query=query.replace("wikipedia","")
                speak(f"searching {query} on wikipedia.......")
                try:
                    responce=wikipedia.summary(query,sentences=5)
                    speak("According to wikipedia...")
                    notifier.show_toast(responce)
                    speak(responce)
                except:
                    print("Make sure you have a internet connection")
            else:
                print('we do not have this functionality now')

        elif 'open' in query:
            if 'notepad' in query:
                os.startfile('C:\\Program Files (x86)\\Notepad++\\notepad++.exe')
            elif 'pycharm' in query:
                os.startfile('C:\\Program Files\\JetBrains\\PyCharm Community Edition 2019.2.2\\bin\\pycharm64.exe')
            elif 'microsoft' in query:
                if 'word' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Word 2007')
                elif 'excel' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Excel 2007')
                elif 'power' and 'point' in query:
                    os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office PowerPoint 2007')
            else:
                speak('do not have this functionality right now')

        elif 'play' in query:
            if 'song' in query:
                query=query.replace('bye','')
                query=query.replace('play','')
                query=query.replace('song','')
                query=query.replace('on','')
                query = query.replace('in', '')
                query = query.replace('ganna', '')
                play_audio(query)
            else:
                speak("sorry i don't have this functionality right now")
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

        elif 'read' in query:
            if 'pdf' in query:
                try:
                    speak('Please select a file')
                    root.filename = filedialog.askopenfilename(initialdir="C://Users//Dell//Documents//Projects", title="Select pdf File",
                                                       filetypes=(("Pdf File", "*.pdf"), ("all files", "*.*")))
                    pdfreader=PyPDF2.PdfFileReader(open(root.filename,'rb'))
                    for page_num in range(pdfreader.numPages):
                        text=pdfreader.getPage(page_num).extractText()
                        print(text)
                        speak(text)
                except:
                    print()
            elif 'text' in query:
                try:
                    root.filename = filedialog.askopenfilename(initialdir="C://Users//Dell//Documents//Projects",
                                                               title="Select text File",
                                                               filetypes=(("txt File", "*.txt"), ("all files", "*.*")))
                    file=open(root.filename,"r+")
                    text=file.read()
                    print(text)
                    speak(text)
                    file.close()
                except:
                    print()
        elif 'what' in query or 'explain' in query or 'who' in query:
            googlesearch(query)

        elif query=='exit':
            speak(random.choice(tuple(byewishing)))
            break
        else:
            googlesearch(query)