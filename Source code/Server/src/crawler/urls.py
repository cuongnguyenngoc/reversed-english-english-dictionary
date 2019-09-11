from django.conf.urls import url

from .views import (
    DictionaryCrawlingAPI,
    WordCrawlingAPI,
)

urlpatterns = [
    url(r'^crawl-dictionary', DictionaryCrawlingAPI.as_view(), name='crawl-dictionary'),
    url(r'^crawl-word', WordCrawlingAPI.as_view(), name='crawl-word')
]