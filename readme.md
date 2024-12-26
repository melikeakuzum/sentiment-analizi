# Türkçe-İngilizce Duygu Analizi

Bu proje, Türkçe ve İngilizce metinler için gerçek zamanlı duygu analizi yapan bir web uygulamasıdır. Makine öğrenmesi ve doğal dil işleme teknikleri kullanarak metinlerin duygusal tonunu tespit eder.

## Özellikler

- ✨ Gerçek zamanlı analiz
- 🌍 Türkçe ve İngilizce dil desteği
- 😊 Emoji analizi
- 📊 Detaylı metin istatistikleri
- 🤖 Makine öğrenmesi tabanlı tahminler
- 💬 Cümle bazlı analiz
- 🎯 Pozitif/Negatif/Nötr sınıflandırma
- 📈 Güven skoru hesaplama

## Kurulum

1. Projeyi klonlayın:   
2. Gerekli paketleri yükleyin:   
3. Uygulamayı çalıştırın:   

## Nasıl Çalışır?

1. **Metin Girişi**: Kullanıcı analiz edilecek metni girer
2. **Dil Tespiti**: Sistem otomatik olarak metnin dilini tespit eder
3. **Duygu Analizi**: 
   - Makine öğrenmesi modeli metni analiz eder
   - Emoji'ler tespit edilir ve puanlanır
   - Cümleler ayrı ayrı değerlendirilir
4. **Sonuç**: 
   - Genel duygu durumu (Pozitif/Negatif/Nötr)
   - Güven skoru
   - En pozitif ve negatif cümleler
   - Metin istatistikleri

## Teknik Detaylar

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript (jQuery)
- **ML Model**: Scikit-learn (TF-IDF + Naive Bayes)
- **NLP**: NLTK
- **Stil**: Bootstrap 5

## Proje Yapısı
duygu-analizi/
├── app.py # Flask uygulaması
├── model.py # ML model ve analiz mantığı
├── requirements.txt # Python bağımlılıkları
├── README.md # Dokümantasyon
├── .gitignore # Git dışında tutulacak dosyalar
└── templates/ # HTML şablonları
└── index.html # Ana sayfa

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: X'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

- Proje Sahibi: [Ad Soyad]
- E-posta: [E-posta adresi]
- GitHub: [GitHub profil linki]

## Teşekkürler

- NLTK ekibine
- Scikit-learn topluluğuna
- Flask geliştiricilerine

