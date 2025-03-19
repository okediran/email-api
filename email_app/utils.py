import requests
from django.conf import settings

def verify_recaptcha(captcha_value):
    """Verify Google reCAPTCHA token"""
    recaptcha_secret = settings.RECAPTCHA_SECRET_KEY
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": recaptcha_secret, "response": captcha_value}
    ).json()
    
    return response.get("success", False)
