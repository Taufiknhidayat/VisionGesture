# VisionGesture

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0+-green.svg?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-brightgreen.svg?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

**VisionGesture** adalah kerangka kerja (*framework*) *Computer Vision* berbasis Python yang memanfaatkan **Google MediaPipe Hands** untuk pelacakan tangan secara *real-time*. Proyek ini diimplementasikan menggunakan arsitektur modular (*Clean Architecture & Event-Driven*) berstandar industri dengan algoritma canggih untuk memproses geometri tangan secara stabil, presisi, dan bebas dari kedipan (*anti-flicker*).

---

## 🚀 Modul Terintegrasi & Fitur Utama

### 1. Core Gesture Engine & Hand Tracking
- **Advanced Joint Angle Detection**: Kalkulasi sudut rotasi antar sendi (Hukum Cosinus) untuk deteksi jari yang akurat 360°.
- **Adaptive Distance Ratio**: Deteksi konsisten tanpa terpengaruh jarak tangan dari kamera.
- **Bi-Directional Anti-Flicker Filter**: Mekanisme antrean riwayat (*history buffer voting*) untuk hasil yang solid dan stabil.
- **Hungarian Centroid Tracker**: Pelacakan Hand ID tingkat militer yang mengunci ID secara permanen meskipun tangan saling bersilangan.
- **Motion Tracker**: Pengenalan pergerakan dinamis seperti *Swipe Left, Right, Up, Down*, dan *Zoom In/Out* (Multi-hand).

### 2. Virtual Mouse Controller
Mengendalikan kursor komputer sepenuhnya menggunakan gestur tangan di udara dengan dukungan multimonitor dan penghalus gerak (*Smoothing Filter*).

### 3. Smart Air Drawing
Kanvas virtual interaktif untuk menggambar di udara yang dilengkapi antarmuka pengguna cerdas (*Palette UI*) dan ekspor otomatis ke format Transparan PNG dan PDF.

### 4. Real-time System Dashboard
Panel UI bergaya *High-Tech* transparan di sisi kiri layar untuk memonitor:
- **FPS (Frame Per Second)**
- **CPU & RAM Usage** (via *psutil*)
- **Active Module**
- **Hand ID, Gesture State, & Confidence Score**

---

## 🖐️ Kamus Gestur (Gesture Dictionary)

Sistem ini mengenali berbagai bentuk gestur tangan. Berikut adalah panduan bentuk fisik tangan Anda dan fungsinya di setiap modul:

| Nama Gestur | Bentuk Fisik Jari Tangan | Fungsi di Virtual Mouse | Fungsi di Air Drawing |
| :--- | :--- | :--- | :--- |
| **INDEX** | Hanya jari Telunjuk terbuka, sisanya mengepal. | Menggerakkan Kursor | Menggambar / Mencoret |
| **OK** | Ujung Jempol & Telunjuk menempel (menjepit). | *Left Click & Drag* | - |
| **PEACE** | Jari Telunjuk & Tengah terbuka (huruf V). | *Right Click* | Melayang (*Hover*) & Pilih Warna |
| **ROCK** | Jari Telunjuk & Kelingking terbuka (Metal). | *Double Click* | - |
| **FIST** | Semua jari mengepal rapat. | - | Menghapus seluruh kanvas (*Clear*) |
| **THUMB UP** | Hanya Jempol yang menunjuk ke atas. | - | Batal (*Undo*) |
| **THUMB DOWN** | Hanya Jempol yang menunjuk ke bawah. | - | Ulangi (*Redo*) |
| **LOVE** | Jempol, Telunjuk, Kelingking terbuka (Spiderman).| - | Simpan Gambar (Export PNG & PDF)|
| **OPEN HAND**| Telapak tangan terbuka penuh (Lima jari). | Siaga (*Standby*) | Siaga (*Standby*) |
| **SWIPE** | Gerakkan `OPEN HAND` dengan cepat ke atas/bawah. | *Scroll Mouse* (Naik/Turun)| - |

---

## 📁 Struktur Paket Modular

```text
VisionGesture/
│
├── configs/
│   ├── colors.py          # Palet warna terpusat
│   └── settings.py        # Pusat konfigurasi tuning & threshold
│
├── src/visiongesture/
│   ├── camera/            # Abstraksi OpenCV VideoCapture
│   ├── counter/           # Algoritma geometri & orientasi telapak tangan
│   ├── detector/          # Pipeline MediaPipe & pembungkus kelas model
│   ├── drawing/           # Smart Canvas & integrasi export file
│   ├── gesture/           # Event-driven Gesture Engine & History Buffer
│   ├── models/            # Dataclass (Hand, Landmark, Gesture)
│   ├── tracker/           # Centroid Tracker (Hungarian Alg) & Motion Engine
│   ├── ui/                # Dashboard, FPS counter, Overlay Bounding Box
│   ├── virtual_mouse/     # PyAutoGUI Cursor Controller & Smoother
│   └── main.py            # Application Core-Loop & Hotkey Switcher
│
├── assets/exports/        # Folder output penyimpanan PNG/PDF (Otomatis dibuat)
├── requirements.txt
└── README.md

```

---

## 🛠️ Panduan Instalasi & Eksekusi

### 1. Kloning Repositori

```bash
git clone [https://github.com/taufiknhidayat/visiongesture.git](https://github.com/taufiknhidayat/visiongesture.git)
cd visiongesture

```

### 2. Konfigurasi Lingkungan Virtual (*Virtual Environment*)

* **Windows (Command Prompt / cmd):**
```cmd
python -m venv venv
.\venv\Scripts\activate

```


* **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 3. Instalasi Dependensi & Menjalankan Aplikasi

```bash
pip install --upgrade pip
pip install -r requirements.txt
python -m src.visiongesture.main

```

---

## ⌨️ Kontrol Hotkey Aplikasi

Tekan tombol berikut pada *keyboard* Anda saat aplikasi berjalan untuk berpindah mode:

* **`M`** : Mengaktifkan Mode **Virtual Mouse**
* **`D`** : Mengaktifkan Mode **Air Drawing**
* **`T`** : Mengaktifkan Mode **Tracking Engine** (Hanya deteksi)
* **`Q`** : Keluar aplikasi

---

## 📝 Lisensi

Proyek ini dirilis di bawah hak cipta **MIT License** - Lihat file `LICENSE` untuk rincian ketentuan hukum lebih lanjut.