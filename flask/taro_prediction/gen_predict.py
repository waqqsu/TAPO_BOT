
import pandas as pd
import random
import numpy as np

class gen_prediction:
    def __init__(self, message):
         self.message = message
         self.tr = ''


    def choose_category(self):

        if self.message == "Общее":
            self.tr = pd.read_csv("taro_prediction/taro.csv", index_col=0)
        elif self.message == "Здоровье":
            self.tr = pd.read_csv("taro_prediction/taro_health.csv", index_col=0)
        elif self.message == "Прошлое, настоящее, будущее":
            self.tr = pd.read_csv("taro_prediction/taro_LifeTime.csv", index_col=0)
        elif self.message == "Любовь":
            self.tr = pd.read_csv("taro_prediction/taro_LifeTime.csv", index_col=0)
        elif self.message == "Карьера, деньги":
            self.tr = pd.read_csv("taro_prediction/taro_money.csv", index_col=0)
        else:
            self.tr = None


        return self.tr

    def random_cards(self):
        text_card = []
        name_card =[]
        for i in random.sample(list(self.tr.index), 3):
            text = self.tr['pred'][i]
            text_card.append(text)
            name_card.append(self.tr['card'][i])
        self.text = ''.join(text_card)
        self.names = ', '.join(name_card)

        return self.text, self.names

    def write_names(self):
        return "Вам выпали следующие карты: " + self.names


    def make_pred(self):
        corpus = self.text.split()

        def make_pairs(corpus):
            for i in range(len(corpus) - 1):
                yield (corpus[i], corpus[i + 1])

        pairs = make_pairs(corpus)

        word_dict = {}


        for word_1, word_2 in pairs:
            if word_1 in word_dict.keys():
                word_dict[word_1].append(word_2)
            else:
                word_dict[word_1] = [word_2]


        first_word = np.random.choice(corpus)

        while first_word.islower():
            first_word = np.random.choice(corpus)

        chain = [first_word]
        n_words = 80

        for i in range(n_words):
            try:

                chain.append(np.random.choice(word_dict[chain[-1]]))
            except Exception:
                pass



        def random_emoji():
            emoji = ['😂', '🥲', '😆', '🥰', '😍', '😘', '🥳', '🤩', '😎', '😝', '😋', '😳', '🤬', '🥵', '😱', '🙄',
                     '🤥',
                     '🤫', '🤤', '🤢', '🤮', '😈', '👹', '🤡', '💩', '👻', '💀', '🤡', '👽', '👍', '👌', '☝️', '💪',
                     '👀',
                     '🔫', '❤️', '💖', '❣️', '🖤', '💔', '🏳️‍', '🌈', '✨', '💋', '⭐️', '💦', '💸', '💤', '💫', '💅🏻',
                     '😭', '🥺', '👶', '😵', '🤯', '🤓', '😑', '💢', '💯', '💥', '💌', '💘', '👅']
            rand = random.sample(emoji, 3)
            rand = ''.join(rand)
            return rand

        pred = (' '.join(chain)).split('.')
        pred.pop(-1)
        em_pred=[]
        for i in pred:
            em_pred.append(i + f'{random_emoji()}')

        self.pred = '.'.join(em_pred)

        return self.pred


