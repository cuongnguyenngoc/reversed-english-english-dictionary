from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from processHelper.Processor import Processor

from searcher.models import Definition, Word
from searcher.serializers import DefinitionSerializer

# Create your views here.
class ImprovingSearchSystemAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        word = request.data['word']
        description = request.data['description']
        isExisted = Definition.objects.filter(idword__name=word, def_field=description).count()
        print(isExisted)
        if not isExisted:
        	wordObject = Word.objects.get(name=word)

	        definition = Definition.objects.create(idword=wordObject, def_field=description, isapproved=0)

        return Response({'message': 'Thank you so much for your help. We really appreciate that'})

class UpdatingSearchSystemAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        
        processor = Processor(200,
                          'data/vectors_ap8889_skipgram_s200_w20_neg20_hs0_sam1e-4_iter5.bin')
        processor.update_search_system('data/matrixvector_skipgram_s200_w20_neg20.bin', 
            'data/3D_matrix_definitions_with_skipgram_s200_w20_neg20_model.bin')

        return Response({'message': 'Update system search successfully'})