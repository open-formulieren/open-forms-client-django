import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "so-secret-i-cant-believe-you-are-looking-at-this"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "testapp.db"),
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "solo",
    "openformsclient",
    "testapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "testapp.urls"

DEBUG = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

try:
    import csp  # noqa

    print("Using CSP headers and allowing:")
    MIDDLEWARE += [
        "csp.middleware.CSPMiddleware",
    ]

    # Default source as self
    CSP_DEFAULT_SRC = ("'self'",)

    # The Open Forms SDK files might differ from the API domain.
    OPEN_FORMS_API_DOMAIN = "forms.example.com"
    OPEN_FORMS_SDK_DOMAIN = OPEN_FORMS_API_DOMAIN

    # Allow your webapp to load styles from Open Forms SDK.
    CSP_STYLE_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to load script from Open Forms SDK.
    CSP_SCRIPT_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to load images from Open Forms SDK.
    CSP_IMG_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to load fonts from Open Forms SDK.
    CSP_FONT_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to connect to the Open Forms API.
    CSP_CONNECT_SRC = ("'self'", OPEN_FORMS_API_DOMAIN)

    # The 'style-src' is only added here to allow our own inline styles.
    CSP_INCLUDE_NONCE_IN = ("script-src", "style-src")

except ImportError:
    print("Not using CSP headers: Django-CSP is not installed.")
