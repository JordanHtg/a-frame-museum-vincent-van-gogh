# 🎨 Museum Seni Vincent Van Gogh — Virtual 3D Exhibition

![Version](https://img.shields.io/badge/Version-1.1.0-gold)
![Platform](https://img.shields.io/badge/Platform-WebXR%20%7C%20A--Frame%20%7C%20Three.js-blue)
![Audio](https://img.shields.io/badge/Audio-Beethoven%20F%C3%BCr%20Elise%20(Piano%20%26%20Biola)-purple)
![License](https://img.shields.io/badge/License-MIT-green)

Selamat datang di **Museum Seni Vincent Van Gogh**, sebuah pameran seni virtual 3D interaktif berbasis **A-Frame**, **Three.js**, dan **WebXR** yang dirancang secara profesional dengan nuansa museum elegan, artistik, dan hangat.

---

## ✨ Fitur Unggulan

- 🏛️ **Desain Museum Modern & Elegan**: Palet warna hangat khas galeri seni kelas dunia (`#F7F1E5`, `#DDB967`, `#8B5E3C`, `#5A3E2B`, `#F2D8A7`, `#FFF8EE`) lengkap dengan pilar, lantai kayu herringbone, pencahayaan directional hangat, dan sorotan spotlight pada tiap karya seni. Dinding area exit bersih tanpa papan billboard hitam.
- 🖼️ **Karya Seni Ikonik Lengkap dengan Frame 3D**:
  - *The Starry Night* (1889)
  - *Sunflowers* (1888)
  - *Bedroom in Arles* (1888)
- 🎻 **Audio Latar Beethoven — Für Elise (Piano & Biola / Violin)**: Sistem sintesis suara **Web Audio API** polifonik yang memainkan melodi klasik *Für Elise* dengan paduan merdu **Piano Akustik** dan **Biola (Violin)** secara otomatis tanpa membutuhkan file eksternal tambahan.
- 🗿 **Rotunda 3D Vincent Van Gogh**: Karakter 3D bergaya low-poly artistik yang berputar perlahan 360° dan mengambang secara halus.
- 🟡 **Interactive Golden Floating Spheres (Raycaster 1 Detik)**: Setiap karya dilengkapi bola emas transparan beranimasi naik-turun di depannya. Arahkan pointer ke bola emas selama 1 detik untuk memunculkan **Panel Informasi Glassmorphism** beranimasi halus.
- 👶 **Sudut Pandang Anak Kecil 6 Tahun (Tinggi Mata 1.12m)**: Kamera pemain diatur dekat dengan lantai setinggi anak umur 6 tahun, menghadirkan sudut pandang museum yang agung, imersif, dan unik.
- ⚡ **Langsung Masuk Tanpa Intro Screen**: Saat website dibuka, pengunjung langsung berada di dalam museum virtual siap untuk menjelajah.
- 🚶 **First Person Controller & Lompat Fisika (WASD + Mouse Look + SPACE)**:
  - Tekan `W`, `A`, `S`, `D` untuk berjalan melintasi galeri.
  - Gerakkan **Mouse** untuk melihat sekeliling (didukung *Pointer Lock*).
  - Tekan tombol **SPACE** untuk melompat secara realistis dengan gravitasi.
- 🔵 **Senjata / Projectile Shooter (Klik Kiri)**: Tembakkan bola energi biru bercahaya yang meluncur cepat menggunakan arsitektur **Object Pooling** berkinerja tinggi 60 FPS.

---

## 🎨 Cara Mudah Mengganti Gambar Lukisan (Bingkai 3D & Panel Informasi)

Sistem telah dilengkapi mekanisme **sinkronisasi otomatis**. Untuk mengganti gambar lukisan yang tampil di **Bingkai 3D Galeri** dan **Panel Informasi**:

1. Buka file [`script.js`](file:///C:/Users/gurse/Documents/A-Frame%203D/script.js).
2. Temukan objek `MUSEUM_CATALOG` di bagian atas file:
   ```javascript
   const MUSEUM_CATALOG = {
     "starry-night": {
       title: "The Starry Night",
       year: "1889",
       image: "assets/images/starry_night.png", // <-- Cukup ganti path atau URL gambar di sini
       ...
     }
   }
   ```
4. **Selesai!** Gambar pada Bingkai 3D di dinding museum dan gambar pada Panel Informasi otomatis berubah serentak (tampil **utuh 100% tanpa terpotong**).

---

## 🎵 Cara Mengganti Audio Latar Belakang dengan File MP3 Sendiri

Jika Anda memiliki file audio/lagu MP3 hasil download Anda sendiri dan ingin memutarnya sebagai musik latar museum:

1. Letakkan file MP3 Anda ke dalam folder [`assets/audio/`](file:///C:/Users/gurse/Documents/A-Frame%203D/assets/audio) (misal: `lagu_museum.mp3`).
2. Buka file [`script.js`](file:///C:/Users/gurse/Documents/A-Frame%203D/script.js) dan cari baris di bagian paling atas:
   ```javascript
   const CUSTOM_AUDIO_PATH = "";
   ```
3. Ubah menjadi path file MP3 Anda:
   ```javascript
   const CUSTOM_AUDIO_PATH = "assets/audio/lagu_museum.mp3";
   ```
4. **Selesai!** Website akan otomatis memutar lagu MP3 Anda secara berulang (loop). Jika dikosongkan kembali (`""`), museum akan otomatis memutar sintesis klasik **Beethoven — Für Elise (Piano & Biola)**.

---

## 📂 Struktur Project

```text
/
├── index.html                  # Struktur utama WebXR & Museum 3D Scene (tanpa billboard hitam)
├── style.css                   # Antarmuka HUD Glassmorphism & Responsif
├── script.js                   # Sintesis Für Elise (Piano & Biola), Raycaster & Sync Gambar
├── assets/
│   ├── images/                 # Karya seni & lukisan Van Gogh
│   │   ├── starry_night.png
│   │   ├── sunflowers.png
│   │   └── bedroom_in_arles.png
│   ├── models/                 # Model 3D format GLB
│   │   ├── van_gogh_character.glb
│   │   ├── museum_bench.glb
│   │   └── flower_pot.glb
│   └── textures/               # Tekstur lantai kayu, dinding museum, & frame emas
│       ├── wood_floor.png
│       ├── wall_plaster.png
│       └── gold_frame.png
└── README.md                   # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan Project Secara Lokal

### Opsi 1: Menggunakan VS Code Live Server (Direkomendasikan)
1. Buka folder project di **Visual Studio Code**.
2. Klik kanan pada file [`index.html`](file:///C:/Users/gurse/Documents/A-Frame%203D/index.html).
3. Pilih **Open with Live Server**.
4. Website akan terbuka secara otomatis di browser pada `http://127.0.0.1:5500`.

### Opsi 2: Langsung Buka File `index.html`
1. Klik dua kali file [`index.html`](file:///C:/Users/gurse/Documents/A-Frame%203D/index.html) pada File Explorer Anda.
2. Museum virtual siap dinikmati langsung di browser modern (Chrome, Edge, Firefox, Safari).

---

## 🌐 Panduan Deploy ke Vercel & GitHub

1. Unggah / Push repository ini ke akun **GitHub** Anda.
2. Buka dasbor [Vercel](https://vercel.com/) dan klik **Add New Project**.
3. Hubungkan akun GitHub Anda dan pilih repository **Museum Seni Vincent Van Gogh**.
4. Klik **Deploy**. Website Anda langsung live!

---

## 🎮 Panduan Kontrol

| Tombol / Aksi | Fungsi |
| :--- | :--- |
| **W, A, S, D** / **Panah** | Berjalan maju, kiri, mundur, kanan |
| **Mouse Look** | Melihat sekeliling ruang museum |
| **SPACE** | Melompat dengan fisika gravitasi |
| **Klik Kiri Mouse** | Menembakkan proyektil biru (Object Pool) |
| **Arahkan Crosshair 1s** | Memeriksa informasi lukisan & patung Van Gogh |
| **Tombol Suara HUD** | Menyalakan / mematikan musik klasik Für Elise (Piano & Biola) |
# a-frame-museum-vincent-van-gogh
