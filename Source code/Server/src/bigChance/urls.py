"""bigChance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import (obtain_jwt_token, verify_jwt_token)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/dictionary/crawl/', include(("crawler.urls", "crawling"), namespace="crawling")),
    url(r'^api/dictionary/search/', include(("searcher.urls", "searcher"), namespace="searcher")),
    url(r'^api/dictionary/improve/', include(("improver.urls", "improver"), namespace="improver")),
    url(r'^api/auth/token/', obtain_jwt_token),
    url(r'^api/auth/token-verify/', verify_jwt_token),
    url(r'^api/admin/', include(("admin_manage.urls", "admin-manage"), namespace="admin-manage")),
]
