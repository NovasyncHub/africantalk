from text_to_speech import tts  
from translation import translate 
from hand_tracking import track
from fastapi import FastAPI,Request

app=FastAPI()


message=track()
tr=translate(message)
print(tr)


tts(tr)