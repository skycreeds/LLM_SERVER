import speech_recognition as sr
import requests
import sys
import json
import nest_asyncio
from pyngrok import ngrok
import uvicorn
import pyttsx3
import threading
engine=pyttsx3.init()
engine.setProperty('rate',100)
# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

def remove_words(text, words_to_remove):

    words = text.split()  # Split the string into a list of words
    filtered_words = [word for word in words if word not in words_to_remove]
    return " ".join(filtered_words)

def SpeakOut(words:str):
    try:
        if engine.isBusy:
            print("is busy")
            engine.stop()

        engine.say(words)
        engine.runAndWait()
    except:
        print("speak issue")
        pass

def AudioToText():
        print("starting to listening")
        with sr.Microphone() as source:
         
         r.energy_threshold=30
         r.adjust_for_ambient_noise(source=source,duration=1)
         print("listening")
         audio = r.listen(source,timeout=2)
         print("stopped")
         return r.recognize_google(audio)
    
 

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class objrecev(BaseModel):
    obj:str

@app.post("/audio")
async def create_upload_file(data:objrecev):

    print("request came")
    try:
        ans=requests.post(sys.argv[1]+"/data",data=json.dumps({"quest":AudioToText()+" "+data.obj}))
        words=ans.text
        words=words[(words.find("Answer")):]
        words=remove_words(words,["\n","<p>","</p>","<a>","</a>","\\"])
        threading.Thread(target=SpeakOut,args=(words,),daemon=True).start()
        print(words)
        return words
    except:
        print("try,audio issue")
        pass

    

@app.post("/link")
async def send_linkto_main(data:objrecev):
    print(data.obj)
    requests.post(sys.argv[1]+"/link",data=json.dumps({"quest":data.obj}))



port = 8000
ngrok_tunnel = ngrok.connect(port)

print('Public URL:', ngrok_tunnel.public_url)


nest_asyncio.apply()

# finally run the app
uvicorn.run(app, port=port)
