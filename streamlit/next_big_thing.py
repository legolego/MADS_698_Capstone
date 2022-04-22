import numpy as np
import pandas as pd
import streamlit as st
import os
from PIL import Image
from pathlib import Path

from nbt_utils import get_mvp_terms, make_wordcloud

CURRENT_THEME = "dark"

img_path = Path(__file__).parents[1] / 'streamlit/images/NextBigThingHeader.png'
image = Image.open(img_path)

st.sidebar.subheader("About")
st.sidebar.markdown("Want to find the next big thing like Squid Game? or Dogecoin? Our application will filter through Reddit to find the next big thing like something you're interested in.")
st.sidebar.markdown('##')
st.sidebar.subheader("Contributors")
st.sidebar.markdown("Oleg Nikolsky, Kim Di Camillo, Cody Crow")
st.sidebar.markdown('##')
mode = st.sidebar.radio(
     "Try out the App",
     ('Blog Mode', 'App Mode'))

st.sidebar.markdown('##')
git_url = 'https://github.com/legolego/MADS_698_Capstone'
st.sidebar.markdown("Source Code on [Github](%s)" % git_url)


st.image(image, caption='The Thing vs The Thing vs Thingss')

if mode == "App Mode":
    st.header('App Mode')
    term = st.selectbox('Select a Thing', get_mvp_terms())

    term_edit = term.replace(" ","_")

    term_location = Path(__file__).parents[1] / 'streamlit/example_output' / str('crf_results_' + term_edit + '.csv')
    df_filepath = Path(__file__).parents[1] / term_location

    results_df = pd.read_csv(df_filepath)

    st.subheader('Top 10 Result Table for ' + term)    
    df_top10_crf = results_df[["Entity", "CRF_Model_Found"]].dropna().astype({'CRF_Model_Found':'int'}).head(10)
    df_top10_crf.columns = ['Next Big Thing?', 'Number Found']
    st.table(df_top10_crf)

    fig = make_wordcloud(results_df, title = 'Top CRF Results')
    st.image(fig)
    #st.pyplot(fig)

else:
    st.header("Introduction")

    st.header("Step 1: Find Category from Thing")
      
    st.header("Step 2: Find Subreddits")
    
    st.header("Step 3: Find Influencers")

    st.markdown("Once we have our list of relevant subreddits, our next step was to find influential redditors\
                (users of reddit) within those subreddits. We will not be concerned about the Thing in this step\
                 - we will strictly be looking to find the redditors who would be talking about the Next Big Thing.")

    st.markdown("Once we have our list of relevant subreddits, our next step was to find influential redditors\
            (users of reddit) within those subreddits. We will not be concerned about the Thing in this step\
                - we will strictly be looking to find the redditors who would be talking about the Next Big Thing.")
    
    st.header("Step 4: Find Influencer Relevevant Posts")

    st.header("Step 5: Find Next Big Thing")