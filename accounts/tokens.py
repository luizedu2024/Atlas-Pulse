from django.core import signing


EMAIL_VERIFICATION_SALT = "atlas-pulse-email-verification"


def make_email_token(user):
    return signing.dumps({"user_id": user.pk, "email": user.email}, salt=EMAIL_VERIFICATION_SALT)


def read_email_token(token, max_age=60 * 60 * 24 * 3):
    return signing.loads(token, salt=EMAIL_VERIFICATION_SALT, max_age=max_age)
