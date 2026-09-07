import os
import smtplib
from email.message import EmailMessage


class EmailServiceError(Exception):
    """Raised when a lead notification cannot be sent."""


class EmailService:
    def __init__(self, server, port, username, password, recipient, use_tls=True):
        self.server = server
        self.port = int(port)
        self.username = username
        self.password = password
        self.recipient = recipient
        self.use_tls = use_tls

    @property
    def configured(self):
        return bool(self.server and self.username and self.password and self.recipient)

    def lead_bildirimi_gonder(self, isim, telefon, mesaj):
        if not self.configured:
            return False

        email = EmailMessage()
        email["Subject"] = f"Yeni PLAK INDUSTRIES ön görüşme talebi: {isim}"
        email["From"] = self.username
        email["To"] = self.recipient
        email.set_content(
            "PLAK INDUSTRIES yeni ön görüşme talebi\n\n"
            f"İsim: {isim}\n"
            f"Telefon: {telefon}\n"
            f"Proje özeti:\n{mesaj or 'Belirtilmedi'}\n"
        )

        try:
            with smtplib.SMTP(self.server, self.port, timeout=20) as smtp:
                if self.use_tls:
                    smtp.starttls()
                smtp.login(self.username, self.password)
                smtp.send_message(email)
        except (OSError, smtplib.SMTPException) as error:
            raise EmailServiceError("Ön görüşme bildirimi gönderilemedi.") from error
        return True


email_service = EmailService(
    server=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    port=os.getenv("MAIL_PORT", "587"),
    username=os.getenv("MAIL_USERNAME", ""),
    password=os.getenv("MAIL_PASSWORD", "").replace(" ", ""),
    recipient=os.getenv("LEAD_NOTIFICATION_EMAIL", "plakendustri@gmail.com"),
    use_tls=os.getenv("MAIL_USE_TLS", "true").lower() == "true",
)
