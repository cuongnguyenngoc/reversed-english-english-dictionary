from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from searcher.models import Definition, Word
from .serializers import DefinitionSerializer


class ListMeaningOfWordsNotYetApprovedAPI(APIView):

	def get(self, request, format=None):
		definitions = Definition.objects.filter(isapproved=False)
		definitionSerializer = DefinitionSerializer(definitions, many=True)

		return Response(definitionSerializer.data)

class ApprovingWordDefinitionPairAPI(APIView):

	def post(self, request, format=None):
		pair = request.data['pair']

		wordObject = Word.objects.get(name=pair['word']['name'])
		definition = Definition.objects.get(idword=wordObject, def_field=pair['def_field'])
		definition.isapproved = True;
		definition.save()
		definitionSerializer = DefinitionSerializer(definition)
		return Response(definitionSerializer.data)