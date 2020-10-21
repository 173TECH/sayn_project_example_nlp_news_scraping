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
    text_name = text_field.split("_")[0]
    df[text_name + "_letters"] = df[text_field].fillna("").str.len() # counts the number of letters in text_field
    df[text_name + "_words"] = df[text_field].fillna("").apply(lambda x: len(word_tokenize(x, language=language))) #  counts the number of words in text_field
    df[text_name +"_sentences"] = df[text_field].fillna("").apply(lambda x: len(sent_tokenize(x, language=language))) # counts the number of sentences in text_field


# Automated word cloud generating function

def word_cloud(name, text, stopwords, b_colour = "white", c_colour = "firebrick"):
    try:
        mask = np.array(Image.open(f"python/img/masks/{name}_mask.png"))
    except:
        mask = None
    wordcloud = WordCloud(stopwords=stopwords
                          , max_words=100
                          , mask=mask
                          , background_color = b_colour
                          , contour_width=1
                          , contour_color= c_colour).generate(text)
    wordcloud.to_file(f"python/img/{name}_wordcloud.png")
# Uncomment if you want to show plots
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()


# Standard set of STOPWORDS

def words():
    return set(STOPWORDS)
