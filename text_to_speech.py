from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import sounddevice as sd

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = VitsModel.from_pretrained("facebook/mms-tts-yor")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")
model.to(device)

def tts(text="Ọrọìwòye tu vas"):
    inputs = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model(**inputs).waveform

    output=output.squeeze().cpu().numpy()
    sd.play(output,samplerate=model.config.sampling_rate)
    sd.wait()
    scipy.io.wavfile.write(f"{text[:3]}.wav",
                            rate=model.config.sampling_rate, data=output)
