import pandas as pd
import csv, os.path, pickle, numpy as np
from gensim import utils
import _pickle

class FileProcess:

    def __init__(self, num_features):
        self.num_features = num_features

    def get_raw_test_data_from_file(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                return list(reader)
        return []


    def get_dictionary_from_file(self, file_path):
        with open(file_path, 'rb') as data_file:
            dictionary = _pickle.load(data_file)
            return dictionary

    def _get_model_from_word2vec_pretrained_data_text_file(self, filePath):
        model = {}
        with utils.smart_open(filePath) as fin:
            next(fin)# removes the first line 978.. (number of words)
            for line in fin:
                elements = utils.to_unicode(line).split()
                model[elements[0]] = np.array(elements[1:], dtype=float)
        return model

    def dump_word_vector_model_to_binary(self, file_to_dump, file_to_be_dumped):
        model = self._get_model_from_word2vec_pretrained_data_text_file(file_to_dump)
        with open(file_to_be_dumped, 'wb') as fin:
            _pickle.dump(model, fin)

    def get_model_from_word2vec_pretrained_data(self, file_path):
        with open(file_path, 'rb') as fin:
            model = _pickle.load(fin)
            return model
