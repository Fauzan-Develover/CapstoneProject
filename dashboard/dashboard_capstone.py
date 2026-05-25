import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy import stats
import warnings
import re
warnings.filterwarnings('ignore')

# Konfig Halaman
st.set_page_config(
    page_title="Dashboard Analisis Kecemasan Mahasiswa | SkripsiVibe AI",
    page_icon="assets/skripsivibeAI-logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stMetric {
        background-color: var(--secondary-background-color); 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .stMetric:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# Loading Data
@st.cache_data
def load_and_prep_data():
    try:
        df = pd.read_csv('finalDataset/data_clean_sidang_skripsi.csv')
        
        if df['score'].dtype == 'object':
            df['score'] = df['score'].str.replace(',', '.').astype(float)
            
        if 'panjang_teks' not in df.columns:
            df['panjang_teks'] = df['teks'].astype(str).apply(lambda x: len(x.split()))
        if 'jumlah_filler' not in df.columns:
            df['jumlah_filler'] = df['teks'].astype(str).apply(lambda x: sum([len(re.findall(fr'\b{fw}\b', str(x).lower())) for fw in ['eee', 'eh', 'anu', 'emm']]))
        if 'jumlah_ulang' not in df.columns:
            df['jumlah_ulang'] = df['teks'].astype(str).apply(lambda x: len(re.findall(r'\b(\w+)\s+\1\b', str(x).lower())))
            
    except FileNotFoundError:
        st.warning("File 'cleanDataset/data_clean_sidang_skripsi.csv' tidak ditemukan. Menggunakan Dummy Data.")
        np.random.seed(42)
        n = 7971
        level = np.random.choice([0, 1], size=n, p=[0.4, 0.6]) # 0=Tenang, 1=Panik
        label = np.random.choice([1, 2, 3], size=n)
        jurusan = np.random.choice(['Informatika', 'Hukum', 'Ilmu Komunikasi', 'Kedokteran', 'PGSD', 'Keperawatan'], size=n)
        
        score = np.where(level == 1, np.random.uniform(0.1, 0.6, n), np.random.uniform(0.5, 0.95, n))
        panjang_teks = np.where(level == 1, np.random.poisson(30, n), np.random.poisson(100, n))
        jumlah_filler = np.where(level == 1, np.random.poisson(2, n), np.random.poisson(0.5, n))
        jumlah_ulang = np.where(level == 1, np.random.poisson(2.5, n), np.random.poisson(0.3, n))
        
        df = pd.DataFrame({'id': range(1, n+1), 'jurusan': jurusan, 'teks': ['dummy text'] * n,
                           'level': level, 'label': label, 'score': score, 
                           'panjang_teks': panjang_teks, 'jumlah_filler': jumlah_filler, 'jumlah_ulang': jumlah_ulang})

    # Labeling Level
    LEVEL_MAP = {0: '0 (Tenang)', 1: '1 (Panik)'}
    df['level_desc'] = df['level'].map(LEVEL_MAP)
    
    # Pre-Compute K-Means
    fitur_cluster = df[['panjang_teks', 'score', 'jumlah_filler']].copy()
    scaler = StandardScaler()
    fitur_scaled = scaler.fit_transform(fitur_cluster)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster_persona'] = kmeans.fit_predict(fitur_scaled)
    
    persona_map = {
        0: "0: The Inaccurate but Fluent",
        1: "1: The Confident Expert",
        2: "2: The Verbose Rambler"
    }
    df['Nama_Persona'] = df['cluster_persona'].map(persona_map)
    
    # Labeling Anxious Genius
    df['kelompok_analisis'] = 'Mahasiswa Lainnya'
    anxious_genius_idx = df[(df['score'] > 0.75) & (df['level'] == 1)].index
    df.loc[anxious_genius_idx, 'kelompok_analisis'] = 'Anxious Genius (Pintar tapi Panik)'

    return df

# Load Data
df_clean = load_and_prep_data()

# Konstanta Warna
COLOR_MAP = {'0 (Tenang)': '#4C72B0', '1 (Panik)': '#DD8452'} 

# Sidebar Navigasi dan Global Filter
st.sidebar.image("assets/skripsivibeAI-logo.png", width=200)
st.sidebar.title("Dashboard")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Tinjauan Umum", 
     "Analisis Eksplanatori Data", 
     "Analisis Lanjutan", 
     "Uji A/B (Signifikansi)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Interaktif")
# Filter Jurusan Interaktif
pilihan_jurusan = st.sidebar.multiselect(
    "Filter Berdasarkan Program Studi:",
    options=sorted(df_clean['jurusan'].unique()),
    default=sorted(df_clean['jurusan'].unique())
)

if not pilihan_jurusan:
    st.error("Silakan pilih minimal satu program studi di sidebar!")
    st.stop()

df_filtered = df_clean[df_clean['jurusan'].isin(pilihan_jurusan)]

st.sidebar.markdown("---")
st.sidebar.info("**Capstone Project CC26-PSU183**\n\nDashboard ini menyajikan analisis dampak *speech disfluency* terhadap penilaian presentasi akademik.")

# Halaman 1 - Tinjauan Umum
if menu == "Tinjauan Umum":
    st.title("SkripsiVibe AI : Virtual Thesis Defense Simulator")
    st.subheader("Evaluasi Kesiapan Mental & Kepercayaan Diri Berbasis AI")
    st.markdown("Selamat datang di *interactive dashboard* untuk eksplorasi dataset pola linguistik dan psikologis mahasiswa.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sampel Tersaring", f"{len(df_filtered):,}")
    col2.metric("Program Studi Terpilih", len(pilihan_jurusan))
    col3.metric("Rata-rata Skor", f"{df_filtered['score'].mean():.2f}")
    col4.metric("Rata-rata Kata", f"{df_filtered['panjang_teks'].mean():.0f}")
    
    st.markdown("### Preview Dataset Interaktif")
    st.dataframe(df_filtered[['id', 'jurusan', 'teks', 'level_desc', 'score', 'panjang_teks', 'jumlah_filler', 'Nama_Persona']].head(50), use_container_width=True)

# Halaman 2 - Analisis  Eksplanatori
elif menu == "Analisis Eksplanatori Data":
    st.title("Analisis Eksplanatori Data")
    st.caption("Semua grafik di bawah ini menyesuaikan dengan filter Program Studi di sidebar.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Linguistik", "Korelasi Jawaban", "Dampak Penilaian", "Kerentanan Jurusan"])
    
    with tab1:
        st.subheader("Validitas Pola Bahasa sebagai Indikator Kepanikan")
        rata_linguistik = df_filtered.groupby('level_desc')[['jumlah_filler', 'jumlah_ulang']].mean().reset_index()
        rata_melt = rata_linguistik.melt(id_vars='level_desc', var_name='Indikator', value_name='Rata_Rata')
        
        fig1 = px.bar(rata_melt, x='Indikator', y='Rata_Rata', color='level_desc', barmode='group',
                      color_discrete_map=COLOR_MAP,
                      labels={'Rata_Rata': 'Rata-rata per Jawaban', 'level_desc': 'Status Presentasi'},
                      title="Penggunaan Filler Words & Pengulangan Kata")
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.expander("Lihat Interpretasi Data"):
            st.markdown("* **Dominasi Speech Disfluency:** Mahasiswa kategori Panik memiliki rata-rata penggunaan kata pengisi dan pengulangan jauh di atas mahasiswa Percaya Diri.\n* **Validitas Mental:** Tekanan mental membuat otak kesulitan menyusun kalimat, sehingga mulut memproduksi gangguan (filler) untuk membeli waktu berpikir.")
            
    with tab2:
        st.subheader("Korelasi Panjang Teks dan Skor Kesesuaian")
        fig2 = px.scatter(df_filtered, x='panjang_teks', y='score', color='level_desc', 
                          opacity=0.6, color_discrete_map=COLOR_MAP, hover_data=['jurusan'],
                          title="Persebaran Kelancaran vs Kualitas Jawaban",
                          labels={'panjang_teks': 'Panjang Teks (Jumlah Kata)', 'score': 'Skor Kesesuaian'})
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("Lihat Interpretasi Data"):
            st.markdown("* **Mental Block:** Titik oranye (Panik) mendominasi area kiri bawah, mengindikasikan jawaban pendek dengan skor rendah.\n* **Korelasi Positif:** Titik biru (Tenang) menyebar ke kanan atas. Ketenangan memberi ruang untuk mengartikulasikan jawaban kompleks yang berkorelasi dengan skor optimal.")

    with tab3:
        st.subheader("Efek Penutup (Masking Effect) Kompetensi")
        fig3 = px.box(df_filtered, x='label', y='score', color='level_desc',
                      color_discrete_map=COLOR_MAP,
                      title="Degradasi Skor Akibat Kepanikan di Tiap Level Kepahaman",
                      labels={'label': 'Tingkat Kepahaman (1=Kurang, 2=Paham, 3=Sangat Paham)', 'score': 'Skor'})
        st.plotly_chart(fig3, use_container_width=True)
        
        with st.expander("Lihat Interpretasi Data"):
            st.markdown("* Pada semua tingkat pemahaman, mahasiswa panik konsisten mendapat skor lebih rendah.\n* **Kesenjangan Ekstrem:** Mahasiswa berlabel 'Sangat Paham' (Label 3) namun panik, bisa kehilangan poin drastis hingga setara dengan mahasiswa yang kurang paham. Kepanikan menciptakan bias penilaian.")

    with tab4:
        st.subheader("Persentase Kepanikan Berdasarkan Jurusan")
        cross_jurusan = pd.crosstab(df_filtered['jurusan'], df_filtered['level_desc'], normalize='index') * 100
        if '1 (Panik)' in cross_jurusan.columns:
            cross_jurusan = cross_jurusan.reset_index().sort_values(by='1 (Panik)', ascending=True)
        else:
            cross_jurusan = cross_jurusan.reset_index()
            
        fig4 = px.bar(cross_jurusan, x=[c for c in ['0 (Tenang)', '1 (Panik)'] if c in cross_jurusan.columns], y='jurusan', orientation='h',
                      color_discrete_map=COLOR_MAP,
                      title="Kerentanan Kecemasan Berdasarkan Program Studi",
                      labels={'value': 'Persentase Mahasiswa (%)', 'jurusan': 'Program Studi', 'variable': 'Status'})
        st.plotly_chart(fig4, use_container_width=True)
        
        with st.expander("Lihat Interpretasi Data"):
            st.markdown("* **Fokus Intervensi:** Tuntutan *public speaking* di jurusan humaniora/komunikasi justru seringkali memberikan beban mental ekstra saat ujian.\n* **Ketahanan Mental:** Mahasiswa eksakta menunjukkan persentase ketenangan tertinggi (warna biru terpanjang).")

# Halaman 3 - Analisis Lanjutan (Clustering)
elif menu == "Analisis Lanjutan":
    st.title("Analisis Lanjutan & Segmentasi Persona")
    st.caption("Data K-Means dan Anomali diproses secara komprehensif, namun grafik menyesuaikan dengan filter Jurusan di sidebar.")
    
    st.markdown("### 1. Feature Importance Berdasarkan Korelasi Statistik")
    fitur_numerik = ['panjang_teks', 'score', 'jumlah_filler', 'jumlah_ulang']
    kor = abs(df_filtered[fitur_numerik + ['level']].corr()['level'].drop('level', errors='ignore')).sort_values(ascending=True)
    
    fig_corr = px.bar(x=kor.values, y=kor.index, orientation='h', 
                      title="Kekuatan Fitur dalam Mendeteksi Kepanikan (Korelasi Absolut)",
                      labels={'x': 'Nilai Korelasi Absolut', 'y': 'Fitur'})
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.info("""
    **Insight Interpretasi Feature Importance (Korelasi Absolut):**
    * **Indikator Kinerja Utama sebagai Prediktor Terkuat:** Parameter **Skor Kesesuaian (`score`)** dan **Panjang Teks (`panjang_teks`)** memiliki korelasi absolut tertinggi terhadap kepanikan. Ini membuktikan bahwa dampak utama dari kepanikan *mental block* adalah penurunan tajam pada jumlah kata yang mampu diproduksi.
    * **Fitur Linguistik sebagai Faktor Pendukung:** Frekuensi pengulangan (`jumlah_ulang`) dan kata jeda (`jumlah_filler`) menempati posisi menengah-bawah. Hal ini logis karena respons kepanikan mahasiswa beragam; ada yang banyak menggunakan *filler* (gugup), namun banyak pula yang murni *freezing* (terdiam).
    """)
    
    st.markdown("---")
    st.markdown("### 2. Segmentasi Persona dengan K-Means Clustering")
    
    color_map_kmeans = {
        "0: The Inaccurate but Fluent": "#023EFF", 
        "1: The Confident Expert": "#FF7C00",      
        "2: The Verbose Rambler": "#1AC938"        
    }
    
    fig_cluster = px.scatter(df_filtered, x='panjang_teks', y='score', color='Nama_Persona',
                             color_discrete_map=color_map_kmeans,
                             hover_data=['jurusan', 'jumlah_filler'], opacity=0.7,
                             title="Pemetaan Persona Berdasarkan Kelancaran dan Akurasi",
                             labels={'panjang_teks': 'Panjang Teks / Jumlah Kata', 'score': 'Skor (Akurasi)'})
    
    fig_cluster.update_traces(marker=dict(size=9, line=dict(width=0.5, color='white')))
    st.plotly_chart(fig_cluster, use_container_width=True)
    
    st.markdown("#### Karakteristik Rata-Rata Tiap Persona (Berdasarkan Filter Saat Ini)")
    tabel_karakteristik = df_filtered.groupby('Nama_Persona')[['panjang_teks', 'score', 'jumlah_filler', 'level']].mean().round(2)
    st.dataframe(tabel_karakteristik, use_container_width=True)
    
    st.info("""
    **Insight Interpretasi Karakteristik Tiap Cluster:**
    * **Cluster 0: "The Inaccurate but Fluent"** (Skor sedang, ketenangan rendah, berbicara cukup panjang, filler sangat sedikit).
    * **Cluster 1: "The Confident Expert"** (Skor tertinggi, tingkat ketenangan sangat tinggi, berbicara efisien, filler nyaris nol).
    * **Cluster 2: "The Verbose Rambler"** (Jumlah kata terbanyak, filler ekstrem tinggi, akurasi paling rendah - menutupi kepanikan dengan banyak bicara).
    """)
    
    st.markdown("---")
    st.markdown("### 3. Error Pattern: Penemuan 'The Anxious Genius'")
    
    anxious_filtered = df_filtered[df_filtered['kelompok_analisis'] == 'Anxious Genius (Pintar tapi Panik)']
    rata_keseluruhan = df_filtered['panjang_teks'].mean()
    
    colA, colB, colC = st.columns(3)
    colA.metric("Total 'Paham tapi Panik'", f"{len(anxious_filtered)} Baris")
    
    avg_filler = anxious_filtered['jumlah_filler'].mean() if len(anxious_filtered) > 0 else 0
    avg_len = anxious_filtered['panjang_teks'].mean() if len(anxious_filtered) > 0 else 0
    
    colB.metric("Rata-rata Filler", f"{avg_filler:.2f}")
    colC.metric("Rata-rata Panjang Teks", f"{avg_len:.2f}", f"Total Rata: {rata_keseluruhan:.2f}")
    
    category_order = ['Anxious Genius (Pintar tapi Panik)', 'Mahasiswa Lainnya']
    fig_ag = px.box(df_filtered, x='kelompok_analisis', y='panjang_teks', color='kelompok_analisis',
                    category_orders={'kelompok_analisis': category_order},
                    color_discrete_sequence=['#BDC3C7', '#DD8452'], 
                    title="Perbandingan Kelancaran Verbal (Jumlah Kata)",
                    labels={'kelompok_analisis': 'Kategori Mahasiswa', 'panjang_teks': 'Jumlah Kata per Jawaban'})
    
    fig_ag.update_layout(height=500, margin=dict(t=50, b=50, l=50, r=50))
    st.plotly_chart(fig_ag, use_container_width=True)
    
    st.info("""
    **Insight Error Pattern Analysis (Berdasarkan Fakta Data):**
    * **Stabilitas Verbal di Bawah Tekanan:** Berbeda dengan ekspektasi awal, kelompok Anomali ini ternyata memiliki rata-rata jumlah kata yang stabil di atas rata-rata keseluruhan. Penguasaan materi yang matang mencegah terjadinya *mental block*.
    * **Sindrom "Robotic Delivery" (Ketiadaan Jeda Natural):** Penggunaan *filler words* pada kelompok ini menyentuh angka mutlak **0.00**. Ketiadaan kata jeda mengindikasikan penyampaian yang sangat kaku, cepat, dan tidak natural (menghafal kaku / membaca).
    * **Implikasi pada Penilaian AI / Penguji:** AI mendeteksi "kepanikan" pada kelompok ini bukan karena mereka gagap, melainkan karena **hilangnya ritme bicara natural yang komunikatif**.
    """)

# Halaman 4 - Uji A/B Signifikansi
elif menu == "Uji A/B (Signifikansi)":
    st.title("Uji A/B: Signifikansi Dampak Speech Disfluency")
    
    st.markdown("""
    Pengujian Hipotesis (*Welch's T-Test*) untuk membuktikan secara matematis apakah penggunaan kata pengisi (filler) berdampak signifikan terhadap anjloknya nilai objektif.
    
    * **Grup A (Control):** Mahasiswa Lancar (Filler $\le$ 1)
    * **Grup B (Variant):** Mahasiswa Tersendat (Filler > 1)
    * **Metrik Kesuksesan:** Skor Kesesuaian (0.0 - 1.0)
    """)
    
    group_a = df_filtered[df_filtered['jumlah_filler'] <= 1]['score']
    group_b = df_filtered[df_filtered['jumlah_filler'] > 1]['score']
    
    if len(group_a) == 0 or len(group_b) == 0:
        st.warning("Data tidak mencukupi untuk membandingkan kedua grup. Silakan sesuaikan filter program studi.")
    else:
        t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
        uplift = ((group_a.mean() - group_b.mean()) / group_b.mean()) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric(f"Skor Rata-Rata (Grup A)", f"{group_a.mean():.3f}")
        col2.metric(f"Skor Rata-Rata (Grup B)", f"{group_b.mean():.3f}", f"{-abs(uplift):.1f}%")
        
        if p_value < 0.05:
            col3.metric("P-Value (Signifikansi)", f"{p_value:.5f}", "Signifikan (H0 Ditolak)")
            st.success(f"KESIMPULAN: Perbedaan skor sangat signifikan secara statistik (P-Value < 0.05). Mahasiswa yang lancar memiliki performa skor {uplift:.1f}% lebih tinggi.")
        else:
            col3.metric("P-Value", f"{p_value:.5f}", "Tidak Signifikan", delta_color="inverse")
            st.warning("KESIMPULAN: Tidak terdapat perbedaan skor yang signifikan antara kedua kelompok.")
            
        st.markdown("### Distribusi Kepadatan Skor")
        import plotly.figure_factory as ff
        
        hist_data = [group_a.values, group_b.values]
        group_labels = ['Grup A (Lancar)', 'Grup B (Tersendat)']
        colors = ['#4C72B0', '#DD8452']
        
        try:
            fig_ab = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)
            fig_ab.update_layout(title_text='Distribusi Kepadatan Skor Kesesuaian Materi', 
                                 xaxis_title='Skor Kesesuaian', yaxis_title='Density')
            st.plotly_chart(fig_ab, use_container_width=True)
        except Exception as e:
            st.info("Kepadatan distribusi tidak dapat digambar karena variansi data terlalu kecil untuk filter tersebut.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Capstone Project CC26-PSU183 - Dashboard Analytics")
