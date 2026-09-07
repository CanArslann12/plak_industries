# Gereksinim Kontrol Listesi

| Gereksinim | Dosya | Test | Durum |
|---|---|---|---|
| Ortam ayarları ve marka bağlamı | `config.py`, `.env.example` | Config testleri | Tamamlandı |
| Lead veritabanı | `app/database.py` | DB testleri | Tamamlandı |
| AI servisi | `app/services/ai_service.py` | Mock HTTP testleri | Tamamlandı |
| API ve yönetici erişimi | `app/routes.py` | Flask client testleri | Tamamlandı |
| Karşılama ve dashboard | `app/templates/`, `app/static/` | Flask route testleri | Tamamlandı |
| Wix teslimi | `wix/` | Manuel Wix doğrulaması | Hazır, canlı test yok |
| Render/GitHub hazırlığı | `README.md`, `.gitignore` | Yapılandırma kontrolü | Hazır, deploy yok |
