# Penjelasan Rinci untuk Presentasi: Eksperimen Konfigurasi Chunking

## 1. Tujuan Presentasi

Menjelaskan hasil pengujian konfigurasi chunking pada satu dokumen markdown ilmiah. Tujuan utama:

- Menentukan konfigurasi `chunk_size` dan `chunk_overlap` yang paling optimal untuk pipeline embedding.
- Menunjukkan dampak parameter chunking terhadap jumlah chunk, ukuran chunk, dan kualitas retrieval.
- Menyajikan rekomendasi yang mudah dipresentasikan.

## 2. Dataset dan Metodologi

- Dokumen yang diuji: `data/markdown/jurnal_random_forest.md`
- Chunking pipeline: `core/chunker.py`
- Metode chunking:
  - Pemisahan awal berdasar header markdown (header-based)
  - Rekursif karakter split ketika section terlalu panjang
- Parameter yang diuji:
  - `chunk_size`: panjang karakter maksimal per chunk
  - `chunk_overlap`: overlap antar chunk dalam karakter

## 3. Konfigurasi yang Diuji

|  No | chunk_size | chunk_overlap |
| --: | ---------: | ------------: |
|   1 |        500 |           100 |
|   2 |        750 |           150 |
|   3 |       1000 |           200 |
|   4 |       1250 |           250 |
|   5 |       1500 |           300 |

> Catatan: Struktur section tetap sama di semua konfigurasi, sehingga perubahan hanya berasal dari ukuran chunk dan overlap.

## 4. Hasil Eksperimen

| chunk_size | chunk_overlap | total_chunks | avg_length | min_length | max_length | text_chunks | table_chunks | references_chunks | figure_chunks | unique_sections |
| ---------: | ------------: | -----------: | ---------: | ---------: | ---------: | ----------: | -----------: | ----------------: | ------------: | --------------: |
|        500 |           100 |          176 |      352.7 |        109 |        498 |         148 |            4 |                23 |             1 |              14 |
|        750 |           150 |          118 |      537.0 |        130 |        745 |         102 |            3 |                12 |             1 |              14 |
|       1000 |           200 |           86 |      742.9 |        130 |        994 |          73 |            2 |                10 |             1 |              14 |
|       1250 |           250 |           69 |      940.8 |        130 |       1246 |          58 |            2 |                 9 |             0 |              14 |
|       1500 |           300 |           60 |     1074.9 |        130 |       1496 |          50 |            2 |                 7 |             1 |              14 |

## 5. Insight Utama

### 5.1 Pola Utama

- `total_chunks` menurun secara konsisten saat `chunk_size` meningkat.
- `avg_length` mendekati `chunk_size` seiring parameter semakin besar.
- `unique_sections` tetap 14, menunjukkan struktur dokumen tidak berubah.

### 5.2 Interpretasi

- `chunk_size=500`: sangat granular, tapi jumlah chunk tinggi. Ini meningkatkan biaya embedding dan potensi overhead retrieval.
- `chunk_size=1500`: sangat sedikit chunk, tapi ukuran panjang. Ini dapat membuat retrieval memasukkan terlalu banyak konteks sekaligus.
- `chunk_size=1000`: berada di tengah, memberikan keseimbangan antara granularitas dan efisiensi.

## 6. Rekomendasi Optimal

### Pilihan Utama

- `chunk_size = 1000`
- `chunk_overlap = 200`

### Mengapa ini direkomendasikan?

- Jumlah chunk moderat: `86` titik data.
- Ukuran rata-rata `742.9` karakter: mendekati rentang ideal.
- Ukuran maksimal masih di bawah `1000` karakter.
- Overlap `20%` menjaga kesinambungan konteks antar chunk.

## 7. Rekomendasi Alternatif

### 7.1 Untuk granularitas tinggi

- `chunk_size = 750`
- `chunk_overlap = 150`

Cocok apabila:

- Ingin jawaban dari potongan teks yang lebih kecil.
- Keakuratan spesifik lebih penting daripada biaya embedding.

### 7.2 Untuk densitas konteks lebih besar

- `chunk_size = 1250`
- `chunk_overlap = 250`

Cocok apabila:

- Ingin meminimalkan jumlah chunk.
- Menginginkan biaya indexing rendah.
- Namun, risiko kehilangan fokus lokal sedikit meningkat.


