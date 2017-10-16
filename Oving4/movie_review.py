from re import findall
from glob import glob
from itertools import zip_longest
from heapq import nlargest
from time import time
from math import log

class Review:
    def __init__(self,n_gram,stop_words):
        self.n_gram = n_gram
        self.stop_words = stop_words

    def read_1_file(self,filepath):
        words = findall("[\w][\w]*'?[\w][\w]?", open(filepath, encoding='utf-8').read().lower())
        if self.n_gram > 0:
            words += ['_'.join(words[x:x+self.n_gram])for x in range(0,len(words)-self.n_gram+1)]
        return set([word for word in words if word not in self.stop_words])

    def read_all_files(self,pos_files, neg_files):
        #tot_numb_of_files = len(pos_files) + len(neg_files)

        # Lager dictionaies for pos og neg ord
        pos_words, neg_words, tot_words = {}, {}, {}
        print("Training files...")
        for pos_file, neg_file in zip_longest(pos_files,neg_files): # Går gjennom alle reviews
            pos_list = self.read_1_file(pos_file)
            neg_list = self.read_1_file(neg_file)

            # Teller antall tilfeller at et ord
            for pos_word in pos_list:
                self.word_counter(pos_words, tot_words, pos_word)
            for neg_word in neg_list:
                self.word_counter(neg_words, tot_words, neg_word)

        # Fjerner alle ord som ikke er brukt i minst en hvis prosentandel av reviewsene (0.02)
        self.pruning(pos_words, tot_words, len(pos_files))
        self.pruning(neg_words, tot_words, len(neg_files))

        return pos_words, neg_words

    # Finnner de top25 mest brukte ordene, for hhv. posititve og negative reviews. Returnerer de som to dicts med informasjonsverdien som value
    def find_top_25(self,pos_files, neg_files):
        p, n = self.read_all_files(pos_files, neg_files)
        pos_words, neg_words = list(p.items()), list(n.items())
        pos_words, neg_words = nlargest(25, pos_words, key=lambda w:w[1]), nlargest(25, neg_words, key=lambda w:w[1])
        return pos_words, neg_words

    # Hjelpemetode for scoringssystemet som brukes i classifier
    def get_score(self,vokabular, word):
        score = 0
        try:
            score += log(vokabular[word])
        except KeyError:
            score += log(0.01)
        return score

    # Klassifiserer dokumentene i enten de to gruppene positiv, eller negativ
    def classify(self, path, pos_words, neg_words):
        print("Classyfying...")
        pos_reviews = []
        neg_reviews = []
        files = path
        for fil in files:
            words = self.read_1_file(fil)
            pos_score, neg_score = 0, 0
            for word in words:
                pos_score += self.get_score(pos_words, word)
                neg_score += self.get_score(neg_words, word)
            if pos_score > neg_score:
                pos_reviews.append(fil)
            else:
                neg_reviews.append(fil)
        if "pos" in path[0]:
            return len(pos_reviews) / len(files)
        else:
            return len(neg_reviews) / len(files)

    # Metode som fjerner alle ord som ikke er brukt i minst en hvis prosentandel av reviewsene (0.02)
    def pruning(self,dictionary, tot_dict, nr_of_files):
        print("Pruning...")
        for word in tot_dict:
            try:
                if tot_dict[word] / nr_of_files < 0.02:
                    dictionary.pop(word)
                    continue
                dictionary[word] = round(dictionary[word] / tot_dict[word], 4)
            except KeyError:
                pass
    # Metode som teller antall tilfeller at et ord
    def word_counter(self,dictionary, tot_dict, word):
        if word not in dictionary:
            dictionary[word] = 1
            tot_dict[word] = 1
        else:
            dictionary[word] += 1
            tot_dict[word] += 1

# Le Main
def main():
    start = time()
    stop_words =  set((findall(r"[\w][\w]*'?[\w][\w]?", open("/Users/wgkva/NTNU/OneDrive - NTNU/Datateknologi/2. klasse/TDT4113 - Programmeringsprosjekt/TDT4113/Oving4/data/data/stop_words.txt",
                                                             encoding='utf-8').read().lower())))
    train_pos_files = glob("/Users/wgkva/NTNU/OneDrive - NTNU/Datateknologi/2. klasse/TDT4113 - Programmeringsprosjekt/TDT4113/Oving4/data/data/alle/train/pos/*.txt")
    train_neg_files = glob("/Users/wgkva/NTNU/OneDrive - NTNU/Datateknologi/2. klasse/TDT4113 - Programmeringsprosjekt/TDT4113/Oving4/data/data/alle/train/neg/*.txt")
    test_pos_files = glob("/Users/wgkva/NTNU/OneDrive - NTNU/Datateknologi/2. klasse/TDT4113 - Programmeringsprosjekt/TDT4113/Oving4/data/data/alle/test/pos/*.txt")
    test_neg_files = glob("/Users/wgkva/NTNU/OneDrive - NTNU/Datateknologi/2. klasse/TDT4113 - Programmeringsprosjekt/TDT4113/Oving4/data/data/alle/test/neg/*.txt")

    review = Review(2,stop_words)

    #print(review.read_1_file())
    #print(review.find_top_25(train_pos_files,train_neg_files)) # Test for å finne top25-metoden
    #print(review.read_all_files(train_pos_files, train_neg_files)) # Test for read_all_files-metoden

    pos_vok, neg_vok = review.read_all_files(train_pos_files, train_neg_files) # Deklarerer vokabularet for hhv positive og negative
    pos = review.classify(test_pos_files, pos_vok, neg_vok) # Lager classifier for positive
    neg = review.classify(test_neg_files, pos_vok, neg_vok) # Lager classifier for negative
    print("Positive: ",pos*100, "%")
    print("Negative: ",neg*100, "%")
    print("Total:", ((pos+neg)/2)*100, "%")

    end = time()
    print("Tid:",(end-start))

main()