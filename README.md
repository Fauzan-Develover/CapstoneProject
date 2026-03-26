# Capstone Project

Selamat datang di repositori resmi **Capstone Project**! 
Proyek ini adalah Sistem Simulasi Sidang Skripsi Virtual berbasis AI untuk membantu mahasiswa tingkat akhir berlatih presentasi dan mengatasi *mental block* dengan menganalisis tingkat kepanikan dari suara mereka.

---

## 🌳 Arsitektur Cabang (Branching System)
Repositori ini menggunakan sistem multi-cabang agar pekerjaan tiap divisi tidak saling bertabrakan. **DILARANG KERAS MENDORONG (PUSH) KODE LANGSUNG KE `main`!**

Berikut adalah daftar *branch* dan fungsinya:
* **`main`**: Kode final yang sudah 100% jadi dan siap dinilai juri.
* **`integration`**: Ruang penggabungan. Semua fitur dari tiap divisi akan digabung dan dites di sini sebelum masuk ke `main`.
* **`fullstack`**: Ruang kerja khusus tim Front-End (React/Vite) dan Back-End (Express/FastAPI).
* **`data-science`**: Ruang kerja khusus tim Data (pengumpulan *dataset*, *cleaning*, EDA, dan *dashboard* Streamlit).
* **`ai-engineer`**: Ruang kerja khusus tim AI (pelatihan model TensorFlow, *custom callbacks*, evaluasi).

---

## 🚀 Cara Mulai Bekerja (Alur Kerja Tim)
Ikuti 4 langkah wajib ini setiap kali kamu mau mulai *coding*:

**1. Clone Repositori (Hanya dilakukan sekali di awal)**
\`\`\`bash
git clone https://github.com/Fauzan-Develover/CapstoneProject.git
cd CapstoneProject
\`\`\`

**2. Pindah ke Kamar Divisimu (WAJIB sebelum ngoding!)**
Jangan pernah *coding* di `main` atau `integration`. Langsung pindah ke *branch* divisimu:
* Tim Web: `git checkout fullstack`
* Tim Data: `git checkout data-science`
* Tim AI: `git checkout ai-engineer`

**3. Simpan dan Dorong Pekerjaan Harianmu**
Kalau tugasmu hari itu sudah selesai, simpan kodenya ke GitHub dengan cara:
\`\`\`bash
git add .
git commit -m "menambahkan fitur X"
git push origin nama-branch-kamu
\`\`\`

**4. Pull Request (PR)**
Kalau tugas mingguanmu sudah beres dan siap digabung dengan tim lain, buat **Pull Request** di web GitHub dari *branch* kamu ke *branch* `integration`.

---

## 💻 Aturan Penulisan Kode (Coding Conventions)
Agar kode kita terlihat profesional dan seragam di mata juri, kita sepakat menggunakan standar berikut:

**1. Penamaan Variabel dan Fungsi (WAJIB Bahasa Inggris)**
Gunakan format **camelCase** (huruf pertama kecil, kata selanjutnya diawali huruf besar) dan gunakan **Bahasa Inggris** untuk logika *coding*.
* ✅ **BENAR:** `studentName`, `confidenceScore`, `calculateAccuracy()`, `isUserPanic`
* ❌ **SALAH:** `nama_mahasiswa`, `SkorKepercayaan`, `hitung_akurasi()`, `userPanikGak`

**2. Teks Antarmuka (UI)**
Untuk teks yang dibaca oleh pengguna di *website* (seperti tombol, judul, atau pertanyaan dari Avatar Dosen), **tetap gunakan Bahasa Indonesia** yang baik dan benar (contoh: "Mulai Simulasi", "Skor Anda").

**3. Berikan Komentar (Comments)**
Jika kamu menulis logika yang rumit, tambahkan komentar singkat agar teman beda divisi paham maksud kodemu. (Gunakan bantuan AI kalau bingung bikin kodenya!).

---
*Let's build something awesome and make it to the Top 15!* 🔥
