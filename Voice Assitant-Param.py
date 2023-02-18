import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import json
from urllib.request import urlopen
from playsound import playsound
import webbrowser
import pywhatkit
import os
import pyjokes
import re
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",178)  

def speak(audio):
    # This Function is used to give audio output according to user input
    engine.say(audio)
    print(f"Param: \"{audio}\"\n")
    engine.runAndWait()

def wishMe():
    # This Function checks is made to greet the user based on the complete date and time information in our current Locale. This function is called at the very beginning of the program.
    hour = int(datetime.datetime.now().hour)
    if hour >= 8 and hour < 12:
        speak("Good Morning Sir!")

    elif hour >= 12 and hour < 17:
        speak("Good Afternoon Sir!")

    else:
        speak("Good Evening Sir!")

    speak("I am Param, Your Virtual Assistant")
    speak("How May I Help you Today?")

def takeCommand():
    # This Function takes microphone input from the user and returns string output, which is used in function taskExec() for further processing.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 1000
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: \"{query}\"\n")

    except Exception as e:
        speak("Sorry I couldnt catch that")
        speak("Please try again")
        taskExec()

    return query

def lastWord(str):
    # This Function helps in extracting the last word from user input in variable query, it is used for further processing. This Function helps in making the code less redundant.
    newstr = ""
    l = len(str)
    for i in range(l-1, 0, -1):
        if(str[i] == " "):
            return newstr[::-1]
        else:
            newstr = newstr + str[i]

def seclastWord(str):
    # This Function helps in extracting the second last word from user input in variable query, it is used for further processing. This Function helps in making the code less redundant.
    test = re.search('(?<=\s)\w+', str[::-1])
    return (test.group(0)[::-1])

def taskExec():
    # This Function contains all tasks the Virtual Assistant will perform for set trigger words/phrases
    while True:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if 'hello' in query or 'hi' in query:
            speak("Hello Sir, How Can I Help You")

        elif 'how are you' in query:
            speak("I am Fine, What about you?")

        elif 'i am fine' in query or 'i am good' in query:
            speak("Wonderful to Hear Sir, is there anything I can do for you")

        elif 'what is your name' in query:
            speak("My Name is Param, What's Yours?")

        elif 'my name is' in query or 'i go by' in query:
            query = query.replace("my name is","")
            query = query.replace("i go by","")
            speak("Hello"+query+" How can I help you?")
        
        elif 'wikipedia' in query:
            try:
                speak('Searching Wikipedia')
                query = query.replace("search","")
                query = query.replace("on","")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=1)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry your request cannot be processed, Please try again")

        elif 'search' in query:
            speak("Showing Search Results on Google")
            query = query.replace("search","")
            query = query.replace("for","")
            pywhatkit.search(query)
            time.sleep(15)
                
        elif 'open' in query:
            try:
                speak("Opening...")
                query = lastWord(query)
                web1 = query + '.com'
                webbrowser.open(web1)
                time.sleep(15)
            except Exception:
                speak("Sorry your request cannot be processed, Please try again")
                  
        elif 'music' in query or 'song' in query:
            speak("Ok, Playing Music")
            music_dir = r'C:\Users\Vedant\Documents\Music\Playlist'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            time.sleep(20)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the current time is {strTime}") 

        elif 'greetings to' in query:
            query=query.replace("give greetings to","")
            speak(f" Hello...{query}...Hope you have a great day ahead of you")
                          
        elif 'alarm' in query:
            speak("Alright, when for?") 
            tim = input("Param: Enter the time(in HH:MM:SS): ")
            speak("Alarm Set for "+tim)
            while True:
                Time_Ac = datetime.datetime.now().strftime("%H:%M:%S")
                if Time_Ac == tim:
                    playsound(r'C:\Users\Vedant\Documents\Music\alarm_clock.mp3')
                elif Time_Ac > tim:
                    speak("Alarm Over")
                    break
        
        elif 'timer for' in query:
            tm = (lastWord(query))
            tm1 = int((seclastWord(query)))
            if tm == "seconds":
                timer = tm1
                speak(f"Timer has been set for {tm1} seconds")
            elif tm == "minutes":
                timer = tm1 * 60
                speak(f"Timer has been set for {tm1} minutes")
            elif tm == "hours":
                timer = tm1 * 3600
                speak(f"Timer has been set for {tm1} hours")
            while timer > 0:
                time.sleep(1)
                timer -= 1
            playsound(r'C:\Users\Vedant\Documents\Music\alarm_clock.mp3')
            speak(f"Your {timer} seconds, have been completed")

        elif 'joke' in query:
            get = pyjokes.get_joke()
            speak(get)
        
        elif "where is" in query or "locate" in query:
            query = query.replace("where is", "")
            query = query.replace("locate","")
            location = query
            speak("Showing"+location+" in google maps")
            webbrowser.open("https://www.google.nl/maps/place/"+location+ "")
            time.sleep(15)

        elif 'news' in query:
            try:
                jsonObj = urlopen('''https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=da9c509c936c41c09a1d6e5df2621134''')
                data = json.load(jsonObj)
                i = 0
                speak('Here are some Top Headlines from Google News')
                print('''=============== GOOGLE NEWS ============'''+ '\n')
                for j in data['articles']:
                    speak(str(i+1) + '. ' + j['title'] + '\n')
                    print(j['description'] + '\n')
                    i += 1
                    if i == 5:
                        break
            except Exception as e:
                print(str(e))
            
        elif 'suspend' in query or 'stop listening' in query:
            tm = (lastWord(query))
            tm1 = int((seclastWord(query)))
            if tm == "seconds":
                timer = tm1
                speak(f"Suspending all activities for {tm1} seconds")
            elif tm == "minutes":
                timer = tm1 * 60
                speak(f"Suspending all activities for {tm1} minutes")
            elif tm == "hours":
                timer = tm1 * 3600
                speak(f"Suspending all activities for {tm1} hours")
            while tm1 > 0:
                time.sleep(1)
                tm1 -= 1

        elif 'bye' in query:
            speak("Bye Sir. Have a Great Day")
            exit()

        elif 'thank you' in query:
            speak("Thanks for giving me your time, Hope you have a great day ahead!")
            exit()

wishMe()
taskExec()

