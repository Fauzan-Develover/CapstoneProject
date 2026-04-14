import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import SimulationPage from './pages/SimulationPage';
import ResultPage from './pages/ResultPage';

export default function App() {
  const [page, setPage] = useState('home');

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [score, setScore] = useState(0);

  return (
    <>
      {page === 'home' && <HomePage setPage={setPage} />}

      {page === 'upload' && (
        <UploadPage
          setPage={setPage}
          setFile={setFile}
          setQuestion={setQuestion}
        />
      )}

      {page === 'simulation' && (
        <SimulationPage
          setPage={setPage}
          question={question}
          setScore={setScore}
        />
      )}

      {page === 'result' && (
        <ResultPage
          setPage={setPage}
          score={score}
        />
      )}
    </>
  );
}