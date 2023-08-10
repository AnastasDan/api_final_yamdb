from django.core.mail import send_mail


def send_confirmation_email(email, confirmation_code):
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_code}"
    from_email = "admin@yamdb.ru"
    send_mail(subject, message, from_email, [email], fail_silently=False)
