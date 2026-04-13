import React, { useState, useRef } from 'react';
import './style.css';

export default function App() {
  const [page, setPage] = useState('home'); // home | upload | simulation | result
  const [isRecording, setIsRecording] = useState(false);
  const [question, setQuestion] = useState("Jelaskan latar belakang penelitian Anda");

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();

        // simulasi hasil AI
        setTimeout(() => {
          setPage('result');
        }, 1000);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error(error);
      alert('Gagal akses mikrofon');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  // ================= HOME =================
  if (page === 'home') {
    return (
        <div className="center">  {/* 👈 INI WRAPPER */}
            <div className="card">
                <h1>SkripsiVibe AI</h1>
                <p>Simulasi Sidang Skripsi Virtual berbasis AI</p>
                <button 
                className="btn-primary"
                onClick={() => setPage('upload')}
                >
                Mulai Simulasi
                </button>
            </div>
        </div>
        );
    }

  // ================= UPLOAD =================
  if (page === 'upload') {
    return (
        <div className="center"> {/* 👈 DI SINI JUGA */}
            <div className="card">
                <h2>Upload File Skripsi (PDF)</h2>
                <input type="file" />
                <button
                onClick={() => setPage('simulation')}
                className="btn-success"
                >
                Lanjut ke Simulasi
                </button>
            </div>
        </div>
        );
    }

  // ================= SIMULATION =================
  if (page === 'simulation') {
    return (
      <div className="h-screen w-full bg-gray-900 text-white flex flex-col">
        <div className="flex flex-1">
          <div className="flex-1 bg-black flex items-center justify-center relative">

            {/* Pertanyaan AI */}
            <div className="absolute top-4 bg-black/60 px-4 py-2 rounded">
              {question}
            </div>

            {/* Avatar AI */}
            <div className="absolute bottom-4 right-4 bg-gray-700 p-3 rounded-xl">
              🤖 AI
            </div>
          </div>

          {/* Sidebar */}
          <div className="w-64 bg-gray-800 p-4">
            <h2 className="mb-4">Kontrol</h2>

            {!isRecording ? (
              <button
                onClick={startRecording}
                className="w-full bg-green-500 py-2 rounded mb-2"
              >
                Mulai Jawab
              </button>
            ) : (
              <button
                onClick={stopRecording}
                className="w-full bg-red-500 py-2 rounded mb-2"
              >
                Stop Jawaban
              </button>
            )}

            <button
              onClick={() => setPage('home')}
              className="w-full bg-gray-600 py-2 rounded"
            >
              Keluar
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ================= RESULT =================
  if (page === 'result') {
    return (
        <div className="center"> {/* 👈 DI SINI JUGA */}
        <div className="card">
            <h2>Hasil Evaluasi</h2>
            <p>Confidence Score: 82%</p>
            <p className="result-text">Kamu cukup percaya diri 👍</p>

            <button
            onClick={() => setPage('home')}
            className="btn-primary"
            >
            Kembali
            </button>
        </div>
        </div>
    );
    }
}
