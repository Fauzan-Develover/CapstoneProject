import { useState } from 'react';

export default function UploadPage({ setPage, setFile, setQuestion }) {
  const [localFile, setLocalFile] = useState(null);

const handleSubmit = () => {
  if (!localFile) {
    alert('Upload file dulu!');
    return;
  }

  const isPDF =
    localFile.type === 'application/pdf' ||
    localFile.name.toLowerCase().endsWith('.pdf');

  if (!isPDF) {
    alert('File harus berupa PDF!');
    return;
  }

  if (localFile.size > 5 * 1024 * 1024) {
    alert('Ukuran file maksimal 5MB!');
    return;
  }

  setFile(localFile);

  setTimeout(() => {
    setQuestion("Jelaskan latar belakang penelitian Anda");
    setPage('simulation');
  }, 1000);

    // simulasi API generate pertanyaan
    setTimeout(() => {
      setQuestion("Jelaskan latar belakang penelitian Anda");
      setPage('simulation');
    }, 1000);
  };

  return (
    <div className="center">
      <div className="card">
        <h2>Upload File Skripsi (PDF)</h2>

        <input
          type="file"
          onChange={(e) => setLocalFile(e.target.files[0])}
        />

        <br /><br />

        <button
          className="btn-success"
          onClick={handleSubmit}
        >
          Lanjut ke Simulasi
        </button>
      </div>
    </div>
  );
}