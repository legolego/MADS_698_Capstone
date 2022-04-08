import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from pathlib import Path

img_path = Path(__file__).parents[1] / 'streamlit/images/NextBigThingHeader.png'

image = Image.open(img_path)

# import import_ipynb
# import find_category_from_thing_final as fc
# from nbt_utils import hello, graph_sent, get_wikipedia_search_results

st.title('Next Big Thing!!')
st.image(image, caption='The Thing vs The Thing vs Thing')

st.markdown("""Find the next big thing!""")

nbt_input = st.text_input('Find the next big thing like...', 'type here')

# list_of_choices = get_wikipedia_search_results(nbt_input)
# list_of_choices.insert(0, 'Select one')
# print(list_of_choices)


# if nbt_input not in ['type here', '']:

#     wiki_selection = st.selectbox(
#     'Can you please narrow down your query?',
#     list_of_choices)

#     st.write('You selected:', wiki_selection)

#     if wiki_selection != 'Select one':
#         #Get category
#         category = fc.get_category_from_search_term(wiki_selection)
#         #print(category)

#         #Get subreddits

#         #Get influencers

#         #Get relevant influencers posts

#         #Extract relevant phrases to category

#         #Select final answer

#         #nbt = 'next big thing'
#         nbt = category[0]

#         length = len(nbt_input)

#         st.write('"',' '.join(category),'"', ' is the category of the next big:', wiki_selection, length)