"""
Django settings for shopSite project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os,sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nvwbiy*u@37u9m3q1hz_3f$3^dm6cgty$@q=kty#d)j$3bq1hs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost','wl22.free.ngrok.cc',]


#重载系统的用户，让UserProfile生效
AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    # 包含认证框架的核心和默认的模型
    'django.contrib.auth',
    # django内容类型系统，它允许权限与你创建的模型关联
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 使用pip安装是python2版本，python3版本需源码安装
    'DjangoUeditor',
    # 源码安装xadmin时，会报ModuleNotFoundError，需要手动安装需要的模块，
    # 还有一些问题：http://www.lybbn.cn/data/bbsdatas.php?lybbs=50
    'xadmin',
    # ModuleNotFoundError：pip install django-crispy-forms
    'crispy_forms',
    'users',
    'goods',
    'trade',
    'user_operation',
    'rest_framework',
    'django_filters',
    'coreschema',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # 必须在CsrfViewMiddleware之前
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 管理会话
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 使用会话将用户与请求关联
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
)

ROOT_URLCONF = 'shopSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopSite.wsgi.application'

# 认证后台列表
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',   # 使用自定义基本认证
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.QQOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)



# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop_site',    #数据库名字
        'USER': 'root',         #账号
        'PASSWORD': '123456',   #密码
        'HOST': '127.0.0.1',    #IP
        'PORT': '3306',         #端口
        # 默认引擎myisam,第三方登录时，要求引擎为INNODB
        "OPTIONS":{"init_command":"SET default_storage_engine=INNODB;"}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# 设置上传文件的路径
MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media")



REST_FRAMEWORK = {
    # 分页风格
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 过滤
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # 认证模式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # drf的token缺点：
        # 保存在数据库中，如果是一个分布式的系统，就非常麻烦
        # token永久有效，没有过期时间
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}


import datetime
#有效期限
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),    #也可以设置seconds=20
    'JWT_AUTH_HEADER_PREFIX': 'JWT',                       #JWT跟前端保持一致，比如“token”这里设置成JWT
}


# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 云片
APIKEY = "2b65704bc23ae4ed25f1aa59d61563c1"