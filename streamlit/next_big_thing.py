import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from pathlib import Path

from nbt_utils import get_wikipedia_search_results, get_stanza_dict_of_first_sentence, get_category_from_search_term, graph_sent, get_first_unambiguous_wiki_term_and_page



# https://stackoverflow.com/questions/69768380/share-streamlit-cant-find-pkl-file
img_path = Path(__file__).parents[1] / 'streamlit/images/NextBigThingHeader.png'
image = Image.open(img_path)


st.image(image, caption='The Thing vs The Thing vs Thing')

st.markdown("""Find the next big thing!""")


#st.write(get_stanza_dict_of_first_sentence("This is a senetce.").text)


nbt_input = st.text_input('Find the next big thing like...', 'type here')

list_of_choices = get_wikipedia_search_results(nbt_input)
list_of_choices.insert(0, 'Select one')
print(list_of_choices)


if nbt_input not in ['type here', '']:

    wiki_selection = st.selectbox(
    'Can you please narrow down your query?',
    list_of_choices)

    st.write('You selected:', wiki_selection)

    if wiki_selection != 'Select one':
        #Get category
        nlp_category_phrase, expanded_year_wiki_cats, best_wiki_cats, first_wiki_term = get_category_from_search_term(wiki_selection)
        first_wiki_term, wiki_page = get_first_unambiguous_wiki_term_and_page(wiki_selection)
        #print(category)

        #Get subreddits

        #Get influencers

        #Get relevant influencers posts

        #Extract relevant phrases to category

        #Select final answer

        #nbt = 'next big thing'


        st.write('"',' '.join(nlp_category_phrase),'"', ' is the NLP category of the next big:', wiki_selection)

        st.markdown("The first sentence from wikipedia is:", wiki_page.summary)

        st.write("Chase the arrow to expand the image of the word dependencies below. ----->")
        

        

        
     
        st.graphviz_chart(graph_sent(get_stanza_dict_of_first_sentence(wiki_page.summary)), use_container_width=False)