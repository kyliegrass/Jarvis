#Python program to translate
# Speech-to-text and text-to-speech
import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI KEY HERE - Won't work without)

import openai
openai.api_key = OPENAI_KEY

#Function to convert text to
#speech
def SpeakText(command):

    #Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

#Initialize the recognizer
r= sr.Recognizer()

def record_text():
#Loop in case of errors
    while(1):
        try:
            #Use the microphone as a source for input
            with sr.Microphone() as source2:

                #Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening...")

                #Listens for the user's input
                audio2 = r.listen(source2)

                #Using Google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(
        model=model, #gpt-3.5-turbo
        messages=messages, #array, full context we want GPT to respond to
        max_tokens=100, #how long do we want this message to be in characters
        n=1, #default
        stop=None, #default
        temperature=0.5, #default
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = []
while(1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    SpeakText(response)

    print(response)

#This project requires the following pip install
#pip3 install python-dotenv
#pip3 install pyttsx3
#pip3 install openai
