# VisionGesture

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0+-green.svg?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-brightgreen.svg?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

**VisionGesture** adalah aplikasi berbasis Python yang memanfaatkan teknologi *Computer Vision* dan implementasi *Machine Learning* dari Google MediaPipe untuk mendeteksi tangan (Hand Tracking) secara real-time melalui kamera. Aplikasi ini mampu mengenali sisi tangan (Kiri/Kanan), memetakan 21 titik landmark, menentukan koordinat titik tengah, serta menghitung jumlah jari yang terbuka secara akurat.

---

## 🚀 Fitur Utama

- **Real-Time Hand Tracking & Landmark Mapping**: Deteksi hingga 2 belah tangan secara simultan dengan visualisasi 21 koordinat titik sendi (*landmarks*).
- **Automated Finger Counter**: Menghitung jumlah jari yang terbuka secara dinamis dengan algoritma komparasi spasial sumbu koordinat.
- **Dynamic Overlay UI**: Menampilkan informasi status aplikasi secara bersih (FPS Counter, ID Tangan, Sisi Tangan, Koordinat Titik Tengah, dan Total Jari keseluruhan).
- **Modular & Clean Architecture**: Struktur kode yang rapi, terpisah berdasarkan fungsionalitas komponen (Camera, UI, Models, Detector, Counter), menjadikannya mudah dirawat (*scalable*).
- **Camera Mirroring Support**: Mode kamera selfie otomatis yang menyesuaikan akurasi deteksi sisi tangan kanan dan kiri secara presisi.

---

## 📁 Struktur Direktori Proyek

```text
VisionGesture/
│
├── configs/
│   ├── __init__.py
│   ├── colors.py          # Definisi palet warna BGR OpenCV
│   └── settings.py        # Konfigurasi dimensi frame, FPS, sensitivitas, & kamera
│
├── src/
│   └── visiongesture/
│       ├── __init__.py
│       ├── main.py        # Titik masuk utama aplikasi (Application Core Loop)
│       ├── camera/
│       │   ├── __init__.py
│       │   └── camera.py  # Abstraksi OpenCV VideoCapture
│       ├── counter/
│       │   ├── __init__.py
│       │   └── finger_counter.py # Logika kalkulasi perhitungan jari terbuka
│       ├── detector/
│       │   ├── __init__.py
│       │   └── hand_detector.py  # Pipeline MediaPipe Hands Processing
│       ├── models/
│       │   ├── __init__.py
│       │   └── hand.py    # Dataclasses representasi objek Hand dan Landmark
│       └── ui/
│           ├── __init__.py
│           ├── fps.py     # Logika penghitung performa framerate (FPS)
│           └── overlay.py # Pengolahan grafis rendering teks dan bounding box
│
├── .gitignore
├── requirements.txt       # Daftar dependensi modul eksternal
└── README.md