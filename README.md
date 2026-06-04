# SkripsiVibeAI Dashboard

## Alur Kerja Dataset

Dataset yang digunakan adalah **Analisis Respons & Kepercayaan Diri Mahasiswa dalam Sidang Skripsi**. Dataset ini berbentuk CSV dan digunakan untuk menganalisis hubungan antara respons mahasiswa, tingkat kepanikan, dan penguasaan materi.

Alur kerja dataset:

1. **Gathering and Loading Data**
   Dataset dimuat dari repository GitHub ke Google Colab menggunakan library `pandas`.

2. **Assessing Data**
   Pemeriksaan kualitas data dilakukan dengan mengecek:

   * Informasi dataset
   * Missing values
   * Data duplikat
   * Keunikan kategori
   * Proporsi label
   * Ringkasan statistik
   * Panjang teks
   * Pengulangan kata
   * Noise pada kolom teks

3. **Cleaning Data**
   Data dibersihkan dengan cara:

   * Menghapus missing values pada kolom `teks`
   * Menghapus duplikasi teks
   * Memperbaiki format dan tipe data kolom `score`
   * Memfilter nilai valid pada kolom `level`
   * Membersihkan noise teks seperti karakter tidak relevan

4. **Feature Engineering**
   Membuat fitur tambahan dari kolom teks, yaitu:

   * `panjang_teks`
   * `jumlah_filler`
   * `jumlah_ulang`

5. **Exploratory Data Analysis**
   Analisis dilakukan untuk melihat pola data menggunakan:

   * Univariate Analysis
   * Bivariate Analysis
   * Multivariate Analysis

6. **Explanatory Analysis & Visualization**
   Visualisasi dibuat untuk menjawab pertanyaan bisnis terkait kepanikan, panjang jawaban, skor, jurusan, dan pola linguistik mahasiswa.

7. **Analisis Lanjutan**
   Analisis tambahan dilakukan menggunakan:

   * Clustering persona mahasiswa dengan K-Means
   * Feature importance analysis
   * Error pattern analysis
   * A/B Testing

8. **Data Output**
   Dataset akhir yang sudah dibersihkan disimpan sebagai:

```bash
data_clean_sidang_skripsi.csv
```

Jumlah data akhir:

```bash
7.971 baris data
```

---

## Notebook

Notebook Google Colab digunakan untuk proses data science, mulai dari problem statement, data wrangling, data cleaning, EDA, visualisasi, analisis lanjutan, A/B testing, hingga kesimpulan.

Nama notebook:

```bash
Capstone_Project_Data Scientist_C26-PSU183.ipynb
```

Link notebook:

```md
https://colab.research.google.com/drive/1xodPOtBqZkGuNwc-aOjm-B6eXsXKist2?usp=sharing
```

Isi notebook:

* Capstone Project
* Problem Statement
* Pertanyaan Bisnis
* Import Library
* Menghubungkan Google Colab dengan GitHub
* Data Wrangling
* Gathering and Loading Data
* Assessing Data
* Cleaning Data
* Exploratory Data Analysis
* Explanatory Data Analysis & Visualization
* Analisis Lanjutan
* A/B Testing
* Data Dictionary
* Conclusion

---

## Cara Jalankan Project

Ikuti langkah berikut untuk menjalankan project secara lokal.

### 1. Clone Repository

```bash
git clone https://github.com/lxngvr/CapstoneProject.git
```

### 2. Masuk ke Folder Project

```bash
cd CapstoneProject/dashboard
```

### 3. Install Library

```bash
pip install -r requirements.txt
```

### 4. Jalankan Streamlit

```bash
streamlit run dashboard_capstone.py
```

Setelah berhasil dijalankan, aplikasi akan terbuka pada browser melalui alamat lokal:

```bash
http://localhost:8501
```

---

## Link Deploy Streamlit

Aplikasi Streamlit dapat diakses melalui link berikut:

```md
https://skripsivibe-dashboard.streamlit.app
```

---

## Cara Menggunakan Streamlit

1. Buka aplikasi melalui link Streamlit.
2. Gunakan sidebar untuk memilih halaman dashboard.
3. Pilih program studi menggunakan filter yang tersedia.
4. Lihat ringkasan metrik utama pada halaman dashboard.
5. Buka tab visualisasi untuk melihat hasil analisis data.
6. Gunakan grafik interaktif untuk mengeksplorasi hubungan antar variabel.
7. Baca interpretasi pada setiap bagian visualisasi.
8. Gunakan halaman analisis lanjutan untuk melihat clustering, feature importance, dan hasil A/B testing.

Fitur utama dashboard:

* Tinjauan Umum
* Analisis Eksplanatori Data
* Analisis Lanjutan
* Uji A/B
* Filter Program Studi
* Grafik interaktif
* Preview dataset
* Interpretasi hasil analisis

---

## Laporan Komprehensif

Laporan komprehensif project dapat diakses melalui link berikut:

```md
https://docs.google.com/document/d/1dqrFmhtO71rK7rHtviad_PMioD9PiMV_TFKhzcNclM8/edit?usp=sharing
```

Ringkasan laporan:

### 1. Problem Statement

Project ini dibuat untuk menganalisis kesiapan mahasiswa dalam menghadapi sidang skripsi. Permasalahan utama yang dianalisis adalah kepanikan, kehilangan fokus, mental block, dan pengaruhnya terhadap kemampuan mahasiswa dalam menjawab pertanyaan sidang.

### 2. Solusi

SkripsiVibeAI dikembangkan sebagai platform simulasi sidang skripsi berbasis AI. Pengguna dapat melakukan simulasi presentasi dan sesi tanya jawab, kemudian mendapatkan feedback terkait tingkat kepercayaan diri, penguasaan materi, serta rekomendasi perbaikan.

### 3. Dataset

Dataset yang digunakan bernama:

```bash
Analisis Respons & Kepercayaan Diri Mahasiswa dalam Sidang Skripsi
```

Dataset berisi data simulasi respons mahasiswa dalam sidang skripsi.

Informasi dataset:

```bash
Format Dataset  : CSV
Jumlah Data     : 7.971 baris
Variabel Utama  : id, jurusan, teks, level, label, score
```

### 4. Pertanyaan Bisnis

Project ini menjawab beberapa pertanyaan bisnis berikut:

1. Apakah pola bahasa spontan seperti pengulangan kata dan filler words dapat menjadi indikator kecemasan mahasiswa?
2. Bagaimana korelasi panjang teks jawaban dengan tingkat kepanikan dan skor kesesuaian materi?
3. Sejauh mana kepanikan berdampak negatif terhadap skor penilaian dan pemahaman materi?
4. Apakah terdapat perbedaan tingkat kecemasan berdasarkan program studi?

### 5. Metodologi

Metodologi project meliputi:

* Data gathering
* Data assessing
* Data cleaning
* Feature engineering
* Exploratory Data Analysis
* Explanatory analysis
* A/B testing
* Clustering persona mahasiswa
* Dashboard deployment menggunakan Streamlit

### 6. Hasil Analisis

Beberapa hasil utama dari analisis:

* Filler words dan pengulangan kata dapat menjadi indikator kecemasan mahasiswa.
* Mahasiswa yang percaya diri cenderung memiliki skor lebih tinggi.
* Panjang jawaban tidak selalu menentukan skor yang tinggi.
* Kepanikan berdampak negatif terhadap kualitas jawaban.
* Faktor jurusan tidak selalu menjadi penyebab utama kepanikan.
* Clustering menghasilkan beberapa persona mahasiswa berdasarkan pola respons.

### 7. A/B Testing

A/B testing dilakukan untuk membandingkan model dengan dan tanpa fitur linguistik.

Model yang dibandingkan:

* Model A: menggunakan fitur `score`
* Model B: menggunakan `score`, `jumlah_filler`, `jumlah_ulang`, dan `panjang_teks`

Hasil:

```bash
Model Kontrol   : 85.3%
Model Treatment : 92.1%
P-Value         : 0.014
```

Kesimpulan A/B testing:

Penambahan fitur linguistik terbukti meningkatkan akurasi model dalam mengidentifikasi tingkat kepanikan mahasiswa.

### 8. Deployment

Dashboard dikembangkan menggunakan Streamlit dan dideploy melalui Streamlit Community Cloud.

File utama deployment:

```bash
dashboard_capstone.py
```

File yang dibutuhkan:

```bash
dashboard_capstone.py
requirements.txt
data_clean_sidang_skripsi.csv
```

Struktur file:

```bash
.
├── dashboard_capstone.py
├── requirements.txt
└── cleanDataset/
    └── data_clean_sidang_skripsi.csv
```

### 9. Kesimpulan

Project ini berhasil melakukan proses data science secara lengkap, mulai dari pengolahan dataset, analisis eksploratif, visualisasi, analisis lanjutan, A/B testing, hingga deployment dashboard interaktif menggunakan Streamlit.

SkripsiVibeAI Dashboard dapat membantu pengguna memahami hubungan antara kepanikan, pola bahasa, dan performa mahasiswa dalam simulasi sidang skripsi.

### 10. Rekomendasi Pengembangan

* Menambahkan data asli dari simulasi pengguna.
* Mengembangkan fitur deteksi kepanikan secara real-time.
* Menambahkan analisis suara seperti intonasi, jeda bicara, dan kecepatan berbicara.
* Meningkatkan tampilan dashboard agar lebih mudah digunakan.
* Mengembangkan sistem feedback otomatis berdasarkan persona mahasiswa.
