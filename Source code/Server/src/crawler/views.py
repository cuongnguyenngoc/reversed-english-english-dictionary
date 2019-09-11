import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bigChance import settings

from processHelper.oxford_crawler import oxfordCrawler
from searcher.models import Definition, Word
from searcher.serializers import WordSerializer

class DictionaryCrawlingAPI(APIView):
	
    def get(self, request, format=None):
        fileDatabasePath = os.path.join(settings.BASE_DIR, 'data/raw_dictionary_data.csv')
        print(fileDatabasePath)
        oxfordcrawler = oxfordCrawler(fileDatabasePath)
        oxfordcrawler.create_workers()
        oxfordcrawler.create_crawling_jobs()

        return Response({ 'words': oxfordcrawler.entries_crawled, 'message': 'Crawler is done' })

class WordCrawlingAPI(APIView):
	permission_classes = [AllowAny]

	def post(self, request, format=None):
		word = request.data['word']

		oxfordcrawler = oxfordCrawler()
		info = oxfordcrawler.crawl_individual_word(word)

		if info['word'] is None:
			return Response({'message': info['message']})
		word = Word.objects.get(name=info['word'])
		word = WordSerializer(word).data
		return Response({'word': word, 'message': info['message'] })