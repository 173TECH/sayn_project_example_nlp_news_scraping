### Uncomment the block below if you do not have punkt installed, you only need to run this once ###
# import nltk
# nltk.download('punkt')

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize, sent_tokenize

def desc_text(df, text_field, language):
    text_name = text_field.split("_")[0]
    df[text_name + "_letters"] = df[text_field].fillna("").str.len()
    df[text_name + "_words"] = df[text_field].fillna("").apply(lambda x: len(word_tokenize(x, language=language)))
    df[text_name +"_sentences"] = df[text_field].fillna("").apply(lambda x: len(sent_tokenize(x, language=language)))


def word_cloud(name, text, stopwords):
    try:
        mask = np.array(Image.open(f"python/img/masks/{name}_mask.png"))
    except:
        mask = None
    wordcloud = WordCloud(stopwords=stopwords
                          , max_words=100
                          , mask=mask
                          , background_color = "white"
                          , contour_width=1
                          , contour_color='firebrick').generate(text)
    wordcloud.to_file(f"python/img/{name}_wordcloud.png")
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def words():
    return set(STOPWORDS)
