from flask import Blueprint, current_app, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service
from app.services.email_service import EmailServiceError, email_service

pages = Blueprint("pages", __name__)
api = Blueprint("api", __name__, url_prefix="/api")


@pages.get("/")
def index():
    return render_template("index.html")


@pages.get("/dashboard")
def dashboard():
    if request.headers.get("X-Admin-Secret") != current_app.config["ADMIN_SECRET"]:
        return jsonify(basari=False, hata="Yetkisiz erişim."), 401
    return render_template("dashboard.html")


@api.post("/sohbet")
def sohbet():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("mesaj"), str):
        return jsonify(basari=False, hata="Geçerli bir JSON mesajı gerekli."), 400
    mesaj = payload["mesaj"].strip()
    if not mesaj or len(mesaj) > 4000:
        return jsonify(basari=False, hata="Mesaj boş veya çok uzun."), 400
    if not isinstance(payload.get("gecmis", []), list):
        return jsonify(basari=False, hata="Geçmiş biçimi geçersiz."), 400
    try:
        cevap = ai_service.yanit_uret(mesaj, payload.get("gecmis", []))
    except AIServiceError:
        return jsonify(basari=False, hata="Asistan şu anda yanıt veremiyor."), 503
    return jsonify(basari=True, cevap=cevap)


@api.post("/leads")
def leads_create():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(basari=False, hata="Geçerli bir JSON gövdesi gerekli."), 400
    isim = payload.get("isim")
    telefon = payload.get("telefon")
    mesaj = payload.get("mesaj", "")
    if not all(isinstance(value, str) for value in (isim, telefon, mesaj)):
        return jsonify(basari=False, hata="Alan türleri geçersiz."), 400
    if not isim.strip() or not telefon.strip() or len(mesaj) > 4000:
        return jsonify(basari=False, hata="İsim ve telefon zorunludur."), 400
    temiz_isim = isim.strip()
    temiz_telefon = telefon.strip()
    temiz_mesaj = mesaj.strip()
    lead_id = lead_ekle(temiz_isim, temiz_telefon, temiz_mesaj)
    try:
        bildirim_gonderildi = email_service.lead_bildirimi_gonder(
            temiz_isim, temiz_telefon, temiz_mesaj
        )
    except EmailServiceError:
        bildirim_gonderildi = False
    return jsonify(basari=True, lead_id=lead_id, bildirim_gonderildi=bildirim_gonderildi), 201


@api.get("/leads")
def leads_list():
    if request.headers.get("X-Admin-Secret") != current_app.config["ADMIN_SECRET"]:
        return jsonify(basari=False, hata="Yetkisiz erişim."), 401
    return jsonify(basari=True, leadler=tum_leadler())


@api.get("/ai-durum")
def ai_durum():
    return jsonify(
        basari=True,
        saglayici=current_app.config["AI_PROVIDER"],
        model=current_app.config["AI_MODEL"],
        yapilandirilmis=bool(current_app.config["GROQ_API_KEY"]),
    )