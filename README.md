# PLAK INDUSTRIES Proje Asistanı

PLAK INDUSTRIES için Türkçe proje talebi ve ön görüşme asistanı. MVP; sohbet, iletişim formu ve yönetici paneli sunar. Ödeme, CAD dosyası yükleme ve otomatik teknik tasarım kapsam dışıdır.

## Kurulum

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

`.env` içinde en az `SECRET_KEY` ve yerel geliştirme için `ADMIN_SECRET` değerlerini değiştirin. `GROQ_API_KEY` boşsa uygulama demo yanıtı verir.

Ön görüşme taleplerini `plakendustri@gmail.com` adresine göndermek için `.env` içinde `MAIL_USERNAME` ve `MAIL_PASSWORD` değerlerini doldurun. Gmail kullanıyorsanız normal hesap şifresi yerine uygulama şifresi kullanın. SMTP varsayılanları Gmail için ayarlanmıştır.

## Çalıştırma ve test

```powershell
py run.py
py -m pytest -q
```

Windows'ta masaüstündeki `PLAK INDUSTRIES Proje Asistanı` kısayoluna çift tıklayarak da başlatabilirsiniz. Sunucu penceresini uygulamayı kapatırken kapatın.

## AI API ayarı

Masaüstündeki `PLAK INDUSTRIES AI API Ayarı` kısayolunu çalıştırın. Sağlayıcıyı ve API anahtarını terminalde girin; anahtar ekranda gösterilmez ve `.env` dosyasına yazılır. Anahtarı HTML alanına, Git'e veya sohbet mesajına yazmayın. Ayardan sonra uygulamayı yeniden başlatın.

Üretim başlangıcı: `gunicorn run:app`. Windows geliştirme sunucusu ile üretim sunucusunu birbirinden ayrı kullanın.

## API

- `GET /health`
- `POST /api/sohbet`: `{ "mesaj": "...", "gecmis": [] }`
- `POST /api/leads`: `{ "isim": "...", "telefon": "...", "mesaj": "..." }`
- `GET /api/leads`: `X-Admin-Secret` başlığıyla yönetici erişimi

## Mimari rehber

`config.py` ortam ayarlarını ve PLAK INDUSTRIES iş bağlamını taşır. `app/database.py` yalnızca SQLite işlemlerini yapar. `app/services/ai_service.py` Groq çağrısını ve demo modunu kapsar. `app/services/email_service.py` SMTP bildirimlerini kapsar. `app/routes.py` doğrulama, blueprint ve HTTP yanıtlarından sorumludur. `app/__init__.py` uygulama fabrikasıdır.

## Wix ve Render

Wix tarafında `wix/` içindeki eşleştirme ve örnek kodları kullanın; canlı backend adresini ortamınıza göre değiştirin. Wix veya Render hesabı bu yerel projeden doğrulanamaz. Render'da SQLite kalıcı disk olmadan yeniden dağıtımda verileri kaybedebilir; kalıcı depolama veya harici veritabanı çözülmeden bunu üretim için tamamlanmış kabul etmeyin.

Masaüstündeki `PLAK INDUSTRIES Wix Alan Adı Ayarı` kısayolunu çalıştırarak Wix alan adını ve canlı backend adresini girin. Araç `CORS_ORIGINS` ayarını ve `wix/page.js` içindeki backend adresini günceller. Ardından Wix Editor > Dev Mode/Velo bölümünde `wix/page.js` kodunu sayfa koduna, `wix/backend.js` kodunu güvenli backend bölümüne ekleyip siteyi yayınlayın. Wix hesabı ve Render hesabı bu bilgisayardan otomatik yönetilemez; hesap girişlerini siz yapmalısınız.

LinkedIn adresi eklenmemiştir; geçerli herkese açık profil adresi sağlanmamıştır. Yalnızca `@plak.industries` Instagram adı kullanılır.
