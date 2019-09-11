from django.conf.urls import url

from .views import (
	ListMeaningOfWordsNotYetApprovedAPI,
	ApprovingWordDefinitionPairAPI,
)

urlpatterns = [
	url(r'^manage-word-defintion-pairs-from-users', ListMeaningOfWordsNotYetApprovedAPI.as_view(), name='manage'),
	url(r'^approve-word-defintion-pair-of-users', ApprovingWordDefinitionPairAPI.as_view(), name="approving"),
]
