from rest_framework import serializers
from .models import Example, Word, Phonetic, Definition

class PhoneticSerializer(serializers.ModelSerializer):
	class Meta:
		model = Phonetic
		fields = ('id', 'prefix', 'ipa', 'sound', 'idword')

class ExampleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Example
		fields = ('idex', 'sentence', 'iddef')

class DefinitionSerializer(serializers.ModelSerializer):
	examples = serializers.SerializerMethodField()
	class Meta:
		model = Definition
		fields = ('id', 'def_field', 'idword', 'isapproved', 'examples')

	def get_examples(self, obj):
		examples = Example.objects.filter(iddef=obj.id)
		return ExampleSerializer(examples, many=True).data

class WordSerializer(serializers.ModelSerializer):
	defintions = serializers.SerializerMethodField()
	phonetics = serializers.SerializerMethodField()

	class Meta:
		model = Word
		fields = ('idword', 'name', 'pos', 'defintions', 'phonetics')

	def get_phonetics(self, obj):
		phonetics = Phonetic.objects.filter(idword=obj.idword)
		return PhoneticSerializer(phonetics, many=True).data

	def get_defintions(self, obj):
		print('hello', obj.idword)
		defintions = Definition.objects.filter(idword=obj.idword, isapproved=True)
		return DefinitionSerializer(defintions, many=True).data