### Uncomment the block below if you do not have punkt installed, you only need to run this once ###
# import nltk
# nltk.download('punkt')

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize, sent_tokenize

# Text stats generating function

def desc_text(df, text_field, language):
    df[text_field + "_letters"] = df[text_field].fillna("").str.len() # counts the number of letters in text_field
    df[text_field + "_words"] = df[text_field].fillna("").apply(lambda x: len(word_tokenize(x, language=language))) #  counts the number of words in text_field
    df[text_field +"_sentences"] = df[text_field].fillna("").apply(lambda x: len(sent_tokenize(x, language=language))) # counts the number of sentences in text_field


# Automated word cloud generating function

def word_cloud(name, text, stopwords, b_colour = "white", c_colour = "firebrick", show=False):
    try:
        mask = np.array(Image.open(f"python/img/masks/{name}_mask.png")) # attempt to find a compatible mask
    except:
        mask = None

    wordcloud = WordCloud(stopwords=stopwords
                          , max_words=100
                          , mask=mask
                          , background_color = b_colour
                          , contour_width=1
                          , contour_color= c_colour).generate(text)

    wordcloud.to_file(f"python/img/{name}_wordcloud.png") # store wordcloud image in "python/img"

    # declare show=True if you want to show wordclouds
    if show:
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()


# Standard set of STOPWORDS

def words():
    return set(STOPWORDS)
