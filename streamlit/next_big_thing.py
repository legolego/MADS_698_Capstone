import numpy as np
import pandas as pd
import streamlit as st
import os
from PIL import Image
from pathlib import Path

from nbt_utils import get_mvp_terms, make_wordcloud



def get_image(img_name):
    img_path = Path(__file__).parents[1] / str('streamlit/images/' + img_name)
    image = Image.open(img_path)
    return image

st.sidebar.subheader("About")
st.sidebar.markdown("Want to find the next big thing like Squid Game? or Dogecoin? Our application will filter through Reddit to find the next big thing like something you're interested in.")
st.sidebar.markdown('##')
st.sidebar.subheader("Contributors")
st.sidebar.markdown("Oleg Nikolsky, Kim Di Camillo, Cody Crow")
st.sidebar.markdown('##')

mode = st.sidebar.radio(
     "Try out the App",
     ('Blog Mode', 'App Mode'))

# Table of contents for navigation

st.sidebar.markdown("Navigation")
st.sidebar.markdown("[Introduction](#introduction)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 1](#step-1-find-category-from-thing)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 2](#step-2-find-subreddits)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 3](#step-3-find-influencersg)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 4](#step-4-find-influencer-relevevant-posts)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 5](#step-5-find-next-big-thing)", unsafe_allow_html=True)

st.sidebar.markdown('##')
git_url = 'https://github.com/legolego/MADS_698_Capstone'
st.sidebar.markdown("Source Code on [Github](%s)" % git_url)


st.image(get_image('NextBigThingHeader.png'))

if mode == "App Mode":
    term = st.selectbox('Select a Thing', get_mvp_terms())

    term_edit = term.replace(" ","_")

    term_location = Path(__file__).parents[1] / 'streamlit/example_output' / str('crf_results_' + term_edit + '.csv')
    df_filepath = Path(__file__).parents[1] / term_location

    results_df = pd.read_csv(df_filepath)
    results_df.index += 1

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

    st.markdown('''Once we know The Thing as identified in Wikipedia, we use the Wikipedia library to read the first sentence of the summary,
        which is the text located at the top of any Wikipedia article. Our NLP rules have a little flexibility but rely on the first 
        sentence having a structure of *The Thing* **IS A** *so-and-so…*''')
                 
    st.markdown('''After dependency and part-of-speech parsing with the Stanza library,
        we can see something like the sentence shown in our “star chart” below, with the Root word generally being the grammatical object 
        of the grammatical subject of the first sentence. This worked for all of our example terms except for “Gamestop short squeeze”.
        One simple rule we added was that if the Root, as parsed by Stanza,  turned out to be the first word in the sentence, then the new 
        Root would be a word with a [Universal Dependencies](https://universaldependencies.org/u/dep/ "Universal Dependencies") relationship of
        *nsubj:pass* or *parataxis* (passive nominal subject and parataxis like "I came, I saw, I conquered") to that first word. 
        This seemed to work well for other examples we tried, like the *Lost TV series*.''')

    st.image(get_image('star_chart_Squid_Game.gv.png'), caption="Example 'star chart' for Squid Game")

    st.markdown('''If you look at our “Star Chart”, you can see that each sentence is basically parsed into a network or graph, with each node
     being a word, and each edge between words being labeled with a relationship type. Stanza uses a list of dicts(seen below) with each parsed word's
     `head` property to indicate the word to which the current word is attached, through the `deprel` relationship. These properties were used
      to build the “star chart” in Graphviz.    
    ''')
    
    st.code('''
    [{'id': 1,
  'text': 'Squid',
  'lemma': 'Squid',
  'upos': 'PROPN',
  'xpos': 'NNP',
  'feats': 'Number=Sing',
  'head': 2,
  'deprel': 'compound',
  'start_char': 0,
  'end_char': 5},
 {'id': 2,
  'text': 'Game',
  'lemma': 'Game',
  'upos': 'PROPN',
  'xpos': 'NNP',
  'feats': 'Number=Sing',
  'head': 22,
  'deprel': 'nsubj',
  'start_char': 6,
  'end_char': 10},...]   
    ''', language='python')

    st.markdown('''
    To build our NLP Category, we traversed the sentence graph to make a list of all words with a relationship in
     *obl*, *compound*,*amod*,*nmod*,*conj* or *appos* (oblique nominal, compound, adjectival modifier, nominal modifier, 
     conjunction, or appositional modifier) with the Root word. This will turn the first sentence of the Squid Game article:
 “Squid Game (Korean: 오징어 게임; RR: Ojing-eo Geim) is a South Korean survival drama television series created by Hwang Dong-hyuk 
 for Netflix. Its cast includes Lee Jung-jae, Park Hae-soo, Wi Ha-joon, HoYeon Jung, O Yeong-su, Heo Sung-tae, Anupam Tripathi, and Kim Joo-ryoung.”

    ''')
      
    st.header("Step 2: Find Subreddits")
    
    st.header("Step 3: Find Influencers")

    st.markdown('''Once we have our list of relevant subreddits, our next step was to find influential redditors
                (users of reddit) within those subreddits. We will not be concerned about the Thing in this step
                 - we will strictly be looking to find the redditors who would be talking about the Next Big Thing.''')

    st.markdown('''When considering how to develop a ranking system for finding these influential Redditors, we wanted to ensure 
    that we were gathering not only Redditors with popular submissions and comments, but also Redditors that were recently active 
    in the subreddits. Our process for this involves the following steps: \n
    - Pull recent popular submissions from each subreddit
    - Gather all of the comments from each submission
    - Normalize and aggregate scoring for submissions and comments by author
    - Return list of ranked authors by scoring
    - Gather Top 250 ranked authors Karma Scores''')

    st.markdown('''For this step we will be working with PRAW: The Python Reddit API Wrapper (https://praw.readthedocs.io/) in order to gather all of the 
    necessary information. For our first step in finding influencers, we will use PRAW’s subreddit class to pull submissions 
    from each of our relevant subreddits identified in Step 2. The submissions are able to be gathered using a few different 
    methods like “hot”, “new”, or “top”. If you are familiar with Reddit, you will see that these appear at the top of the page.''')

    st.image(get_image('step3_posts_header.png'), caption = "Example Reddit header")

    st.markdown('''Being that we are looking for the Next Big Thing, we used the “top” method and set our timeframe to only look 
    at top posts within the last month. Throughout this process we experimented with the number of posts that we would pull back, 
    ultimately landing on something that was reasonable time-wise that still gave us some clear delineation on influencers when we 
    conducted our scoring. With the top 50 submissions per subreddit, we were pulling back 500 total posts with all of their comments. 
    As seen in the chart below, the number of comments per subreddit varied from 5,000 to 28,000.''')

    st.image(get_image('step3_num_comment.png'), caption = "Comments retieved from each subreddit")
    
    st.markdown('''A future improvement that we could incorporate is to weight our number of submissions per subreddit on the subreddit
     relevance scoring in order to pull back more submissions and comments from the most relevant subreddits.''')

    st.markdown('''Each of the submissions that we pull back have the author and the score for each post that we are going to utilize in 
    our next steps for ranking our influencers. “Score” in Reddit terms is the net of upvotes and downvotes - this is the same for both 
    comments and submissions.  The full list of submission attributes available from PRAW can be found here:
     https://praw.readthedocs.io/en/stable/code_overview/models/submission.html''')

    st.markdown('''Once we have retrieved our list of 50 submissions from each subreddit (500 in total) we now need to gather the comments 
    from each of the submissions. In our early attempts and inexperience working with PRAW, we were doing this in a separate request. 
    However, after understanding PRAW’s structure more, we realized that we are able to request all of the comments (in the form of a 
    CommentForest) with our submission request. Using this method saves a significant amount of time when gathering the comment information. 
    For the comments, we are going to again use the author name and score information to rank the authors.''')

    st.markdown('''Next we need to normalize all of the scores and rank the authors. To do this, we will normalize submissions and comments
     separately. The reason for this is that the scaling for submissions and comments are typically very different (i.e. a submissions score
      is normally much higher than a comments score since it is a parent-child relationship for the submission and comment)''')

    st.markdown('**_For each submission and comment: normalized score = score/(sum of all scores)_**')

    st.markdown('''Once the scores are normalized, we will then aggregate both submission scores and comments scores together by author to 
    get an author’s total score. Our first attempts produced satisfactory results, however, we decided to add another step in our process 
    later due to our analysis of the Reddit users. As a starting point, we took the top 50 scoring authors, regardless of subreddit 
    participation - below is a sample of scoring results from the test term Beastie Boys. As you can see, after the first 40-50 authors, 
    the scoring becomes flat.''')

    st.image(get_image('step3_author_score.png'), caption = "Scoring for top 250 ranked authors")

    st.markdown('''Upon review of our results in our next step, we observed that not all of the subreddits would have representation in 
    the influential authors list. We felt it was important that all relevant subreddits had representation in our returned list of influencers, 
    so our ranking was adjusted to take the top 5 authors from each subreddit. This avoids the issue of a less popular, but highly relevant 
    subreddit being ignored and not represented by our list of influencers. Below we will discuss some ways in which we could further improve 
    our influencer selection algorithm as a future refinement.''')

    st.markdown('''In our analysis of our chosen authors, we looked at Reddit’s “ranking” for its users (known as Karma) as a way to evaluate 
    how well we captured influencers. Karma is essentially the same as what a score is for submissions and comments, upvotes and downvotes, but 
    instead of scoring one item, it is scoring the user as a whole. In our evaluation, we checked to see if the users that we had identified were 
    within the top 1,000 for comment Karma. This website (https://www.karmalb.com) has a good tool that you can use to see rankings of Redditors over time. At present, to 
    rank in the top 1%, your Karma score would have to be approximately 24,000. To rank in the Top 10%, your Karma score would have to be 758.  
    The table below presents our top 250 scoring list to see how many influencers were within the top 1% and 10% of Redditors based on Comment Karma 
    rankings. From what you can see in the table, the results can vary - this is due to the popularity of the relevant subreddits. Our lowest count 
    of top 10% Redditors within our influencer top 250 for our test results was 173 (69%) - our lowest count for top 1% Redditors within our 
    influencer top 250 scoring was 34 (14%).''')

    st.image(get_image('step3_top1-10pct.png'), caption = "Top 250 Influecers within Top 1% and 10% of Comment Karma")

    st.markdown('''Once we finished some initial full run-throughs of our pipeline, we recognized that we would benefit from gathering additional 
    comments and submissions in Step 4 for our analysis, so we decided to alter our influencer list to include up to 125 authors and incorporate 
    influencer Comment Karma into our selection of authors. Our final ranking of authors balances overall Reddit popularity, individual submission/post 
    scoring (which inherently weights on a user’s activity within subreddits), and representation from each relevant subreddit. The makeup of our 125 
    influencers includes: \n
    - Top 50 ranked by Karma chosen from Top 250 authors based on submission/post scoring
    - Top 25 ranked by our author scoring algorithm (as described above) from remaining author list
    - Top 5 ranked by our author scoring algorithm from each of our 10 relevant subreddits from remaining author list
    - To be considered, authors must have posted a minimum of 2 times in the past month.''')

    st.header("Step 4: Find Influencer Relevevant Posts")


    st.header("Step 5: Find Next Big Thing")