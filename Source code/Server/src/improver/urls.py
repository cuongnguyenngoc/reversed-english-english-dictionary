from django.conf.urls import url

from .views import (
	ImprovingSearchSystemAPI,
	UpdatingSearchSystemAPI
)

urlpatterns = [
	url(r'^receive-feedback', ImprovingSearchSystemAPI.as_view(), name='receive-feedback'),
	url(r'^updating-system', UpdatingSearchSystemAPI.as_view(), name='updating-system'),
]