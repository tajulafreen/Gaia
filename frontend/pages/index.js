import React, { useState } from "react";
import "../styles/globals.css";
export default function Home() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");

  const startRecording = () => {
    setRecording(true);
    // TODO: Whisper AI integration yahan aayegi
  };

  const stopRecording = () => {
    setRecording(false);
    setTranscript("This is a sample transcription from Whisper AI."); // Placeholder text
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4 text-amber-400">
        AI Voice Input Social App
      </h1>
      <div className="p-4 bg-white shadow-md rounded-lg">
        <button
          onClick={recording ? stopRecording : startRecording}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg"
        >
          {recording ? "Stop Recording" : "Start Recording"}
        </button>
        {transcript && (
          <p className="mt-4 p-2 bg-gray-200 rounded-lg">{transcript}</p>
        )}
      </div>
    </div>
  );
}
