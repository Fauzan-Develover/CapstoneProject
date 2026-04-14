import { useState, useRef } from 'react';

export default function SimulationPage({ setPage, question, setScore }) {
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);

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
        setLoading(true);

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        console.log(audioBlob); // nanti kirim ke backend

        setTimeout(() => {
          const randomScore = Math.floor(Math.random() * 40) + 60;
          setScore(randomScore);

          setLoading(false);
          setPage('result');
        }, 1500);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      alert('Gagal akses mikrofon');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();

    // penting: matikan mic
    mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());

    setIsRecording(false);
  };

  return (
    <div className="simulation">
      <div className="main-area">
        <div className="question-box">
          {question}
        </div>

        <div className="avatar">
          🤖 AI
        </div>
      </div>

      <div className="sidebar">
        <h3>Kontrol</h3>

        {!isRecording ? (
          <button className="btn-success" onClick={startRecording}>
            Mulai Jawab
          </button>
        ) : (
          <button className="btn-danger" onClick={stopRecording}>
            Stop Jawaban
          </button>
        )}

        {isRecording && <p>🎤 Sedang merekam...</p>}
        {loading && <p>AI sedang menganalisis...</p>}

        <button onClick={() => setPage('home')}>
          Keluar
        </button>
      </div>
    </div>
  );
}