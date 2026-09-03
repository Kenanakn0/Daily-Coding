# 🍃 Günlüğüm

Kişisel notlarını, ruh halini ve fotoğraf/video anılarını cihazda saklayan, parola korumalı bir günlük uygulaması. Tek bir HTML dosyası (`defter.html`) olarak yazılmış, Capacitor ile Android'e paketlenmiştir.

## Özellikler
- Takvim üzerinden gün gün not, ruh hali ve medya ekleme
- Kamera ile anlık fotoğraf çekme, galeriden çoklu seçim
- Etkinlik/hatırlatıcı ekleme — Android bildirimleriyle gerçek zamanlı hatırlatma
- Tüm veriler yalnızca cihazda (IndexedDB/localStorage), hiçbir sunucuya gönderilmez
- Parola ile kilit ekranı

## Geliştirme
```bash
npm install
npx cap sync android
cd android && ./gradlew assembleDebug
```

`defter.html` üzerinde değişiklik yaptıktan sonra `www/defter.html` ve `www/index.html` dosyalarına da kopyalanmalı, ardından `npx cap sync android` çalıştırılmalıdır.
