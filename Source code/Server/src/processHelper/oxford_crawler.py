import threading
from queue import Queue

import numpy as np
import requests
from bs4 import BeautifulSoup
from .dbprocessor import DBProcessor
from gensim import utils


class oxfordCrawler:

    def __init__(self, file_database_path=''):
        self.entries_crawled = {} # each of entry contains its word, definition, examples
        self.NUMBER_OF_THREADS = 100
        self.queue = Queue()
        self.dbprocessor = DBProcessor()
        self.raw_dictionary = set([
            entry[0] for entry in self.dbprocessor.get_raw_dictionary_from_file(file_database_path)
        ]) # model = ['word1','word2'] because we just use words in dictionary
                                                                     # no need to use their vector

        self.count = 0
        self.number_of_words_crawled = 0

    def _get_definitions_of_word(self, word):
        entries = []
        wordVariants = [word, '_'.join((word,str(1))), '_'.join((word, str(2))), '_'.join((word, str(3))), '_'.join((word, str(4))), ''.join((word, str('1_1')))]
        count = 0

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

        for wordVariant in wordVariants:
            page = requests.get('http://www.oxfordlearnersdictionaries.com/definition/english/'+wordVariant, verify=False, allow_redirects=False, stream=True, headers=headers)
            if page.status_code == 200:
                # print('Worker', threading.current_thread().name, 'is crawling this word...', wordVariant)
                entries = self._extract_full_data_from_page(page)
                return (True, entries)
            count += 1
        if count == len(wordVariants):
            return (False, entries)


    def _extract_data_from_page(self, word_page):
        entries = []
        soup = BeautifulSoup(word_page.content, 'lxml')
        parent_elements = soup.find_all("span", {"class": "sn-gs"})

        if len(parent_elements):
            # print(parent_elements)
            for parent_element in parent_elements:
                if parent_element.parent['class'] != ['idm-g']:
                    entry_elements = parent_element.find_all("span", {"class": "sn-g"})
                    if len(entry_elements) == 0:
                        entry_elements = parent_element.find_all("li", {"class": "sn-g"})
                    # print('1', entry_elements)
                    if len(entry_elements):
                        for element in entry_elements:
                            # print('2', element)
                            defin_elements = element.find_all("span", {"class": "def"}) # This will find all elements that
                                                                                        # has class def or xh or ndv
                            # print('3', defin_elements)
                            if len(defin_elements) == 0:
                                defin_elements = element.find_all("span", {"class": "xh"})
                            if len(defin_elements) == 0:
                                defin_elements = element.find_all("span", {"class": "ndv"})
                            example_elements = element.find_all("span", {"class": "x-g"})
                            examples = []
                            for ex in example_elements:
                                examples.append(ex.text)

                            if len(defin_elements):
                                print('CHECK', {'def': defin_elements[0].text, 'examples': examples})
                                entries.append({'def': defin_elements[0].text, 'examples': examples})
                            else:
                                print('this has no meaning')

            # print('This word has meaning', results)
        return entries

    def _extract_full_data_from_page(self, word_page):
        soup = BeautifulSoup(word_page.content, 'lxml')
        entryContentElement = soup.find(id="entryContent");
        if len(entryContentElement) == 0:
            return {'pos': '', 'phonetic': '', 'definitionsWithExamples': []}

        pos = entryContentElement.find_all("div", {"class": "webtop-g"})[0].find_all("span", {"class": "pos"})
        poses = []
        if len(pos):
            for p in pos:
                poses.append(p.text)
        join_poses = ''
        if len(poses) >= 2:
            join_poses = ', '.join(poses)
        elif len(poses) == 1:
            join_poses = poses[0]

        print('pos', join_poses)

        prons = entryContentElement.find_all("span", {"class": "pron-g"})
        phonetics = []
        if len(prons):
            for pron in prons:
                prefixs = []
                if len(pron.find_all("span", {"class": "prefix"})):
                    for prefix in pron.find_all("span", {"class": "prefix"}):
                        prefixs.append(prefix.text)
                prefixs = ' '.join(prefixs)
                ipa, sound = '', ''
                if len(pron.find_all("span", {"class": "phon"})):
                    ipa = pron.find_all("span", {"class": "phon"})[0].text
                    ipa = ipa.split("/")[2]
                    print(ipa)
                if len(pron.find_all("div", {"class": "sound"})):
                    sound = pron.find_all("div", {"class": "sound"})[0].get('data-src-mp3')
                print('prefix', prefixs,  ipa, sound)
                phonetics.append({'prefix': prefixs, 'ipa': ipa, 'sound': sound})

        parent_elements = soup.find_all("span", {"class": "sn-gs"})
        definitionsWithExamples = []
        if len(parent_elements):
            # print(parent_elements)
            for parent_element in parent_elements:
                if parent_element.parent['class'] != ['idm-g']:
                    entry_elements = parent_element.find_all("span", {"class": "sn-g"})
                    if len(entry_elements) == 0:
                        entry_elements = parent_element.find_all("li", {"class": "sn-g"})
                    # print('1', entry_elements)
                    if len(entry_elements):
                        for element in entry_elements:
                            # print('2', element)
                            defin_elements = element.find_all("span", {"class": "def"})  # This will find all elements that
                            # has class def or xh or ndv
                            # print('3', defin_elements)
                            if len(defin_elements) == 0:
                                defin_elements = element.find_all("span", {"class": "xh"})
                            if len(defin_elements) == 0:
                                defin_elements = element.find_all("span", {"class": "ndv"})
                            example_elements = element.find_all("span", {"class": "x-g"})
                            examples = []
                            for ex in example_elements:
                                examples.append(ex.text)

                            if len(defin_elements):
                                print('CHECK', {'def': defin_elements[0].text, 'examples': examples})
                                definitionsWithExamples.append({'def': defin_elements[0].text, 'examples': examples})
                            else:
                                print('this has no meaning')

                                # print('This word has meaning', results)
        return {'pos': join_poses, 'phonetic': phonetics, 'definitionsWithExamples': definitionsWithExamples}

    def crawl_individual_word(self, word):
        if not self.dbprocessor.checkWordExisting(word):
            check, wordContent = self._get_definitions_of_word(word)

            if check and len(wordContent['definitionsWithExamples']) > 0:
                self.dbprocessor.writeEachWordToDataBase(word, wordContent)
                return {'word': word, 'message': 'Crawling succeeds'}
            return {'word': None, 'message': 'This word cannot be crawled because it does not exist'}

        return {'word': None, 'message': 'This word is existed in database'}

    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            worker = threading.Thread(target=self._crawl_data)
            worker.daemon = True
            worker.start()

    def _crawl_data(self):

        while True:
            word = self.queue.get()
            print('How many it has left ', self.queue.qsize())
            try:
                check, wordContent = self._get_definitions_of_word(word)
                if check and len(wordContent['definitionsWithExamples']) > 0:
                    # self.entries_crawled[word] = entries
                    self.number_of_words_crawled += 1
                    self.dbprocessor.writeEachWordToDataBase(word, wordContent)
                # print('there are', len(self.entries_crawled), 'in entries_crawled')
                self.queue.task_done()
            except Exception as e:
                print("Error", e)
                print('Check this out fize of entries_crawled', self.number_of_words_crawled, 'word error', word)
                self.queue.put(word)
                self.queue.task_done()


    def create_crawling_jobs(self):
        for word in self.raw_dictionary:
            if self.dbprocessor.checkWordExisting(word):
                print('This word is duplicated', word)
                continue
            self.queue.put(word)
            print('len queue', self.queue.qsize())
        self.queue.join()
        print('Crawling is done')