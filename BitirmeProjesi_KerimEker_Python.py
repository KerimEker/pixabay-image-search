import streamlit as st
import requests

# 📌 API bilgileri
API_KEY = "50096047-8bb459140d4c19e045f4f2381"
API_URL = "https://pixabay.com/api/"

# 🖥️ Sayfa ayarı
st.set_page_config(page_title="Pixabay Görsel Arama", layout="wide")
st.title("📷 Pixabay Görsel Arama Uygulaması")

# 🔍 Kullanıcıdan arama kelimesi alınır (İngilizce girilecek)
query = st.text_input("Aratmak İstediğiniz Kelimeyi Giriniz (İngilizce)", placeholder="e.g. cat, space, ocean")

# 🗂️ Türkçe görünen kategori seçenekleri
category_map = {
    "Tümü": "all", "Arka Planlar": "backgrounds", "Moda": "fashion", "Doğa": "nature",
    "Bilim": "science", "Eğitim": "education", "İnsanlar": "people", "Duygular": "feelings",
    "Din": "religion", "Sağlık": "health", "Yerler": "places", "Hayvanlar": "animals",
    "Sanayi": "industry", "Yemek": "food", "Bilgisayar": "computer", "Spor": "sports",
    "Taşımacılık": "transportation", "Seyahat": "travel", "Binalar": "buildings",
    "İş Dünyası": "business", "Müzik": "music"
}

# 🎨 Türkçe görünen renk seçenekleri
color_map = {
    "Filtre Yok": "none", "Gri Tonlama": "grayscale", "Saydam": "transparent", "Kırmızı": "red",
    "Turuncu": "orange", "Sarı": "yellow", "Yeşil": "green", "Turkuaz": "turquoise",
    "Mavi": "blue", "Mor": "lilac", "Pembe": "pink", "Beyaz": "white",
    "Gri": "gray", "Siyah": "black", "Kahverengi": "brown"
}

# 🎛️ Seçim alanları (kategori, renk, sonuç sayısı)
col1, col2, col3 = st.columns(3)

with col1:
    selected_category_tr = st.selectbox("Kategori", list(category_map.keys()))
with col2:
    selected_color_tr = st.selectbox("Renk Filtresi", list(color_map.keys()))
with col3:
    result_count = st.slider("Kaç görsel gösterilsin?", min_value=3, max_value=200, value=21, step=3)

# 🔎 Arama butonu
if st.button("Görselleri Getir"):
    if not query:
        st.warning("Lütfen bir anahtar kelime giriniz.")
    else:
        st.info("Görseller yükleniyor...")

        # API’ye gönderilecek İngilizce kategori ve renk kodları
        selected_category = category_map[selected_category_tr]
        selected_color = color_map[selected_color_tr]

        # 🌐 API parametreleri hazırlanır
        params = {
            "key": API_KEY,
            "q": query,
            "image_type": "photo",
            "per_page": result_count,
            "safesearch": "true"
        }
        if selected_category != "all":
            params["category"] = selected_category
        if selected_color != "none":
            params["colors"] = selected_color

        try:
            # 📡 API'ye istek gönderilir
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            total = data.get("totalHits", 0)
            hits = data.get("hits", [])

            # ✅ Kullanıcıya anlamlı bilgi verilir
            if total == 0 or not hits:
                st.warning("Hiç görsel bulunamadı. Lütfen farklı bir anahtar kelime deneyin.")
            else:
                gösterilen_sayı = min(result_count, len(hits))
                st.success(f"Toplam {total} görsel bulundu. İlk {gösterilen_sayı} tanesi gösteriliyor.")
                
                # 🖼️ Görseller 3 sütun halinde gösterilir
                cols = st.columns(3)
                for i, img in enumerate(hits):
                    with cols[i % 3]:
                        st.image(img["webformatURL"], caption=img["tags"], use_column_width=True)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
