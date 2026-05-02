import pickle
import PyPDF2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

from keras import layers, Model
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app) 

print("Sedang membangun Arsitektur AI dan memuat Otak (Weights), mohon tunggu...")

def build_model(vocab_size=10000, max_length=100):
    input_text = layers.Input(shape=(max_length,), name="input_teks")
    embedding = layers.Embedding(input_dim=vocab_size, output_dim=64)(input_text)
    lstm_layer = layers.Bidirectional(layers.LSTM(64, return_sequences=False))(embedding)
    
    dense_1 = layers.Dense(32, activation='relu')(lstm_layer)
    dropout = layers.Dropout(0.3)(dense_1)
    dense_2 = layers.Dense(16, activation='relu')(dropout)
    
    output_level = layers.Dense(1, activation='sigmoid', name="prediksi_level")(dense_2)
    output_label = layers.Dense(3, activation='softmax', name="prediksi_label")(dense_2)
    
    model = Model(inputs=input_text, outputs=[output_level, output_label])
    return model

model_ai = build_model()

model_ai.load_weights('model_zan.keras')

with open('tokenizer_sidang.pkl', 'rb') as file_kamus:
    tokenizer = pickle.load(file_kamus)

print("Status: Model AI dan Tokenizer berhasil dihidupkan!")

@app.route('/api/prediksi', methods=['POST'])
def proses_penilaian():
    if 'file_skripsi' not in request.files:
        return jsonify({"error": "File PDF skripsi tidak ditemukan!"}), 400
    
    if 'teks_mahasiswa' not in request.form:
        return jsonify({"error": "Teks presentasi mahasiswa tidak ditemukan!"}), 400

    file_pdf = request.files['file_skripsi']
    teks_mahasiswa = request.form['teks_mahasiswa']

    teks_skripsi = ""
    try:
        reader = PyPDF2.PdfReader(file_pdf)
        for page in reader.pages:
            teks_skripsi += page.extract_text()
    except Exception as e:
        return jsonify({"error": f"Gagal membaca PDF: {str(e)}"}), 500

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([teks_skripsi, teks_mahasiswa])
        skor_match = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        skor_match = 0.0

    sekuens = tokenizer.texts_to_sequences([teks_mahasiswa])
    siap_masuk = pad_sequences(sekuens, maxlen=100, padding='post', truncating='post')
    
    hasil_prediksi = model_ai.predict(siap_masuk, verbose=0)
    
    prob_pede = float(hasil_prediksi[0][0][0]) * 100
    prob_paham = hasil_prediksi[1][0]

    if prob_pede >= 50:
        keputusan_pede = "Percaya Diri"
    else:
        keputusan_pede = "Gugup / Panik"

    daftar_label = ["Gak Paham", "Lumayan Paham", "Sangat Paham"]
    index_jawaban = np.argmax(prob_paham)
    
    if skor_match < 0.02: 
        keputusan_paham = "TIDAK NYAMBUNG (Out of Topic)"
    else:
        keputusan_paham = daftar_label[index_jawaban]

    hasil_akhir = {
        "status": "success",
        "kesesuaian_skripsi_persen": round(skor_match * 100, 2),
        "skor_percaya_diri_persen": round(prob_pede, 2),
        "status_psikologis": keputusan_pede,
        "status_pemahaman": keputusan_paham
    }

    return jsonify(hasil_akhir), 200

@app.route('/', methods=['GET'])
def halaman_utama():
    return "<h1>Server SkripsiVibe AI Berjalan Normal!</h1><p>Gunakan endpoint POST ke <b>/api/prediksi</b> untuk menilai mahasiswa.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=8000)