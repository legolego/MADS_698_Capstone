
import numpy as np
import pickle
import pandas as pd
import datetime as dt
import os
from pathlib import Path
#import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import random



def get_mvp_terms():

    file_path = Path(__file__).parents[1] / 'streamlit/example_output/'
    file_list = os.listdir(file_path)
    term_list = []

    for f in file_list:
        if f.startswith("crf_results_"):
            term_list.append(f.replace(".csv", "").replace("crf_results_", "").replace("_"," "))
   
    return pd.Series(sorted(term_list))


def make_wordcloud(df, title = 'Top CRF Results'):
    res = dict(zip(df['Entity'].dropna(), df['CRF_Model_Found'].dropna().astype('int32')))
    def custom_color_func(word, font_size, position, orientation, random_state=None,
                        **kwargs):
        return "hsl(0, 100%%, %d%%)" % random.randint(30, 70)

    mask_filepath = Path(__file__).parents[1] / 'streamlit/images/reddit-logo5-2.jpg'
    reddit_mask = np.array(Image.open(mask_filepath))

    wordcloud = WordCloud(width=800,
                    height=800,
                    background_color="white", 
                        mask=reddit_mask,
                        contour_width=0, 
                        repeat=True,
                        min_font_size=3,
                        contour_color='red')

    # Generate a wordcloud
    wordcloud.generate_from_frequencies(res)
    
    wordcloud.recolor(color_func=custom_color_func, random_state=3)

    arr = wordcloud.to_array()
    
    return arr
    