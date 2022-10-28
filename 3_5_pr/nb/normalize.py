from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')
# морфологический анализатор для русского языка
morph = MorphAnalyzer()

# подгружаем стоп слова для русского языка
stopwords_ru = stopwords.words("russian")


def normalize_text(text, stop_words=False):
    # приведение к нижнему регистру и токенизация
    text = nltk.word_tokenize(text.lower())

    # удаление стоп слов
    if stop_words:
        # фильтрация
        text = [token for token in text if token not in stopwords_ru]

    # лемматизация
    # для каждого токена в тексте приведение его к нормальной форме
    text = [morph.normal_forms(token)[0] for token in text]

    return " ".join(text)
