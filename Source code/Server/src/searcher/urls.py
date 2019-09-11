from django.conf.urls import url

from .views import (
    SearcherMethodTakeAverageAPI,
    SearcherMethodMaxOfEveryPairOfWords,
    WordList,
    MeaningOfWordAPI
)

urlpatterns = [
    url(r'^basic_search', SearcherMethodTakeAverageAPI.as_view(), name='searchcase1'),
    url(r'^advanced_search', SearcherMethodMaxOfEveryPairOfWords.as_view(), name='searchcase2'),
    url(r'^words', WordList.as_view(), name='words'),
    url(r'^meaning', MeaningOfWordAPI.as_view(), name='meaning')
]