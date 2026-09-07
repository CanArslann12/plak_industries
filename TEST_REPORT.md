# Test Raporu

## Çalıştırılan komutlar

- `py -m py_compile config.py run.py app\__init__.py`: başarılı.
- `C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe -m pytest -q`: **14 passed**.
- Güncel test paketi: **15 passed**.
- Yerel HTTP testi: `/api/ai-durum` demo modunu bildirdi; `/api/leads` gerçek sunucuda başarılı kayıt döndürdü.
- Groq canlı bağlantı testi: eski `llama-3.1-8b-instant` modeli hesapta bulunamadı; erişilebilir `openai/gpt-oss-20b` modeline geçildi ve sohbet endpointi HTTP 200 ile doğrulandı.
- Güncel yerel test paketi: **15 passed**.

## Kapsam

Config ortam ayrımı, üretim sırları, SQLite tablo/kayıt/sıralama/özel karakter ve SQL injection metinleri, API doğrulama, yönetici erişimi, güvenli hata yanıtı ve mock AI timeout/bozuk yanıt yolları test edildi.

## Çalıştırılmadı / engelli

Gerçek Groq ağı, Wix çalışma alanı ve Render deploy doğrulaması dış hesap erişimi ve canlı backend adresi bulunmadığı için çalıştırılmadı.
