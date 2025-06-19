from fastapi.responses import StreamingResponse 
from fastapi import FastAPI ,UploadFile ,File
from pydantic import BaseModel
import io 
import scipy.io.wavfile 
import numpy as np 
from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import os 
import tempfile
from hand_tracking import track

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = VitsModel.from_pretrained("facebook/mms-tts-yor")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")
model.to(device)

app=FastAPI()
class TTSInput(BaseModel):
    text:str

@app.post("/tss")
async def stream_audio(data:TTSInput):
    inputs=tokenizer(data.text,return_tensors='pt')
    inputs={k: v.to(model.device) for k,v in inputs.items()}

    with torch.no_grad():
        output=model(**inputs).waveform 

    waveform=output.squeeze().cpu().numpy()
    
    buf=io.BytesIO()
    scipy.io.wavfile.write(buf,rate=model.config.sampling_rate,data=(waveform*32767).astype(np.int16))
    buf.seek(0)

    return StreamingResponse(buf,media_type='audio/wav')



@app.post('/video_tss')
async def videod_to_speech(file:UploadFile=File(...)):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".mp4") as tmp_video:
        tmp_video.write(await file.read())
        tmp_video_path=tmp_video.name
    try:
        text=track(tmp_video_path)
        inputs=tokenizer(text,return_tensors='pt')
        inputs={k: v.to(model.device) for k,v in inputs.items()}

        with torch.no_grad():
            output=model(**inputs).waveform 

        waveform=output.squeeze().cpu().numpy()
        
        buf=io.BytesIO()
        scipy.io.wavfile.write(buf,rate=model.config.sampling_rate,data=(waveform*32767).astype(np.int16))
        buf.seek(0)
        print("It's work")
        return StreamingResponse(buf,media_type='audio/wav')

    except:
        return "Lecture impossible"
    finally:
        os.remove(tmp_video_path)




if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # fallback sur 8000 localement
    uvicorn.run("streaming:app", host="0.0.0.0", port=port)
