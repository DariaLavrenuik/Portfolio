import pandas as pd
import random
from random import choice

import pyinflect
import spacy
import en_core_web_sm

from gensim.test.utils import lee_corpus_list
from gensim.models import Word2Vec
import gensim.downloader as api

model = api.load("glove-wiki-gigaword-100") 
nlp = spacy.load("en_core_web_sm")

class EnglishExercise():
   
    def choose_variant(self, row):
        random_var = random.choice([self.choose_verb_form, self.fill_the_gap, 
                                    self.choose_the_sent, self.select_word])
        row['type'] = random_var.__name__
    
        if row['type'] == 'choose_verb_form':
            return self.choose_verb_form(row)
        elif row['type'] == 'fill_the_gap':
            return self.fill_the_gap(row)
        elif row['type'] == 'choose_the_sent':
            return self.choose_the_sent(row)
        elif row['type'] == 'select_word':
            return self.select_word(row)
        else:
            return row

    
    
    def fill_the_gap(self, row):
        if row['type'] == 'fill_the_gap':
            
            token_list = []
            for token in nlp(row['raw']):
                if token.pos_ in ['ADJ', 'NOUN', 'VERB']:
                    token_list.append(token.text)
            if len(token_list) == 0:
                return row
            token_random = random.choice(token_list)
            row['options'] = []
            row['object'] = token_random
            row['answer'] = token_random
            row['description'] = 'Заполните пропуск'
            return row
    
    
    def choose_verb_form (self, row):
        token_list = []
        if row['type'] == 'choose_verb_form': 
            for token in nlp(row['raw']):
                if token.pos_ == 'VERB':
                    token_list.append(token)
        if len(token_list) == 0:
            return row
        token_random = random.choice(token_list)
        try:
            options = []
            if token_random.text == token_random._.inflect('VBG'):
                options.extend([token_random.text, token_random._.inflect('VBD'), token_random._.inflect('VBP')])
            elif token_random.text == token_random._.inflect('VBD'):
                options.extend([token_random.text, token_random._.inflect('VBG'), token_random._.inflect('VBP')])
            else:
                options.extend([token_random._.inflect('VBG'), token_random._.inflect('VBD'), token_random.text])
        
            random.shuffle(options)
            row['options'] = options
            row['type'] = 'choose_verb_form'
            row['answer'] = token_random.text
            row['description'] = 'Выберите правильный глагол'
            row['object'] = token_random.text
        except:
               pass
     
        return row  
    
    
    def choose_the_sent(self, row):
        token_list = []
        if row['type'] == 'choose_the_sent':
            words = row['raw'].split()
            if len(words) < 4 or len(words) > 10:
                return row
    
            new_sent_1, new_sent_2 = row['raw'], row['raw']
    
           
            for token in nlp(row['raw']):
                if token.pos_ in ['NOUN', 'VERB', 'ADJ']:
                    token_list.append(token)
            if len(token_list) == 0:
                return row           
                
            for token in token_list:
                try:

                    new_word_1 = model.most_similar(token.text.lower())[1][0]
                    new_word_2 = model.most_similar(positive = [token.text.lower(), 'bad'],
                                        negative = ['good'],
                                        )[2][0]

                    new_word_1 = new_word_1.title() if token.text.istitle() else new_word_1
                    new_word_2 = new_word_2.title() if token.text.istitle() else new_word_2
        
                    new_sent_1 = new_sent_1.replace(token.text, new_word_1)
                    new_sent_2 = new_sent_2.replace(token.text, new_word_2)
                except:
                    pass               
                    
                
                options = [new_sent_1, new_sent_2, row['raw']]
                row['type'] = 'choose the sent'
                row['options'] = options
                row['answer'] = row['raw']
                row['description'] = 'Выберите правильное предложение'      
                return row       
    
    def select_word (self, row):

        token_list = []
        if row['type'] == 'select_word':
            for i in nlp(row['raw']):
                if i.pos_ in ['NOUN', 'VERB', 'ADJ']:
                    token_list.append(i)
            if len(token_list) == 0:
                return row
            token_random = random.choice(token_list)
            try:
                options = [w[0] for w in model.similar_by_word(token_random.text.lower(), topn = 2)] + [token_random.text] 
        
                if token_random.text.istitle():
                    options = [x.title() for x in options]
                random.shuffle(options) 
                
                row['options'] = options 
                row['object'] = token_random.text
                row['answer']  = token_random.text
                row['description'] = 'Выберите наиболее подходящее слово'
            except:
                  pass
            return row   
