import pickle
from pymorphy2 import MorphAnalyzer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nb import normalize_text
import nltk

# подгружаем необходимые словари
nltk.download('punkt')
nltk.download('stopwords')
morph = MorphAnalyzer()

path = "data/"
# загружаем сохраненные модель и векторизатор
# -- Модель SVC
# model = pickle.load(open(path + "model_svc.sav", 'rb'))
# vectorizer: TfidfVectorizer = pickle.load(open(path + "vec_svc.pk", 'rb'))
# -- Модель KNN
model = pickle.load(open(path + "model_knn.sav", 'rb'))
vectorizer: TfidfVectorizer = pickle.load(open(path + "vec_knn.pk", 'rb'))
# -- Модель LogReg
# model = pickle.load(open(path + "model_logreg.sav", 'rb'))
# vectorizer: TfidfVectorizer = pickle.load(open(path + "vec_logreg.pk", 'rb'))


def get_intent(text):
    # нормализуем и векторизируем текст
    vector = vectorizer.transform([normalize_text(text)]).toarray()
    # получаем распределение
    probability_distribution = model.predict_proba(vector)
    print(probability_distribution)

    if np.max(probability_distribution) > 0.5:
        return model.predict(vector)[0]


if __name__ == '__main__':
    print(get_intent("у вас парковка закрывается на обед"))
