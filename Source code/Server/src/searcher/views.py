import time, re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from processHelper.Processor import Processor
from processHelper.oxford_crawler import oxfordCrawler
from .models import Word
from .serializers import WordSerializer


class SearcherMethodTakeAverageAPI(APIView):
    permission_classes = [AllowAny]

    processor = Processor(200,
                          'data/vectors_ap8889_skipgram_s200_w20_neg20_hs0_sam1e-4_iter5.bin')

    def post(self, request, format=None):
        start = time.time()

        description = request.data['description']
        matrix_words_path = 'data/matrixvector_skipgram_s200_w20_neg20.bin'

        print('description', description)
        the_best_words_and_scores = self.processor.get_N_best_words(matrix_words_path, description)

        the_best_words_and_scores = [
            {'name': re.sub('[^A-Za-z]+', '', w[0]), 'score': w[1]} for w in the_best_words_and_scores
        ]

        return Response({'words': the_best_words_and_scores, 'time': time.time() - start})


class SearcherMethodMaxOfEveryPairOfWords(APIView):
    permission_classes = [AllowAny]

    processor = Processor(200,
                          'data/vectors_ap8889_skipgram_s200_w20_neg20_hs0_sam1e-4_iter5.bin')

    def post(self, request, format=None):
        start = time.time()
        description = request.data['description']

        the_best_words_and_scores = self.processor.get_the_N_best_words_case_2(
            'data/3D_matrix_definitions_with_skipgram_s200_w20_neg20_model.bin',
            description
        )
        the_best_words_and_scores = [
            {'name': re.sub('[^A-Za-z]+', '', w[0]), 'score': w[1]} for w in the_best_words_and_scores
        ]

        return Response({'words': the_best_words_and_scores, 'time': time.time() - start})

class WordList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        word = Word.objects.filter(name='hello')
        wordSerializer = WordSerializer(word, many=True)

        return Response(wordSerializer.data)

class MeaningOfWordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        word = request.data['word']
        try:
            word = Word.objects.get(name=word)
            return Response({'word': WordSerializer(word).data});
        except Word.DoesNotExist:
            print('crawling....')
            oxfordcrawler = oxfordCrawler()
            info = oxfordcrawler.crawl_individual_word(word)

            if info['word'] is None:
                return Response({'message': info['message'] })
            word = Word.objects.get(name=info['word'])
            print(word)
            return Response({'word': WordSerializer(word).data, 'message': info['message']});


