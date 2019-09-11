import _pickle
import csv

import numpy as np
from .file_process import FileProcess
from scipy.spatial.distance import cdist

from .word_processor import wordProcessor
from .dbprocessor import DBProcessor


class Processor:

    def __init__(self, num_features, file_model_path):
        self.num_features = num_features
        self.wordProcessor = wordProcessor()
        self.fileProcessor = FileProcess(num_features)
        self.dbprocessor = DBProcessor()
        self.model = self.fileProcessor.get_model_from_word2vec_pretrained_data(file_model_path)

    def sentence_to_vector_average_words_vector(self, sentence):
        index2word_set = set(self.model)
        words = self.wordProcessor.sentence_to_wordslist(sentence, remove_stopwords = True)
        featureVec = np.zeros((self.num_features,), dtype="float32")
        nwords = 0
        for word in words:
            if word in index2word_set:
                nwords += 1
                featureVec = np.add(featureVec, self.model[word])
        if nwords > 0:
            featureVec = np.divide(featureVec, nwords)
            return (True, featureVec)
        return (False, featureVec)

    def cos_cdist(self, matrix, vector):
        """
        Compute the cosine distances between each row of matrix and vector.
        """
        v = vector.reshape(1, -1)
        return 1 - cdist(matrix, v, 'cosine').reshape(-1)


    def create_feature_from_oxford_dictionary(self):
        entries = self.dbprocessor.getDictionary()

        entries = tuple(sorted(entries, key=lambda x: x[0].lower().strip()))
        resultsJson = {}
        word_tail = 0  # This is for distinguish the same word
        for entry in entries:
            origin_word = entry[0].lower()
            word = '_'.join((origin_word, str(0)))  # we will make this word has a tail zero like go_0
            definition = entry[1]

            if word in resultsJson:
                word_tail += 1
                right_word = '_'.join((origin_word, str(word_tail)))
                resultsJson[right_word] = self.wordProcessor.clean_meaning(definition)
            else:
                word_tail = 0
                resultsJson[word] = self.wordProcessor.clean_meaning(definition)

        print('Dictionary has ', len(resultsJson), 'words')
        for key in resultsJson:
            print('key = ', key)
        return resultsJson


    # this is for case 1: We will transfrom a sentence to a vector by averaging all vectors of words in sentence
    def get_matrix_of_wordvecs(self, dictionary):
        words = []
        matrixWordVecs = np.array([]).reshape(0, self.num_features)

        for word in dictionary:
            definiton_of_word = dictionary[word]
            check, sentenceVec = self.sentence_to_vector_average_words_vector(definiton_of_word)

            if check:
                print('word: ', word)
                wordVector_candidate = np.array(sentenceVec).reshape(1, self.num_features)
                matrixWordVecs = np.concatenate((matrixWordVecs, wordVector_candidate), axis=0)
                words.append(word)
        words = np.array(words)
        return (matrixWordVecs, words)

    def cal_similarity_description_and_meanings_of_words(self, matrix, sentence):
        check, sentenceVec = self.sentence_to_vector_average_words_vector(sentence)
        if check:
            # print('sentence', sentenceVec)
            return self.cos_cdist(matrix, sentenceVec)
        return "No result, please type a better desciption"

    def write_matrix_definitions_vector_by_average_words_vector(self, dictionary, file_matrix_vector_with_model):
        words_and_its_matrix_vecs = self.get_matrix_of_wordvecs(dictionary)
        with open(file_matrix_vector_with_model, 'wb') as fin:
            _pickle.dump(words_and_its_matrix_vecs, fin)

    def read_matrix_definitions_vector_by_average_words_vector(self, file_matrix_vector_with_model):
        with open(file_matrix_vector_with_model, 'rb') as fin:
            matrix, words = _pickle.load(fin)
            return (matrix, words)

    def get_N_best_words(self, matrix_words_path, description, N=10):

        matrix, words = self.read_matrix_definitions_vector_by_average_words_vector(
            matrix_words_path
        )
        list_scores = self.cal_similarity_description_and_meanings_of_words(matrix, description)

        indexs = np.argpartition(list_scores, -N)[-N:]
        largest_indices = indexs[np.argsort(-list_scores[indexs])]  # negative to sort from the highest value to the lowest value
        the_best_words_and_scores = list(zip(words[largest_indices], list_scores[largest_indices]))
        print('results', the_best_words_and_scores)

        return the_best_words_and_scores

    def similarity_of_words(self, word1, word2):
        vector1 = self.model[word1].reshape(1, -1)
        vector2 = self.model[word2].reshape(1, -1)
        return 1 - cdist(vector1, vector2, 'cosine').reshape(-1)
        # return np.dot(self.model[word1], self.model[word2]) / (np.linalg.norm(self.model[word1]) * np.linalg.norm(self.model[word2]))

    # End of case 1

    # For case 2, We will compare all pair words in 2 sentences and then sum of max.

    def write_3D_matrix_definitions_case_2(self, dictionary, file_to_save):

        index2word_set = set(self.model)
        dictionary_vectors = {}
        for word in dictionary:
            print(word)
            definition_vectors = np.array([]).reshape(0, self.num_features)
            words = self.wordProcessor.sentence_to_wordslist(dictionary[word], remove_stopwords=True)
            print(words)
            for w in words:
                if w in index2word_set:
                    word_vector = self.model[w].reshape(1, self.num_features)
                    definition_vectors = np.concatenate((definition_vectors, word_vector), axis=0)

            if len(definition_vectors) > 0:
                dictionary_vectors[word] = definition_vectors
        with open(file_to_save, 'wb') as fin:
            _pickle.dump(dictionary_vectors, fin)

    def read_3D_matrix_definitions_case_2(self, file_to_read):
        with open(file_to_read, 'rb') as fin:
            dictionary_vectors = _pickle.load(fin)
            return dictionary_vectors

    def cos_cdist_2(self, matrix1, matrix2):
        return 1 - cdist(matrix1, matrix2, 'cosine')

    def get_the_N_best_words_case_2(self, file_definition_with_model, description, N=10):

        index2word_set = set(self.model)
        words = self.wordProcessor.sentence_to_wordslist(description, remove_stopwords=True)
        words_vector = np.array([]).reshape(0, self.num_features)
        for word in words:
            if word in index2word_set:
                word_vector = self.model[word].reshape(1, self.num_features)
                words_vector = np.concatenate((words_vector, word_vector), axis=0)
        if len(words_vector) > 0:
            dictionary_vectors = self.read_3D_matrix_definitions_case_2(file_definition_with_model)
            words_and_scores = []
            for w in set(dictionary_vectors):
                # print(w)
                matrix_dist = self.cos_cdist_2(words_vector, dictionary_vectors[w])
                max_dist_each_word = matrix_dist.max(axis=1)
                score = np.mean(max_dist_each_word)  # get average of all maxs
                words_and_scores.append((w, score))

            best_words_and_scores = sorted(words_and_scores, key=lambda item: -item[1])[:N]

            return best_words_and_scores

        else:
            print("No result, please type a better desciption")


    # update search system
    def update_search_system(self, file_matrix_vector_with_model_method_one,
        file_matrix_vector_with_model_method_two):

        dictionary = self.create_feature_from_oxford_dictionary()

        #update matrix calculation for method 1
        self.write_matrix_definitions_vector_by_average_words_vector(dictionary, file_matrix_vector_with_model_method_one)
        
        #update matrix calculation for method 2
        self.write_3D_matrix_definitions_case_2(dictionary, file_matrix_vector_with_model_method_two)





