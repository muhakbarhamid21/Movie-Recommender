# Movie Recommender

## Latar Belakang
Industri film saat ini sudah menjadi industri yang terbilang besar. terdapat 4,734,693 judul, yang diantaranya terdapat judul TV series, film pendek, documenter dan sebagainya. Perkembangan industri film juga berkembang pesat. Seiring dengan berkembangnya teknologi yang digunakan dalam pembuatan film. Tidak hanya dari segi plot cerita, film saat ini harus memiliki sisi visual yang membuat konsumen terkagum saat menontonnya. Saat ini menonton film merupakan suatu hiburan alternatif dalam mengusir kebosanan. Tidak sedikit juga seseorang menonton film karena memang hobi. Hal ini menuntut industri film untuk menghadapi persaingan ketat dalam menciptakan terobosan baru guna memenuhi kebutuhan konsumen yang semakin beragam.<br/>
Dewasa ini, website yang berisi video dan komunitas film, seperti Netflix, MovieLens, YouTube dan sebagainya, sudah sangat populer saat ini. Pada website tersebut memiliki banyak user dan kemudian user tersebut bisa memberi penilaian terhadap film yang tersedia. Melihat review terlebih dahulu merupakan salah satu cara untuk mengetahui kualitas dari film tersebut. Namun, banyaknya jumlah user yang memberi review berbedabeda pada suatu film membuat pembaca kebingungan dalam menyimpulkan review tersebut.<br/>
Selera setiap orang pasti berbeda. Seseorang bisa menyukai film berdasarkan genre, aktor atau rumah produksi. Hal ini yang menjadi permasalahan seseorang dalam menentukan film yang sesuai dengan ekspektasi. Mengingat jumlah film yang begitu banyak dan beragam jenisnya, seseorang tentu tidak memiliki cukup waktu untuk memeriksa sinopsis atau trailer satu per satu. Belum lagi jika ada film baru yang belum diketahui judulnya. Maka dari itu harapan seseorang adalah menginginkan rekomendasi film yang sesuai harapan dari berbagai aspek dengan efektifitas waktu yang maksimal.<br/>
Maka aplikasi yang bisa memberikan rekomendasi film kepada pengguna sangat diperlukan untuk mendapatkan rekomendasi film yang sesuai dengan keinginan. Content-based filtering dan Collaborative filtering adalah pendekatan yang paling umum untuk membangun sebuah sistem rekomendasi.<br/>
Collaborative filtering adalah suatu konsep dimana opini dari pengguna lain yang ada digunakan untuk memprediksi item yang mungkin disukai/diminati oleh seorang pengguna. Sedangkan content-based filtering menggunakan ketersediaan konten sebuah item sebagai basis dalam pemberian rekomendasi.<br/>
Berdasarkan penjelasan diatas, maka penulis membuat sistem rekomendasi film menggunakan content-based filtering dan collaborative sistem sebagai algoritma yang digunakan.

## Metode
- Content-based Filtering
- Collaborative System

## Gambaran Umum Sistem
Sistem rekomendasi yang dibangun merupakan aplikasi berbasis web yang menggunakan bahasa pemrograman Python, HTML, CSS, Javascripts, Framework Bootstrap dan Django. DBMS yang digunakan adalah Neo4J berbasis graph database dengan menggunakan query Cypher. Data yang digunakan yaitu dataset movie recommender. Sistem ini memiliki 4 menu utama yaitu menu rekomendasi, movie, tag dan rate.

## Implementasi

### Halaman Beranda
<p align="center">
<img src="https://user-images.githubusercontent.com/72149133/178533116-8074a5e0-6a8f-4d2c-82af-b9e73ea46d1a.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178533155-52efcf34-3cd7-4ed7-a83a-0c86ca9cbe10.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178533162-fc5a2d0d-80e7-433d-9fe4-14a739b5ca8f.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178533170-7b214064-0845-4596-9f81-d469fbbaf65b.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178533129-14acd880-3a6d-437a-847d-4399ab8b1706.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178533140-92f992c7-017f-44b2-a85d-2504455f44a5.png" width="300" height="160">
</p>

### Halaman Autentikasi
<p align="center">
<img src="https://user-images.githubusercontent.com/72149133/178533145-3fc618b6-04c4-422f-87fc-e1f4b488a0c0.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178533150-bf1fa841-dc17-4de9-a702-220944d59891.jpg" width="300" height="160">
</p>

### Halaman Utama Sistem Rekomendasi
<p align="center">
<img src="https://user-images.githubusercontent.com/72149133/178538624-0615d3da-2bcc-4337-a0d6-853576ec8ae2.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538655-7d628c6f-c8d2-4f04-bd33-3aca0dcaf9fb.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538666-4320a1bc-0e7f-4d0f-b26d-02b430a6c8cf.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538676-7af4ecad-b1a4-49b6-98c8-106a1c62221d.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538691-0cac7f9b-6d23-45d5-8135-892cd6d04214.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538707-bc73b92d-a64e-41bd-9ce2-970432c3471d.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538721-4dc30335-49eb-4e76-920e-348d87d9da4b.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538739-abe714a2-8977-4e57-8d66-0a908b71edcb.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538773-a7ef3b69-fcf4-4a28-b189-2d0f8868bfed.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538786-b109c242-81ac-4bc4-960a-876577815b5f.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538798-bb8fea13-145b-4954-b2e8-9186ba4399f4.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538810-3ec99667-3beb-454b-8c33-e317d5bfe503.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538822-bafde171-fea7-489d-bfb7-ebe3117390ee.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538838-f940366f-6d2a-4782-a1da-37641f35aa6e.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538848-0427db5c-54d4-470a-834d-dad8782cba0f.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538858-e68466db-3c30-4d10-9f7b-2ec4c8eaf841.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538868-5b7e4525-8696-44de-b610-ad1a083e43f7.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538881-25a8e687-9dee-49a6-84df-e5713372e2da.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538894-53566942-faba-4dda-8a39-bb6330ffb9e3.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538906-300c1f30-4d7b-4cc4-b894-80acba455899.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538915-2cece951-511a-45c9-95f0-a474020055e9.jpg" width="300" height="160">
<img src="https://user-images.githubusercontent.com/72149133/178538928-533418da-7ba1-42d1-a282-3624e995f366.jpg" width="300" height="160">
</p>

## Basis Data
Basis data yang digunakan adalah basis data berbentuk graph atau biasa disebut dengan graph database dan dalam penerapan graph database yang digunakan adalah menggunakan Neo4j.
![graph](https://user-images.githubusercontent.com/72149133/178528621-cc1dedae-c13e-4109-8dd5-596263878d67.png)<br/>
Grafik properti yang digunakan dalam sistem rekomendasi adalah sebagai berikut:
- 49 Node: User (9), Movie (14), Genre (12), dan Link (14).
- 575 Edge: givesRating (64), isTaggedBy (452), hasLink (14), dan hasGenre (45).
- Node User mempunyai 3 properti: ID, Password dan Role.
- Node Movie mempunyai 3 properti: ID, Title, dan Genre.
- Node Genre mempunyai 1 properti: name.
- Node Link mempunyai 2 properti: IMDB_ID dan TMDB_ID.
- Edge givesRating mempunya 2 properti: Rating dan TimeStamp.
- Edge isTaggedBy mempunyai 2 properti: Tag dan TimeStamp.
- Edge hasLink tidak mempunyai properti.
- Edge hasGenre tidak mempunyai properti

## Kesimpulan
Sistem rekomendasi merupakan suatu aplikasi untuk menyediakan dan merekomendasikan suatu item dalam membuat suatu keputusan yang diinginkan oleh pengguna dan dalam hal ini yang ditampilkan adalah rekomendasi film. Dalam project ini sistem rekomendasi film menggunakan algoritma content-based filtering dan collaborative filtering. Bahasa pemrograman digunakan adalah Python, HTML, CSS, Javascripts, Framework Bootstrap dan Django, serta RDMBS Neo4j. Neo4j dipilih karena menerapkan konsep Graph database dengan skema yang fleksibel dan tidak membutuhkan query yang kompleks dan memiliki Graph Data Science Library yang dapat digunakan untuk perhitungan Jaccard untuk content-based filtering dan Pearson correlation untuk collaborative filtering.<br/>
Sistem dapat memberikan rekomendasi movie berdasarkan genre favorite, rekomendasi movie pada user baru, rekomendasi movie pada user yang belum pernah merating, rekomendasi movie pada user yang memberikan rating satu kali, dan movie dengan rata-rata rating tertinggi. Sistem memiliki empat menu yakni menu rekomendasi untuk mencari movie yang direkomendasikan berdasarkan id user yang dipilih, menu movie untuk mengelola data movie, menu tag untuk mengelola semua data tag, menu rate untuk menginformasikan movie dengan rata-rata rating tertinggi.

## Developer
> I Kadek Ari Surya / I Gede Aditya Mahardika Pratama / Muhammad Akbar Hamid
