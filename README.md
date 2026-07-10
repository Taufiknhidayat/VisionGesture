![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0+-green.svg?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-brightgreen.svg?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

**VisionGesture** adalah kerangka kerja (*framework*) *Computer Vision* berbasis Python yang memanfaatkan **Google MediaPipe Hands** untuk pelacakan tangan secara *real-time*. Proyek ini diimplementasikan menggunakan arsitektur modular berstandar industri dengan algoritma canggih untuk memproses geometri tangan secara stabil, presisi, dan bebas dari kedipan (*anti-flicker*).

Aplikasi ini sangat ideal sebagai fondasi pengembangan sistem cerdas seperti *Gesture Engine berbasis AI*, *Virtual Mouse control*, hingga *Air Drawing*.

---

## 🚀 Fitur Utama & Inovasi Algoritma

- **Advanced Joint Angle Detection**: Menghitung sudut rotasi antar sendi (`CMC` ➔ `MCP` ➔ `IP` ➔ `TIP`) menggunakan hukum cosinus. Algoritma ini membuat deteksi jari tetap akurat 360° meskipun tangan dimiringkan, diputar, atau terbalik.
- **Adaptive Distance Ratio**: Mengganti perbandingan piksel kaku dengan rasio dinamis (jarak pergelangan tangan ke ujung jari dibagi jarak ke sendi tengah). Deteksi tetap konsisten tanpa terpengaruh jarak tangan dari kamera.
- **Bi-Directional Anti-Flicker Filter**: Menggunakan mekanisme antrean riwayat (*history buffer frame voting*) dengan struktur data `deque` untuk menyaring fluktuasi minor (*noise*) sehingga angka hitungan pada layar sangat kokoh.
- **Real-Time Palm Orientation Tracking**: Mampu mengklasifikasikan arah hadap dan posisi telapak tangan secara geometris (`Palm Front`, `Palm Back`, `Palm Left`, `Palm Right`, `Palm Down`).
- **AI-Ready Finger State Matrix**: Menghasilkan representasi *state* biner per-jari dalam bentuk matriks array (contoh: `[1, 1, 1, 1, 1]` untuk telapak terbuka penuh) yang tersimpan langsung di objek model data sehingga siap dikonsumsi oleh lapisan kecerdasan buatan (*AI Layer*).
- **Semi-Transparent HUD UI Overlay**: Desain antarmuka grafis yang modern dan minimalis menggunakan teknik *alpha blending* dan *corner-only bounding box* yang elegan tanpa memblokir pandangan objek utama.

---

## 📁 Struktur Paket Modular

```text
VisionGesture/
│
├── configs/
│   ├── __init__.py
│   ├── colors.py          # Palet warna terpusat format BGR OpenCV
│   └── settings.py        # Pusat konfigurasi (Thresholds, Smoothing Window, FPS, dsb)
│
├── src/
│   └── visiongesture/
│       ├── __init__.py
│       ├── main.py        # Titik masuk utama aplikasi (Application Core-Loop)
│       ├── camera/
│       │   ├── __init__.py
│       │   └── camera.py  # Abstraksi OpenCV VideoCapture
│       ├── counter/
│       │   ├── __init__.py
│       │   └── finger_counter.py # Core Engine: Kalkulasi Sudut, Rasio, Orientasi & Smoothing
│       ├── detector/
│       │   ├── __init__.py
│       │   └── hand_detector.py  # Pipeline Pemrosesan MediaPipe Hands
│       ├── models/
│       │   ├── __init__.py
│       │   └── hand.py    # Dataclass representasi objek Hand dan Landmark (State & Orientation)
│       └── ui/
│           ├── __init__.py
│           ├── fps.py     # Pengukur performa framerate sistem
│           └── overlay.py # Desain HUD UI, Garis Sendi, dan Bounding Box Minimalis
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md

```

---

## 🛠️ Panduan Instalasi & Eksekusi

Berikut adalah langkah-langkah lengkap untuk mengunduh, mengonfigurasi *environment*, menginstal *library*, dan menjalankan proyek VisionGesture di komputer lokal Anda:

### 1. Kloning Repositori

Buka Terminal, Command Prompt (cmd), atau PowerShell Anda, lalu jalankan perintah berikut untuk mengunduh seluruh *source code* langsung dari GitHub:

```bash
git clone [https://github.com/taufiknhidayat/visiongesture.git](https://github.com/taufiknhidayat/visiongesture.git)
cd visiongesture

```

### 2. Buat & Aktifkan Virtual Environment (venv)

Sangat disarankan memakai *virtual environment* terisolasi agar *library* pendukung proyek ini tidak bentrok dengan *package* Python global di sistem operasi Anda. Jalankan salah satu perintah di bawah ini sesuai dengan OS yang digunakan:

* **Windows (Command Prompt / cmd):**
```cmd
python -m venv venv
.\venv\Scripts\activate

```


* **Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```


* **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 3. Instalasi Dependensi Eksternal

Setelah tanda `(venv)` aktif di baris perintah terminal Anda, pastikan `pip` berada di versi terbaru, lalu instal semua *library* eksternal yang terdaftar di dalam file `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

### 4. Jalankan Aplikasi

Jalankan file utama aplikasi dari direktori terluar (*root directory*) proyek dengan menggunakan perintah berikut:

```bash
python -m src.visiongesture.main

```

---

## ⚙️ Pusat Parameterisasi & Tuning

Kalibrasi sensitivitas deteksi dapat dilakukan secara langsung tanpa mengubah logika inti algoritma melalui file `configs/settings.py`:

```python
# configs/settings.py

# Konfigurasi Geometri & Algoritma Tingkat Lanjut
FINGER_RATIO_THRESHOLD = 1.05   # Rasio ambang batas adaptif perpanjangan jari
THUMB_ANGLE_THRESHOLD = 160.0    # Batas minimum sudut kelurusan sendi jempol (derajat)
FINGER_ANGLE_THRESHOLD = 150.0   # Batas minimum sudut kelurusan empat jari utama (derajat)
SMOOTHING_WINDOW_SIZE = 5        # Jumlah frame riwayat untuk kalkulasi filter anti-flicker

```

---

## ⌨️ Kontrol Aplikasi

* **`Q`**: Menutup jendela grafis (*window UI*) OpenCV, menghentikan tangkapan kamera, membebaskan alokasi memori, dan keluar dari aplikasi secara bersih (*graceful shutdown*).

---

## 📝 Lisensi

Proyek ini dirilis di bawah hak cipta **MIT License** - Lihat file `LICENSE` untuk rincian ketentuan hukum lebih lanjut.

```

```