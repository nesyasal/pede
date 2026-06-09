# Hasil Eksperimen Konfigurasi Chunking

Eksperimen dilakukan pada file markdown `data/markdown/jurnal_random_forest.md` menggunakan fungsi `chunk_markdown` di `core/chunker.py`. Konfigurasi yang diuji terdiri dari lima kombinasi `chunk_size` dan `chunk_overlap`.

## Tabel Hasil Chunking

| chunk_size | chunk_overlap | num_chunks | avg_length | min_length | max_length | text_chunks | table_chunks | references_chunks | figure_chunks | unique_sections |
| ---------: | ------------: | ---------: | ---------: | ---------: | ---------: | ----------: | -----------: | ----------------: | ------------: | --------------: |
|        500 |           100 |        176 |      352.7 |        109 |        498 |         148 |            4 |                23 |             1 |              14 |
|        750 |           150 |        118 |      537.0 |        130 |        745 |         102 |            3 |                12 |             1 |              14 |
|       1000 |           200 |         86 |      742.9 |        130 |        994 |          73 |            2 |                10 |             1 |              14 |
|       1250 |           250 |         69 |      940.8 |        130 |       1246 |          58 |            2 |                 9 |             0 |              14 |
|       1500 |           300 |         60 |     1074.9 |        130 |       1496 |          50 |            2 |                 7 |             1 |              14 |

## Analisis Hasil

1. `unique_sections` sama untuk semua konfigurasi (14), karena pemisahan berdasar header markdown tetap konsisten.
2. Semakin besar `chunk_size`, jumlah chunk berkurang. Ini menurunkan overhead jumlah embedding dan pencarian, tetapi membuat setiap chunk lebih panjang.
3. `chunk_size=500` menghasilkan banyak chunk (176) dengan ukuran rata-rata kecil. Ini bagus bila ingin konteks sangat granular, tetapi dapat meningkatkan biaya embedding dan mengurangi efisiensi pencarian.
4. `chunk_size=1500` menghasilkan paling sedikit chunk (60), tetapi ukuran maksimal mencapai hampir 1.5k karakter. Chunk seukuran ini berpotensi memasukkan terlalu banyak konteks sekaligus saat retrieval.
5. Konfigurasi `1000/200` menawarkan keseimbangan terbaik:
   - Jumlah chunk moderat: 86
   - Ukuran rata-rata mendekati batas ideal ~750 char
   - Ukuran maksimum masih di bawah 1000 char
   - Overlap 20% menjaga transisi konteks antar chunk

## Rekomendasi Optimal

Untuk uji coba konfigurasi chunking yang paling optimal pada dataset ini, rekomendasi utama adalah:

- `chunk_size = 1000`
- `chunk_overlap = 200`

Alasan:

- Menjaga jumlah chunk pada tingkat wajar tanpa membuat chunk terlalu kecil atau terlalu besar.
- Mengurangi jumlah metadata dan vektor yang harus diindeks dibandingkan konfigurasi lebih kecil.
- Mempertahankan granularitas yang baik untuk pemulihan konteks tanpa kehilangan detail di potongan teks.

## Catatan Tambahan

- Jika tujuan utama adalah pencarian yang lebih mahal dengan konteks maksimum per chunk, konfigurasi `1250/250` dapat dipertimbangkan sebagai alternatif "lebih padat".
- Jika fokus adalah memaksimalkan granularitas dan precision pada jawaban sangat spesifik, konfigurasi `750/150` atau `500/100` bisa digunakan, tetapi perlu diperhatikan overhead jumlah chunk.
- Seksi `references` masih terhitung dalam hasil ini. Jika ingin mengecualikan referensi dari database embedding, jumlah chunk total akan berkurang sesuai nilai `references_chunks` masing-masing konfigurasi.
