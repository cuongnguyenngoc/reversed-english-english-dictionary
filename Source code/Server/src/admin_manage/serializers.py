
from rest_framework import serializers
from searcher.models import Definition, Word

class WordSerializer(serializers.ModelSerializer):
	class Meta:
		model = Word
		fields = ('idword', 'name', 'pos')

class DefinitionSerializer(serializers.ModelSerializer):
	word = serializers.SerializerMethodField()
	isapproved = serializers.SerializerMethodField()

	class Meta:
		model = Definition
		fields = ('id', 'def_field', 'idword', 'isapproved', 'word')

	def get_word(self, obj):
		return WordSerializer(obj.idword).data

	def get_isapproved(self, obj):
		return False