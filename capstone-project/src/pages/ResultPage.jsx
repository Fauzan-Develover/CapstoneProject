export default function ResultPage({ setPage, score }) {

  const getFeedback = () => {
    if (score > 80) return "Sangat percaya diri 🔥";
    if (score > 65) return "Cukup percaya diri 👍";
    return "Masih perlu latihan 😅";
  };

  return (
    <div className="center">
      <div className="card">
        <h2>Hasil Evaluasi</h2>

        <h3>Confidence Score: {score}%</h3>
        <p>{getFeedback()}</p>

        <button
          className="btn-primary"
          onClick={() => setPage('home')}
        >
          Kembali
        </button>
      </div>
    </div>
  );
}