import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import pickle
import PyPDF2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- JURUS ANTI ERROR KERAS (SATPAM PENYARING LAYER) ---
# Fungsi untuk membuang variabel siluman dari layer manapun
def bersihkan_config(kwargs):
    kwargs.pop('quantization_config', None)
    return kwargs

# Kita buat versi aman untuk SEMUA layer yang dipakai AI Anda
class SafeEmbedding(Embedding):
    def __init__(self, **kwargs):
        super().__init__(**bersihkan_config(kwargs))

class SafeDense(Dense):
    def __init__(self, **kwargs):
        super().__init__(**bersihkan_config(kwargs))

class SafeLSTM(LSTM):
    def __init__(self, **kwargs):
        super().__init__(**bersihkan_config(kwargs))

class SafeDropout(Dropout):
    def __init__(self, **kwargs):
        super().__init__(**bersihkan_config(kwargs))

# 1. Membuat fondasi server
app = Flask(__name__)
CORS(app) 

print("Sedang memuat model AI dan Tokenizer, mohon tunggu...")

# 2. Memuat otak AI dengan memasang satpam ke semua layer
satpam_layer = {
    'Embedding': SafeEmbedding,
    'Dense': SafeDense,
    'LSTM': SafeLSTM,
    'Dropout': SafeDropout
}

# Load model dengan penjagaan ketat
model_ai = load_model('model_zan.h5', custom_objects=satpam_layer)

# 3. Membaca kamus kata (Tokenizer)
with open('tokenizer_sidang.pkl', 'rb') as file_kamus:
    tokenizer = pickle.load(file_kamus)

print("Status: Model AI dan Tokenizer berhasil dihidupkan!")

# 4. Membuat Pintu Masuk (Endpoint)
@app.route('/api/prediksi', methods=['POST'])
def proses_penilaian():
    # A. Pengecekan barang bawaan dari React
    if 'file_skripsi' not in request.files:
        return jsonify({"error": "File PDF skripsi tidak ditemukan!"}), 400
    
    if 'teks_mahasiswa' not in request.form:
        return jsonify({"error": "Teks presentasi mahasiswa tidak ditemukan!"}), 400

    # B. Mengambil barang bawaannya
    file_pdf = request.files['file_skripsi']
    teks_mahasiswa = request.form['teks_mahasiswa']

    # C. Ekstraksi teks dari PDF
    teks_skripsi = ""
    try:
        reader = PyPDF2.PdfReader(file_pdf)
        for page in reader.pages:
            teks_skripsi += page.extract_text()
    except Exception as e:
        return jsonify({"error": f"Gagal membaca PDF: {str(e)}"}), 500

    # D. Cek Kesesuaian / Nyambung atau Tidak (TF-IDF)
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([teks_skripsi, teks_mahasiswa])
        skor_match = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        skor_match = 0.0

    # E. Proses Penilaian Psikologi & Pemahaman (LSTM)
    sekuens = tokenizer.texts_to_sequences([teks_mahasiswa])
    siap_masuk = pad_sequences(sekuens, maxlen=100, padding='post', truncating='post')
    
    hasil_prediksi = model_ai.predict(siap_masuk, verbose=0)
    
    prob_pede = float(hasil_prediksi[0][0][0]) * 100
    prob_paham = hasil_prediksi[1][0]

    # F. Menerjemahkan Angka jadi Keputusan
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

    # G. Membungkus paket untuk React (JSON)
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
    return "<h1>Server SkripsiVibe AI Berjalan Normal! 🚀</h1><p>Gunakan endpoint POST ke <b>/api/prediksi</b> untuk menilai mahasiswa.</p>"

# 5. Tombol Power untuk menyalakan Server
if __name__ == '__main__':
    app.run(debug=True, port=8000)
