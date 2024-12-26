from flask import Flask, render_template, request
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect
from collections import Counter
import re
import json
import string
from model import DuyguModeli

# NLTK gerekli dosyaları indir
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

# Türkçe duygu kelimeleri ve ağırlıkları
tr_duygu_sozlugu = {
    # Pozitif kelimeler
    'güzel': 1.5,
    'iyi': 1.0,
    'harika': 2.0,
    'muhteşem': 2.0,
    'süper': 1.5,
    'mükemmel': 2.0,
    'hoş': 1.0,
    'başarılı': 1.0,
    'keyifli': 1.0,
    'mutlu': 1.5,
    'sevindirici': 1.5,
    'olumlu': 1.0,
    
    # Negatif kelimeler
    'kötü': -1.5,
    'berbat': -2.0,
    'korkunç': -2.0,
    'rezalet': -2.0,
    'felaket': -2.0,
    'yetersiz': -1.0,
    'başarısız': -1.0,
    'sorunlu': -1.0,
    'üzücü': -1.5,
    'olumsuz': -1.0,
    
    # Nötr kelimeler
    'normal': 0.0,
    'orta': 0.0,
    'fena değil': 0.2,
    'idare': 0.0,
    'fena': -0.5,
    'şöyle': 0.0,
    'böyle': 0.0
}

# Emoji sözlüğü
emoji_sozlugu = {
    '😊': 1.5, '😃': 1.5, '😄': 1.5, '🙂': 1.0, '😍': 2.0,
    '😢': -1.5, '😞': -1.5, '😡': -2.0, '😠': -1.5, '😕': -0.5,
    '👍': 1.0, '👎': -1.0, '❤️': 2.0, '💔': -2.0, '🙁': -1.0
}

# Global model değişkeni
duygu_modeli = DuyguModeli()

def metin_on_isleme(metin):
    metin = metin.lower()
    noktalama = set(char for char in string.punctuation if char not in emoji_sozlugu)
    metin = ''.join(char for char in metin if char not in noktalama)
    return metin

def emoji_analizi(metin):
    emoji_puani = 0
    emoji_sayisi = 0
    for emoji, puan in emoji_sozlugu.items():
        sayi = metin.count(emoji)
        if sayi > 0:
            emoji_puani += puan * sayi
            emoji_sayisi += sayi
    return emoji_puani, emoji_sayisi

def analiz_et(metin):
    if not metin or len(metin.strip()) == 0:
        return {"sonuc": "Boş Metin", "puan": 0, "dil": "Belirsiz"}

    try:
        # Dil tespiti ve analiz
        dil = detect(metin)
        emoji_puani, emoji_sayisi = emoji_analizi(metin)
        
        # AI analizi
        ai_sonuc = duygu_modeli.predict(metin)
        
        # Sonuçları birleştir
        toplam_puan = (
            ai_sonuc["puan"] * 0.7 + 
            emoji_puani * 0.3
        )

        return {
            "sonuc": ai_sonuc["sonuc"],
            "puan": toplam_puan,
            "dil": "Türkçe" if dil == 'tr' else "İngilizce",
            "detaylar": {
                "kelime_sayisi": len(metin.split()),
                "karakter_sayisi": len(metin),
                "emoji_sayisi": emoji_sayisi,
                "cumle_skorlari": ai_sonuc["detaylar"]["cumle_skorlari"],
                "genel_skor": ai_sonuc["detaylar"]["genel_skor"],
                "en_pozitif_cumle": ai_sonuc["detaylar"]["en_pozitif_cumle"],
                "en_negatif_cumle": ai_sonuc["detaylar"]["en_negatif_cumle"],
                "emoji_etkisi": emoji_puani
            }
        }
        
    except Exception as e:
        print(f"Analiz hatası: {e}")
        return {"sonuc": "Hata", "puan": 0, "dil": "Belirsiz"}

@app.route('/', methods=['GET', 'POST'])
def ana_sayfa():
    return render_template('index.html')

@app.route('/analiz', methods=['POST'])
def canli_analiz():
    metin = request.json.get('metin', '')
    if metin:
        sonuc = analiz_et(metin)
        return json.dumps(sonuc)
    return json.dumps({"error": "Metin bulunamadı"})

if __name__ == '__main__':
    app.run(debug=True) 