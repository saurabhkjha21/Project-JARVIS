import speech_recognition as sr # pip install SpeechRecognition
import webbrowser # python standard library
import pyttsx3 # pip install pyttsx3
import musicLibrary # user-defined file with song links
import requests # pip install requests
from openai import OpenAI # pip install openai
from gtts import gTTS # pip install gTTS
import pygame # pip install pygame
import os # for file operations
import datetime # for date and time

'''You can install all required modules in one line:
pip install SpeechRecognition pyttsx3 requests openai gTTS pygame
'''

# global variables
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "10ea18249c094b348b1a369aea7f9a64" # put your newsapi key here
openai_key = "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" # put your OpenAI key here


# speak using gTTS, fallback to pyttsx3 if fails
def speak(text):
    try:
        if not text.strip():
            return  # skip if empty

        tts = gTTS(text=text, lang='en')
        filename = "temp.mp3"
        tts.save(filename)

        # play the audio
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # stop and clean up
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(filename)
    except Exception as e:
        print("Speech error:", e)
        engine.say(text)
        engine.runAndWait()


# function to handle OpenAI API
def aiProcess(command):
    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
        model="openrouter/cypher-alpha:free",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa, Siri and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content


# function to process user commands
def processCommand(c):
    c_low = c.lower()  # convert to lowercase for easy comparison

    if "open google" in c_low:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in c_low:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c_low:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c_low:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif c_low.startswith("play"):
        song = c_low.replace("play", "").strip()  # extract song name
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            speak(f"Playing {song}")
            if link.startswith("http"):
                webbrowser.open(link)
            else:
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load(link)
                    pygame.mixer.music.play()
                except Exception as e:
                    speak("Sorry, I couldn't play the song.")
                    print("Music error:", e)
        else:
            speak(f"I couldn't find the song {song}")

    elif "time" in c_low:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "date" in c_low:
        today = datetime.datetime.today().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    elif "news" in c_low:
        speak("Fetching latest news headlines")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # read only top 5 headlines
                speak(article['title'])
        else:
            speak("Sorry, I can't access the news right now.")

    elif c_low in ["stop", "exit", "shutdown", "quit"]:
        speak("Shutting down. Goodbye.")
        exit()  # exits the program

    else:
        # send command to OpenAI if not matched
        output = aiProcess(c)
        speak(output)


# main code execution
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=4)

            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("Error;", e)
