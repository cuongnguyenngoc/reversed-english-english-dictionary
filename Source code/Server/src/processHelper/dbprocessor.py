import pymysql, os, csv

class DBProcessor:

    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", password="cuong", db="originenglishdictionary", charset='utf8')
        self.cursor = self.conn.cursor()

    def writeAllToDataBase(self, entries_crawled):

        conn = pymysql.connect(host="localhost", user="root", password="cuong", db="originenglishdictionary", charset='utf8')
        cursor = conn.cursor()

        for key, value in entries_crawled.items():
            word = key
            print('word to save to db', word)
            pos = value['pos']

            query_word = 'INSERT INTO word(name, pos) VALUES (%s,%s)'

            cursor.execute(query_word, (word, defin, pos))
            conn.commit()

            wordid = cursor.lastrowid

            definitionsWithExamples = value['definitionsWithExamples']
            query_definition = 'INSERT INTO definition(def, idword) VALUES(%s,%s)'

            for definition in definitionsWithExamples:
                defin = definition['def']
                cursor.execute(query_definition, (defin, wordid))
                conn.commit()

                defin_id = cursor.lastrowid

                examples = definition['examples']
                query_example = 'INSERT INTO example(sentence, idword) VALUES (%s,%s)'

                for ex in examples:
                    cursor.execute(query_example, (ex, defin_id))
                    conn.commit()

            phonetics = value['phonetic']
            query_phonetic = 'INSERT INTO phonetic(prefix, ipa, sound, idword) VALUES(%s,%s,%s,%s)'
            for phonetic in phonetics:
                cursor.execute(query_phonetic, (phonetic['prefix'], phonetic['ipa'], phonetic['sound'], wordid))
                conn.commit()

        cursor.close()
        conn.close()

    def writeEachWordToDataBase(self, word, wordContent):
        conn = pymysql.connect(host="localhost", user="root", password="cuong", db="originenglishdictionary", charset='utf8')
        cursor = conn.cursor()

        print('word to save to db', word)
        pos = wordContent['pos']

        query_word = 'INSERT INTO word(name, pos) VALUES (%s,%s)'

        cursor.execute(query_word, (word, pos))
        conn.commit()

        wordid = cursor.lastrowid

        definitionsWithExamples = wordContent['definitionsWithExamples']
        query_definition = 'INSERT INTO definition(def, idword) VALUES(%s,%s)'
        for definition in definitionsWithExamples:
            defin = definition['def']
            cursor.execute(query_definition, (defin, wordid))
            conn.commit()

            defin_id = cursor.lastrowid

            examples = definition['examples']
            query_example = 'INSERT INTO example(sentence, iddef) VALUES (%s,%s)'

            for ex in examples:
                cursor.execute(query_example, (ex, defin_id))
                conn.commit()

        phonetics = wordContent['phonetic']
        query_phonetic = 'INSERT INTO phonetic(prefix, ipa, sound, idword) VALUES(%s,%s,%s,%s)'
        for phonetic in phonetics:
            cursor.execute(query_phonetic, (phonetic['prefix'], phonetic['ipa'], phonetic['sound'], wordid))
            conn.commit()

        cursor.close()
        conn.close()

    def checkWordExisting(self, word):
        query = 'SELECT COUNT(idword) FROM word WHERE name=%s'
        self.cursor.execute(query, (word))
        result = self.cursor.fetchone()

        if result[0]:
            return True
        return False

    def getDictionary(self):
        query = 'SELECT name, def FROM word, definition WHERE word.idword = definition.idword'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_raw_dictionary_from_file(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                return list(reader)
        return []