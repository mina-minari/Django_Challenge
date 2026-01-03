from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# .nev 파일 로드
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
DEBUG = os.getenv("DEBUG", "TRUE") == "TRUE"
<<<<<<< HEAD
=======

>>>>>>> upstream/main
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

LOGIN_URL = "/"
# Application definition

INSTALLED_APPS = [
    "app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
]

AUTH_USER_MODEL = "app.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # app/templates 를 쓸 거라 이대로 둬도 됨
        "APP_DIRS": True,  # app/templates/challenge/... 자동 인식
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
<<<<<<< HEAD
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
=======
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
>>>>>>> upstream/main
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization

<<<<<<< HEAD

=======
>>>>>>> upstream/main
LANGUAGE_CODE = "ko-kr"  # 한국어
TIME_ZONE = "Asia/Seoul"  # 한국 시간대

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"


# 업로드 이미지(인증 사진)용 MEDIA 설정
MEDIA_URL = "/media/"  # 브라우저에서 접근할 URL prefix
MEDIA_ROOT = BASE_DIR / "media"  # 실제 파일이 저장될 폴더 경로



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"