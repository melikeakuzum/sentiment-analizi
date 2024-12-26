from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

class DuyguModeli:
    def __init__(self):
        self.model = None
        self.model_path = 'model/duygu_model.joblib'
        
        # Pozitif ve negatif kelime listeleri
        self.pozitif_kelimeler = {
            'bayıldım': 1.0, 'çok iyi': 1.0, 'harika': 1.0, 'mükemmel': 1.0,
            'süper': 1.0, 'muhteşem': 1.0, 'fevkalade': 1.0, 'şahane': 1.0,
            'güzel': 0.8, 'beğendim': 0.8, 'iyi': 0.8, 'hoş': 0.8,
            'başarılı': 0.8, 'keyifli': 0.8, 'memnun': 0.8,
            'sevdim': 0.9, 'tavsiye': 0.9, 'kaliteli': 0.9
        }
        
        self.negatif_kelimeler = {
            'kötü': -1.0, 'berbat': -1.0, 'rezalet': -1.0, 'korkunç': -1.0,
            'beğenmedim': -0.8, 'başarısız': -0.8, 'yetersiz': -0.8,
            'sorunlu': -0.8, 'pişman': -0.9, 'olmamış': -0.7
        }
        
        # Model yoksa oluştur
        if not os.path.exists('model'):
            os.makedirs('model')
            self._create_model()
        else:
            try:
                self.load_model()
            except:
                self._create_model()
    
    def _create_model(self):
        # Genişletilmiş veri seti
        texts = [
            # Pozitif Türkçe (tekli kelimeler)
            "bayıldım", "harika", "muhteşem", "süper", "mükemmel",
            "fevkalade", "şahane", "güzel", "beğendim", "iyi",
            "hoş", "başarılı", "keyifli", "memnun", "sevdim",
            
            # Pozitif Türkçe (çoklu kelimeler)
            "çok iyi", "çok güzel", "çok beğendim", "harika bir deneyim",
            "çok memnun kaldım", "tam istediğim gibi", "kesinlikle tavsiye ederim",
            "çok başarılı olmuş", "bayıldım buna", "süper bir ürün",
            "mükemmel bir deneyim", "çok kaliteli", "harika bir seçim",
            
            # Negatif Türkçe
            "kötü", "berbat", "rezalet", "korkunç", "beğenmedim",
            "başarısız", "yetersiz", "sorunlu", "pişman oldum", "olmamış",
            "hiç beğenmedim", "çok kötü", "berbat ötesi",
            
            # Nötr Türkçe
            "fena değil", "idare eder", "normal", "ortalama", "vasat",
            "eh işte", "şöyle böyle", "orta", "standart", "sıradan",
            
            # İngilizce örnekler
            "great", "awesome", "wonderful", "perfect", "excellent",
            "terrible", "bad", "awful", "horrible", "worst",
            "okay", "not bad", "decent", "average", "so so"
        ]
        
        # Etiketleri oluştur
        labels = (
            ["Pozitif"] * 15 +    # Pozitif tekli
            ["Pozitif"] * 13 +    # Pozitif çoklu
            ["Negatif"] * 13 +    # Negatif
            ["Nötr"] * 10 +       # Nötr
            ["Pozitif"] * 5 +     # İngilizce pozitif
            ["Negatif"] * 5 +     # İngilizce negatif
            ["Nötr"] * 5          # İngilizce nötr
        )

        # Pipeline oluştur
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3),
                min_df=1,
                max_df=0.95,
                sublinear_tf=True
            )),
            ('clf', MultinomialNB(alpha=0.05))
        ])
        
        # Modeli eğit
        self.model.fit(texts, labels)
        self.save_model()
    
    def predict(self, text):
        try:
            text = text.lower().strip()
            cumleler = [c.strip() for c in text.split('.') if c.strip()]
            
            toplam_skor = 0
            toplam_agirlik = 0
            cumle_skorlari = []
            
            # Her cümleyi ayrı analiz et
            for i, cumle in enumerate(cumleler):
                skor = 0
                kelime_sayisi = 0
                
                # Pozitif kelime kontrolü
                for kelime, puan in self.pozitif_kelimeler.items():
                    tekrar = cumle.count(kelime)
                    if tekrar > 0:
                        skor += puan * (1 + 0.3 * (tekrar - 1))
                        kelime_sayisi += tekrar
                
                # Negatif kelime kontrolü
                for kelime, puan in self.negatif_kelimeler.items():
                    tekrar = cumle.count(kelime)
                    if tekrar > 0:
                        skor += puan * (1 + 0.5 * (tekrar - 1))
                        kelime_sayisi += tekrar
                
                # Cümle skorunu hesapla
                if kelime_sayisi > 0:
                    pozisyon_agirlik = 1 + (i / len(cumleler)) * 0.2
                    
                    if skor > 0:
                        skor = skor * 1.2  # Pozitif skorları %20 artır
                    
                    cumle_skoru = (skor / kelime_sayisi) * pozisyon_agirlik
                    cumle_skorlari.append((cumle, cumle_skoru))
                    toplam_skor += cumle_skoru
                    toplam_agirlik += pozisyon_agirlik
            
            # Genel skoru hesapla
            genel_skor = toplam_skor / max(toplam_agirlik, 1)
            
            # En pozitif ve negatif cümleleri bul
            en_pozitif_cumle = max(cumle_skorlari, key=lambda x: x[1])[0] if cumle_skorlari else ""
            en_negatif_cumle = min(cumle_skorlari, key=lambda x: x[1])[0] if cumle_skorlari else ""
            
            # Sonucu belirle
            if abs(genel_skor) > 0.3:
                if genel_skor > 0:
                    sonuc = "Pozitif"
                else:
                    sonuc = "Negatif"
                guven = abs(genel_skor)
            else:
                sonuc = "Nötr"
                guven = 0.5
            
            return {
                "sonuc": sonuc,
                "puan": float(guven),
                "detaylar": {
                    "cumle_skorlari": [(c, float(s)) for c, s in cumle_skorlari],
                    "genel_skor": float(genel_skor),
                    "en_pozitif_cumle": en_pozitif_cumle,
                    "en_negatif_cumle": en_negatif_cumle,
                    "toplam_agirlik": float(toplam_agirlik)
                }
            }
                
        except Exception as e:
            print(f"Tahmin hatası: {e}")
            return {
                "sonuc": "Nötr",
                "puan": 0.5,
                "detaylar": {
                    "cumle_skorlari": [],
                    "genel_skor": 0,
                    "en_pozitif_cumle": "",
                    "en_negatif_cumle": "",
                    "toplam_agirlik": 0
                }
            }
    
    def save_model(self):
        joblib.dump(self.model, self.model_path)
    
    def load_model(self):
        self.model = joblib.load(self.model_path) 