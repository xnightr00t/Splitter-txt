# 🚀 Text Splitter Python 2/3

[![Python Version](https://img.shields.io/badge/python-2.7%20%7C%203.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/xnightr00t/Splitter-txt)

Aplikasi **Text Splitter** yang simple, cepat, dan user-friendly untuk memecah file teks (.txt) besar menjadi bagian-bagian kecil.

## ✨ Fitur Utama

### 🎯 **3 Metode Split**
- **📊 Split by Lines** - Pecah berdasarkan jumlah baris
- **💾 Split by Size** - Pecah berdasarkan ukuran file (MB)
- **🔢 Split by Parts** - Pecah menjadi jumlah bagian tertentu

### 🛡️ **Anti-Overwrite**
- Otomatis rename jika file sudah ada
- Format: `filename(1).txt`, `filename(2).txt`, dst.
- Tidak akan menimpa file yang sudah ada

### 🔧 **Cross-Platform**
- ✅ Python 2.7+
- ✅ Python 3.x
- ✅ Windows, macOS, Linux
- ✅ UTF-8 encoding support
- ✅ Auto-detect encoding

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/xnightr00t/Splitter-txt.git
cd text-splitter

# Jalankan aplikasi
python splitter-text.py
```

### Untuk Windows
```bash
pip install colorama
```

## 📖 Cara Penggunaan

1. **Jalankan aplikasi**
   ```bash
   python splitter-text.py
   ```

2. **Masukkan nama file**
   ```
   📂 Masukkan nama file .txt:
   » list.txt
   ```

3. **Pilih metode split**
   ```
   📋 PILIH METODE SPLIT:
   1️⃣  Split berdasarkan jumlah baris
   2️⃣  Split berdasarkan ukuran file (MB)
   3️⃣  Split menjadi jumlah bagian tertentu
   ```

4. **Selesai!** File akan terpecah otomatis

## 🎯 Contoh Penggunaan

### Split by Lines (1000 baris per file)
```bash
Input: document.txt (50,000 baris)
Output: 
├── document_part001.txt (1,000 baris)
├── document_part002.txt (1,000 baris)
├── ...
└── document_part050.txt (1,000 baris)
```

### Split by Size (10MB per file)
```bash
Input: largefile.txt (100MB)
Output:
├── largefile_part001.txt (10MB)
├── largefile_part002.txt (10MB)
├── ...
└── largefile_part010.txt (10MB)
```

### Split by Parts (5 bagian)
```bash
Input: data.txt (25,000 baris)
Output:
├── data_part001.txt (5,000 baris)
├── data_part002.txt (5,000 baris)
├── data_part003.txt (5,000 baris)
├── data_part004.txt (5,000 baris)
└── data_part005.txt (5,000 baris)
```

### Main Interface
```
🚀 TEXT SPLITTER PYTHON 2/3 🚀
================================

📂 Masukkan nama file .txt:
» list.txt
✓ File ditemukan!

📋 INFORMASI FILE:
📁 File: list.txt
📊 Ukuran: 15.32 MB (16,058,240 bytes)
📄 Total baris: 125,430

📋 PILIH METODE SPLIT:
1️⃣  Split berdasarkan jumlah baris
2️⃣  Split berdasarkan ukuran file (MB)
3️⃣  Split menjadi jumlah bagian tertentu
```

### Progress Output
```
ℹ Memulai split berdasarkan jumlah baris...
→ Membuat file: list_part001.txt
→ Membuat file: list_part002.txt
⚠ File list_part003.txt sudah ada, menggunakan list_part003(1).txt
→ Membuat file: list_part003(1).txt
✓ File berhasil dipecah menjadi 3 bagian!

🎉 PROSES SELESAI! 🎉
```
