export default function HomePage({ setPage }) {
  return (
    <div className="center">
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