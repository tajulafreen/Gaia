import whisper
import os
from fastapi import File, UploadFile
from pydub import AudioSegment
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download NLTK lexicon (if not already downloaded)
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def transcribe_audio(file: UploadFile):
    try:
        # Save uploaded file
        temp_audio_path = f"temp_{file.filename}"
        with open(temp_audio_path, "wb") as f:
            f.write(file.file.read())

        if not os.path.exists(temp_audio_path):
            return {"error": "File save nahi hui!"}

        # Convert MP3 to WAV if needed
        if temp_audio_path.endswith(".mp3"):
            wav_path = temp_audio_path.replace(".mp3", ".wav")
            audio = AudioSegment.from_file(temp_audio_path)
            audio.export(wav_path, format="wav")
        else:
            wav_path = temp_audio_path

        # Load Whisper Model
        model = whisper.load_model("base")
        result = model.transcribe(wav_path, word_timestamps=True)  # ✅ Fix: Word timestamps enabled

        # Speech Detection Filter
        transcript_text = result["text"].strip()
        if len(transcript_text) == 0:
            return {"error": "No speech detected! 🎵 This is likely a music file."}

        # ✅ Extract words with timestamps (Fix: Check if "segments" exists)
        words_with_timestamps = []
        if "segments" in result:
            for segment in result["segments"]:
                if "words" in segment:  # ✅ Fix: Ensure "words" key exists
                    for word in segment["words"]:
                        words_with_timestamps.append({
                            "word": word["word"],
                            "start": word["start"],
                            "end": word["end"]
                        })

        # ✅ Sentiment Analysis
        sentiment_score = sia.polarity_scores(transcript_text)
        if sentiment_score["compound"] >= 0.05:
            sentiment = "Positive 😊"
        elif sentiment_score["compound"] <= -0.05:
            sentiment = "Negative 😡"
        else:
            sentiment = "Neutral 😐"

        # Cleanup temp files
        os.remove(temp_audio_path)
        if temp_audio_path != wav_path:
            os.remove(wav_path)

        return {
            "transcription": transcript_text,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "words_with_timestamps": words_with_timestamps
        }

    except Exception as e:
        return {"error": str(e)}
