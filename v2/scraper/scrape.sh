#!/bin/bash

# Course Scraper Script
# Bu script ders bilgilerini Özyeğin Üniversitesi MIS programından çeker

echo "🚀 Ders bilgileri çekiliyor..."
echo "=================================="

# Python ve pip'in yüklü olup olmadığını kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı. Lütfen Python3'ü yükleyin."
    exit 1
fi

# Virtual environment kontrol et ve yönet
VENV_NAME="ozu-scrape-venv"
VENV_PATH="./$VENV_NAME"

if [ -d "$VENV_PATH" ]; then
    echo "📦 $VENV_NAME virtual environment bulundu, aktifleştiriliyor..."
    source "$VENV_PATH/bin/activate"
else
    echo "📦 $VENV_NAME virtual environment bulunamadı, oluşturuluyor..."
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "✅ Virtual environment oluşturuldu ve aktifleştirildi."
    
    echo "🔧 Gerekli kütüphaneler yükleniyor..."
    pip install --upgrade pip
    pip install requests beautifulsoup4 pandas pyyaml
    echo "✅ Kütüphaneler başarıyla yüklendi."
fi

echo "🔍 Virtual environment aktif: $VIRTUAL_ENV"

# Scraping işlemini başlat
echo ""
echo "🔍 Ders bilgileri çekiliyor..."
python scrape.py

# Virtual environment'ı deaktif et
deactivate

# Config'den output dosyasını oku
OUTPUT_FILE=$(python -c "
import yaml
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print(config['mis_courses']['scrape_output'])
")

echo "📄 Hedef dosya: $OUTPUT_FILE"

# Sonuçları kontrol et
if [ -f "$OUTPUT_FILE" ]; then
    echo ""
    echo "✅ Başarıyla tamamlandı!"
    
    # Dosya uzantısına göre farklı kontroller
    if [[ "$OUTPUT_FILE" == *.csv ]]; then
        echo "📄 Ders bilgileri $OUTPUT_FILE dosyasına kaydedildi."
        echo ""
        echo "📊 İlk 5 ders:"
        head -6 "$OUTPUT_FILE"
        echo ""
        echo "📈 Toplam ders sayısı: $(tail -n +2 "$OUTPUT_FILE" | wc -l)"
    elif [[ "$OUTPUT_FILE" == *.db ]]; then
        echo "🗃️ Ders bilgileri $OUTPUT_FILE veritabanına kaydedildi."
        echo ""
        echo "📊 Veritabanı istatistikleri:"
        python -c "
import sqlite3
conn = sqlite3.connect('$OUTPUT_FILE')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM courses')
total_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(DISTINCT \"Ders Kodu\") FROM courses')
unique_courses = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(DISTINCT term) FROM courses')
unique_terms = cursor.fetchone()[0]
print(f'📈 Toplam ders bölümü: {total_count}')
print(f'📚 Farklı ders sayısı: {unique_courses}')
print(f'📅 Farklı dönem sayısı: {unique_terms}')
conn.close()
"
    fi
else
    echo "❌ Bir hata oluştu. $OUTPUT_FILE dosyası oluşturulamadı."
    exit 1
fi

echo ""
echo "🎉 Scraping işlemi tamamlandı!"
echo "💡 Virtual environment: $VENV_NAME aktif kaldı."
