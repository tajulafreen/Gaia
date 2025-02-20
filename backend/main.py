import whisper
import os
from fastapi import FastAPI, File, UploadFile
from pydub import AudioSegment
import uvicorn

app = FastAPI()

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # ✅ Save uploaded file
        temp_audio_path = f"temp_{file.filename}"
        with open(temp_audio_path, "wb") as f:
            f.write(await file.read())

        if not os.path.exists(temp_audio_path):
            return {"error": "File not saved!"}

        # ✅ Convert MP3 to WAV if needed
        if temp_audio_path.endswith(".mp3"):
            wav_path = temp_audio_path.replace(".mp3", ".wav")
            audio = AudioSegment.from_file(temp_audio_path)
            audio.export(wav_path, format="wav")
        else:
            wav_path = temp_audio_path

        # ✅ Load Whisper Model
        model = whisper.load_model("base")

        # ✅ Transcribe with timestamps
        result = model.transcribe(wav_path, word_timestamps=True)

        # ✅ Speech Detection Filter
        if len(result["text"].strip()) == 0:
            return {"error": "No speech detected! 🎵 This is likely a music file."}

        # ✅ Remove Duplicates
        unique_sentences = []
        seen = set()
        for sentence in result["text"].split(". "):  # Split by sentence
            if sentence not in seen:
                unique_sentences.append(sentence)
                seen.add(sentence)

        cleaned_text = ". ".join(unique_sentences)

        # ✅ Extract words with timestamps
        words_with_timestamps = []
        for segment in result["segments"]:
            for word in segment["words"]:
                words_with_timestamps.append({
                    "word": word["word"],
                    "start": word["start"],
                    "end": word["end"]
                })

        # ✅ Cleanup temp files
        os.remove(temp_audio_path)
        if temp_audio_path != wav_path:
            os.remove(wav_path)

        return {"transcription": cleaned_text, "timestamps": words_with_timestamps}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
