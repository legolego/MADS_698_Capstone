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
     "Choose view:",
     ('Blog', 'Precalculated Results'))

# Table of contents for navigation

st.sidebar.markdown("Navigation")
st.sidebar.markdown("[Introduction](#introduction)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 1](#step-1-find-category-from-thing)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 2](#step-2-find-subreddits)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 3](#step-3-find-influencersg)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 4](#step-4-find-influencer-relevevant-posts)", unsafe_allow_html=True)
st.sidebar.markdown("[Step 5](#step-5-find-next-big-thing)", unsafe_allow_html=True)
st.sidebar.markdown("[Ideas for Next Steps/Improvements](#ideas-for-next-steps-improvements)", unsafe_allow_html=True)
st.sidebar.markdown("[Statement of Work](#statement-of-work)", unsafe_allow_html=True)


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

    st.subheader("Motivation and Premise")

    st.markdown('''Being unfamiliar with it prior to this project, we were pretty shocked to realize the depth and reach of Reddit when 
        considering using it for our master’s Capstone project. According to statistics from 2020 found in [10 Reddit Statistics Every 
        Marketer Should Know](https://www.oberlo.com/blog/reddit-statistics#:~:text=The%20number%20of%20subreddits%20has,(Reddit%20Metrics%2C%202021).), 
        there are more than 52 million daily active Reddit users worldwide, many of whom are from the United States. In the US there are nearly 
        222 million monthly active users and 18% of American adults say they are Reddit users.''') 

    st.markdown('''What differentiates Reddit from other social media networks is its structure around communities, known as subreddits. All 
        conversations on Reddit take place within a community with the intention that all posts and comments focus on the specific topic(s) 
        that the subreddit was created for. This means that if you look at the activity within a subreddit, you can safely assume that it will 
        focus on the content you care about. Reddit has moderators within each subreddit that enforce community rules, such as the type of 
        posts that are and are not allowed, including staying on topic.''')

    st.markdown('''As shown on the [Metrics For Reddit](https://frontpagemetrics.com/list-all-subreddits) website, which runs statistics on 
        a weekly basis, there are currently over 3.4 million subreddits on Reddit. With all of this conversation going on around specific 
        topics, we wondered if it would be possible to mine the Reddit data to see what people are talking about, and maybe to be able to 
        identify upcoming trends. We wondered - if we are interested in a specific “Thing”, can we use people’s Reddit conversations to find 
        similar items that are coming into the public eye? Can we find the “Next Big Thing”?''')

    st.subheader("Current Available Tools")

    st.markdown('''Reddit provides the ability to see the top items that are trending across the platform, as well as the ability to 
        see what is trending within a subreddit. Additionally, there are many useful tools that have been developed for analyzing Reddit 
        data. Here are just a few examples:''')

    st.markdown('''
        - There are tools available that allow you analyze a specific subreddit or user. One is [Redective](https://www.redective.com/), which provides information about subreddit usage such as word frequencies found in posts and daily timing of posts.
        - [Socialgrep](https://socialgrep.com/) allows you to search for keywords, see subreddits where the keywords are found, how often they are found, top users mentioning the keywords, location of use, and the sentiment of text where they were used.
        - There are several excellent tools for analyzing users. [Karmalb](https://www.karmalb.com/) is a leaderboard that allows you to find users with the current highest Karma values. [Redditmetis](https://redditmetis.com/) and [Reddit-User-Analyser](https://reddit-user-analyser.netlify.app/) take this up several notches by providing post and comment sentiment analysis for users along with their post and activity patterns.''')

    st.markdown('''These tools all serve a purpose, but none of them have the functionality to allow a user to isolate a particular area 
        of interest, and find out what is trending in this area of interest across subreddits, as our tool does. The ability to interrogate 
        Reddit communities to see new items that its influential users are discussing has potential applications in many areas. Some examples 
        are:''')

    st.markdown('''
        - Identify products that are getting popular or losing popularity over time
        - Find new investment opportunities 
        - Determine what Redditors are concerned about, with the goal of providing information and/or assistance
        - Identify the latest subfield in a field of study
        - Perform market research on emerging trends in an industry
        - Use results as part of a Reddit subreddit recommender system''')

    st.subheader("Ethical Concerns")

    st.markdown('''In terms of ethical concerns with our project, we are storing the user name and post data for our influential users. 
        We do not display this combined information, but it is available in the data structures created throughout our pipeline. So, 
        through our project, a user can be associated with a certain topic that they may not want to be publicly associated with. However, 
        one benefit of using Reddit data is that Reddit does not require users to display their name or other identifying information, so 
        Redditors can operate with anonymity if they choose to.''')

    st.markdown('''In terms of content that may discuss unethical topics or practices, we have excluded any subreddits that are “nsfw” or 
        Not Safe For Work. However, we are not limiting what users enter into the tool, so it is possible that someone could search on a 
        topic that is unethical. In doing so, a user may be able to use our tool as a resource in gathering information that is unethical 
        and/or potentially harmful to others. We do not currently have a way to address this situation, but it is definitely something that 
        should be considered if additional versions of the product are developed.''')

    st.header("How to Identify 'The Thing'")

    st.markdown('''In our application, the user chooses a specific item that he or she has some interest in. For example, if you are a big 
    fan of “Squid Game”, a South Korean TV series on Netflix, you would enter “Squid Game”. The item should definitely be specific, 
    because we are going to try to find things like “Squid Game” for you, such as “Twenty-Five Twenty-One”, another South Korean TV Series. 
    If you were to enter “tv series”, then our application will look for other things like “tv series”, such as “podcasts” or “miniseries”. 
    In other words, our tool is made to look for “siblings” of The Thing you enter.''')

    st.header("Step 1: Find Category from Thing")

    st.subheader("NLP Category")

    st.markdown('''Once we know The Thing as identified in Wikipedia, we create two types of categories from the article.
        The first is an NLP category, as generated from the first sentence of the Wikipedia summary which is the text located at the top
        of any Wikipedia article. Our NLP rules have a little flexibility but rely on the first sentence having a structure of *The Thing* **IS A** *so-and-so…*''')
                 
    st.markdown('''After dependency and part-of-speech parsing with the Stanza library,
        we can see something like the sentence shown in our “star chart” below, with the Root word generally being the grammatical object 
        of the grammatical subject of the first sentence. This worked for all of our example terms except for “Gamestop short squeeze”.
        One simple rule we added was that if the Root, as parsed by Stanza,  turned out to be the first word in the sentence, then the new 
        Root would be a word with a [Universal Dependencies](https://universaldependencies.org/u/dep/ "Universal Dependencies") relationship of
        *nsubj:pass* or *parataxis* (passive nominal subject and parataxis like "I came, I saw, I conquered") to that first word. 
        This seemed to work well for other examples we tried, like the *Lost TV series*.''')

    st.image(get_image('star_chart_Squid_Game.gv.png'), caption="Example 'star chart' for Squid Game (click arrows in top-right to expand)")

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
    To build our NLP Category, we traversed the sentence graph to make a list of all words with a relationship of
    *obl*, *compound*,*amod*,*nmod*,*conj* or *appos* (oblique nominal, compound, adjectival modifier, nominal modifier, 
    conjunction, or appositional modifier) with the Root word. This will turn the first sentence of the Squid Game article:
    - "Squid Game (Korean: 오징어 게임; RR: Ojing-eo Geim) is a South Korean survival drama television series created by Hwang Dong-hyuk for Netflix.”

    into

    - ['Korean', 'drama', 'television', 'series']

    There is a balance that needs to be found between returning too many words here, and too few. If 'South' and 'survival' were brouight back there,
    other search terms would have brought back too many.
    ''')

    st.subheader("Wikipedia Categories")

    st.markdown('''In addition to the NLP Category for the item of interest, we can also easily get the associated Wikipedia entry
    categories. A problem with these though, is that some of the categories are actually the item itself, and some are too far 
    away conceptually from our item of interest. Squid Game has relevant categories like “2021 South Korean television series debuts” 
    and “South Korean thriller television series”. It also has a category like “Criticism of capitalism” which while true,
    is probably not what most people are looking for when they’re trying to find a “sibling” to Squid Game. 
    The Wikipedia category of “Squid Game” is also available, but articles in this category are things that are “children”
    of Squid Game, such as the 'Crab Game' and characters, also things we’re not looking for.   
    
    ''')

    st.markdown('''
    The solution we used to filter the Wikipedia categories was to use the [Sentence Transformer](https://huggingface.co/sentence-transformers)
    library with huggingface models to make a sentence vector for our found NLP category as well as all the categories from Wikipedia. 
    We used our NLP category as a ground truth, since a human chose it to describe the Thing. The first step was to remove any 
    Wikipedia category that was too similar to the Thing itself, since we’re not interested in its “children.” The next step was to keep at least two categories 
    of the remaining categories that were within a vector closeness threshold of the NLP category to the Wikipedia categories.    
    ''')

    st.markdown('''One last step for the categories was to look for any individual years or decades, i.e.1990s, mentioned in the Wikipedia categories, 
    and add new categories to the list with current timespans. We want things that are being talked about today, so to be safe we checked for the 
    existence of categories in Wikipedia with the year to be replaced with each of the last five years, and any mentioned 
    decades with “2020s”. If these categories existed, they were added to our list.    
    ''')

    st.markdown('''
    Squid Game wikipedia categories went from these:

    - 2021 South Korean television series debuts
    - Battle royale
    - Criticism of capitalism
    - Death games in fiction
    - Korean-language Netflix original programming
    - South Korean action television series
    - South Korean horror fiction television series
    - South Korean thriller television series
    - Squid Game
    - Television series impacted by the COVID-19 pandemic
    - Television series set on fictional islands
    - Television shows about death games
    - Television shows set in Seoul
    ''')

    st.markdown('''
    To this, which we refer to as our “Best Wiki categories”:
    - 2021 South Korean television series debuts
    - South Korean action television series
    - South Korean horror fiction television series
    - South Korean thriller television series
    - Television shows set in Seoul
    ''')
      
    st.markdown('''
    And finally with added years to these:
    - 2021 South Korean television series debuts
    - South Korean action television series
    - South Korean horror fiction television series
    - South Korean thriller television series
    - Television shows set in Seoul
    - 2018 South Korean television series debuts
    - 2019 South Korean television series debuts
    - 2020 South Korean television series debuts
    - 2022 South Korean television series debuts
    ''')

    st.subheader('Failed Whitelist Search')

    st.markdown('''
    Our NLP category and the filtered Wikipedia categories were enough to go on to the next step of searching Reddit 
    for relevant subreddits, but we also needed more information from Wikipedia to help us in Step 5 when it became time to
    isolate and identify siblings of The Thing. A simple solution we tried was to just make a whitelist of all the 
    article names in all of the relevant Wikipedia categories we found. We didn’t have a lot of faith in this 
    actually working in the final step, but a small edit was made to this list to look for words that were 
    too common in the list of article titles from each Wikipedia category. If too 
    many automobile manufacturers, for example, had the word “Company” in the article title, we removed it.
    ''')  

    st.markdown('''
    We didn’t think a whitelist of search terms would work well because we would be limited to only the terms 
    in the whitelist, and not be able to find ones we don’t know about. Even searching text for terms in 
    the whitelist is problematic because many uses would not be exactly like in the whitelist. People don’t 
    say “Ford Motor Company” everytime they talk about a Ford. Removing the word Company above was an attempt 
    to help this. We did also try fuzzy matching of items in the whitelist against the text of found posts and 
    comments from Reddit using the rapidfuzz library. This was guaranteed to bring back results from our whitelist, 
    but accuracy was poor. Most terms brought back this way were not in the text at all. Multi-word phrases 
    having a very close match on one of its words were found often, as well as exact matches for short 
    words that could appear as parts of other words. Tuing accuracy thresholds based on word length didn't help either.
    ''')

    st.markdown('''Fuzzy matching against the whitelist was abandoned in favor of the Conditional Random Field model. 
    We realized that we could use machine learning to classify words of interest in Reddit posts, so we also went back 
    to collect up to 200 Wikipedia articles from each category that we could use as automatically labeled training data. 
    We’ll talk about this more in Step 5.
    ''')

    st.markdown('''What we’re really doing here with Wikipedia is using it as a knowledge graph, without the associated 
    costs of maintenance, but with the added cost of retrieval time over an API. Since Wikipedia has articles in categories, 
    it is quite easy to get things that are “siblings” to each other, as well as find “parents” or categories of things. 
    This hierarchy is important for us to be able to traverse, so we can find the right kinds of things. This can also be 
    thought of as a graph, with article nodes attached to multiple category nodes through edges of an “in_Category”-type, for example.
    ''')

    st.header("Step 2: Find Subreddits")

    st.markdown('''Now that we know what categories The Thing belongs to, it’s time to move to Reddit. We need to find the 
        subreddits where people are talking about other things like The Thing. We pondered how to choose the best subreddits to examine 
        for the Next Big Thing. We considered downloading all of them and creating a search algorithm customized to our task, but quickly 
        realized this would be difficult as subreddits are constantly changing. In the end we decided that Reddit had probably put a lot 
        of work into their own search API so that their users could find the right place to participate. We dug into the different ways 
        to [search a subreddit using PRAW](https://praw.readthedocs.io/en/stable/code_overview/reddit/subreddits.html). We quickly found 
        that the search_by_topic endpoint, which would have been a perfect fit, is no 
        longer supported. This left us with subreddit.search and subreddit.search_by_name. Some testing showed that search_by_name didn’t 
        provide any additional results other than subreddits that are “not suitable for work” (nsfw) or have a pretty small number of 
        subscribers, neither of which we wanted. So, we were left with subreddit.search.''')
        
    st.markdown('''With the API endpoint identified, it was time to figure out what search terms to use to return the best subreddits. 
        We started off by using the NLP category words for The Thing: ''')
       
    st.code('''['Korean', 'drama', 'television', 'series']''')
        
    st.markdown('''Using these words we built four search terms, starting from the last word and concatenating each new word to the left. For 
        Squid Game this resulted in:''')
    
    st.code('''['series', 'television series', 'drama television series', 
    'Korean drama television series']''')
    
    st.markdown('''After running all four search terms through the subreddit.search API, creating a unique set of results, removing 
        nsfw subreddits, subreddits with less than 20K subscribers, and subreddits with no posts in the last 3 days, we were left with over 
        80 subreddits. In order to narrow this down to a more manageable number of subreddits to explore, we used the SentenceTransformer library 
        to calculate cosine similarity between different combinations:''')

    st.markdown('''
        - Subreddit display name to Wikipedia summary paragraph of The Thing
        - Subreddit details to Wikipedia summary paragraph of The Thing, where the subreddit details were a concatenation of the subreddit display name, subreddit title, and subreddit description
        - Subreddit details to the best Wikipedia categories for The Thing (average over all categories)''')
    
    st.markdown('''We found the best precision when using the best Wikipedia categories, so we took the average cosine similarity, and chose 
        the top 20 subreddits.''')

    st.markdown('''For example, for the r/manga subreddit:''')

    st.image(get_image('r_manga.png'), caption = None)

    st.markdown('''We built this string:''')

    st.code('''"manga./r/manga: manga, on reddit..Everything and anything manga! (manhwa/manhua 
        is okay too!) Discuss weekly chapters, find/recommend a new series to read, post a picture 
        of your collection, lurk, etc!”''')

    
    st.markdown('''and ran cosine similarity between it and each of the best Wikipedia categories identified earlier. 
        We then took the average cosine similarity in order to rank the results. This resulted in the following subreddits, 
        in ranked order from most relevant to least relevant: ''')

    st.code('''['MangaCollectors', 'GlobalOffensive', 'manga', 'anime', 'ObscureMedia', 
    'startrek', 'television', 'scifi', 'dvdcollection', 'Documentaries', 'WoT', 
    'doctorwho', 'StarWarsLeaks', 'XboxSeriesS', 'Sonsofanarchy', 'danganronpa', 
    'ActionFigures', 'movies', 'StarWars', 'entertainment']''')

    st.markdown('''We had originally made a conscious decision to not directly search on the original term, ‘Squid Game’, 
        because we were worried we would get back subreddits that only spoke about Squid Game and nothing else. But 
        looking at the list returned, we realized that maybe we might be missing out on some relevant subreddits. So 
        we tried adding in a direct search on Squid Game, along with our other search terms. This produced a different 
        set of results: ''')

    st.code('''['KDRAMA', 'korea', 'squidgame', 'MangaCollectors', 'NANIKPosting', 
    'GlobalOffensive', 'manga', 'anime', 'yourturntodie', 'ObscureMedia', 'startrek', 
    'television', 'scifi', 'dvdcollection', 'Documentaries', 'WoT', 'doctorwho', 
    'StarWarsLeaks', 'XboxSeriesS', 'GachaClubCringe']''')

    st.markdown('''75 percent of the subreddits are the same between the two groups, however, noticeable additions with 
        the inclusion of the original search term are the r/KDRAMA and r/korea subreddits, both of which could contain 
        relevant posts. Also, we see that our results are not filled up with Squid Game specific subreddits, there is 
        only one.''')

    st.markdown('''In examining our results, we noticed that the first 10 subreddits returned based on cosine 
        similarity tended to be more relevant than the last 10. To more empirically determine the best method 
        for subreddit searches we completed a manual evaluation of the precision of our results focusing on two 
        components, each with two options: subreddits returned with category words only vs. subreddits returned 
        with category words plus the original term, and precision at 10 subreddits vs. precision at 20 subreddits. 
        The following chart shows that in 8 of our 10 test cases, using the Category and Term with only 10 
        subreddits returned the highest precision of the four options.''')

    st.image(get_image('subreddit_eval_optimal.png'), caption = None)

    st.markdown('''While performing test runs of new search items , we realized that it might be beneficial to search 
    directly on the best Wikipedia categories for The Thing, such as ‘Television shows set in Seoul’. We tested adding 
    this search to our existing searches and reviewed the results, again by manually determining if each subreddit 
    returned was relevant. Our results, seen in the following chart, showed that adding the Wikipedia Categories did 
    not provide better results, so we returned to our original method of using the NLP Categories and the original search term:''')


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

    st.subheader('Conditional Random Field')

    st.markdown('''Now that we have some relevant posts to search through, how do we know what we’re even looking for? 
    Our first attempt was the whitelist and fuzzy match, described at the end of Step 1. This wasn’t working well, so we 
    discussed the challenge with  Professor David Jurgens, and he gave us the idea of using a 
    [Conditional Random Field](https://albertauyeung.github.io/2017/06/17/python-sequence-labelling-with-crf.html/ ) 
    (CRF) model to find the kinds of words 
    we’re looking for. This was brand new to us, but we were eager to try.
    ''')

    st.markdown('''CRFs are a class of statistical modeling methods used for structural prediction that can take context 
    into account. A graphical model is used to represent the presence of dependencies between predictions, which in the case 
    of natural language processing would be words immediately neighboring the target word.''')

    st.markdown('''Our goal was to find words in the unseen Reddit posts that were of the same category as the Thing. 
    What David Jurgens helped us realize was that we basically had a great training corpus that just needed to be labeled. 
    For each Wikipedia category that our Thing belonged to, we were able to collect up to 200 articles. The number 200 was 
    chosen to make sure the corpus didn’t get too large, as some categories can have over a thousand articles, so this 
    isn’t an exhaustive list of articles. We were limited to 5GB of memory in Deepnote, and did hit this limit a few times.
    ''')

    st.subheader('Training Data')
    
    st.markdown('''We know the title of each article, so we just needed to tag each word in each 
    article with a binary label, ‘Y’ and ‘N’ in our case, if each word was indeed part of the title. This wasn’t perfect, 
    especially with names of people, as someone’s name in the title doesn't usually include their middle name, 
    but the first sentence of Wikipedia often does include middle names. We were looking for the identical phrase, 
    so this prevented some valid names/words from being tagged correctly.''')

    st.markdown('''One trick that helped a Wikipedia title to be parsed as a sentence was to include it 
    in a new “first” sentence before the Wwikipedia article itself, i.e. “Squid Game” is a thing. (quotation marks included) 
    This kept the phrase together so Stanza could correctly parse it, and it was used in a complete sentence instead of just as a phrase.
    This also reduced and one extra call to Stanza per article.''')

    st.markdown('''We used the Stanza dependency parser to get each word’s part of speech, and then we were able to build out 
    our training set. We started making our training set with each row being a tuple of three items, the word, its part of 
    speech, and a Y/N label as to whether it was part of an exact match to the complete phrase in the Wikipedia article title or not. Features were 
    then further added to take into account things like whether the neighboring words were upper or lower case, 
    started with a capital letter, or were digits. This led to a very imbalanced data set, with fewer than 2% of rows having 
    a ‘Y’ tag, and the rest having an ‘N’ tag. Labeling Wikipedia article text was quite time consuming, on the order of an hour or longer, 
    but training the model was surprisingly fast, usually no longer than 2 minutes each time.
    ''')

    st.markdown('''Once we had built a trained tagger to tag individual words, we tested it on a 20% sized test set. Because of the imbalance, the 
    returned precision and recall was always at least 99% for N’s. Our target was the Y’s, and here precision and recall was 
    lower. Precision and recall was as low as 70%/53% respectively for mentions of things like Elon Musk and IPhone, but 
    got as high as 90%/86% respectively for Catan, the board game.
    ''')

    st.subheader('Classification')

    st.markdown('''One decision we made was to combine all of the articles in each category into a single category, which could be 
    thought of as a generic Thing-type category, because some Wikipedia categories had very few articles available to train on. We had 
    to assume that articles in different categories were in fact siblings to each other, when this wouldn’t always be true. 
    This did help simplify the classification step, as each unseen Reddit post would only have to be compared against a single model, 
    instead of one for each category. Parsing and labeling each unseen Reddit post turned out to be quite time consuming, but 
    classifying wasn’t too bad. Once we had every word labeled, we went back to extract and collect phrases that were labeled with 
    a ‘Y’. ''')
    
    
    st.markdown('''For a comparison, we also looked for exact matches of each of the CRF-found matches, as well as exact matches from 
    the original whitelist of article titles we saved back in Step 1. The original whitelist missed many, as we had expected, 
    but the exact CRF whitelist match did find mentions that the model did not. We ended up using the exact CRF whitelist 
    match as a number with which to calculate recall for phrases found with CRF. The final output of this step was a 
    dataframe with a column representing the found Entities, as well as counts for the number of times each was found in the unseen posts.
    ''')



    df = pd.read_csv( Path(__file__).parents[1] / 'streamlit/example_output/crf_results_Squid_Game.csv')
    # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

    st.dataframe(df)

    st.header('Ideas for Next Steps/Improvements')

    st.header("Statement of Work")

    st.markdown('''**_Kim Di Camillo_** - Co-authored the idea for the Next Big Thing and created the initial high level project design; 
    Designed, developed, tested, and evaluated Step 2: Find Relevant Subreddits, and Step 4: Find Relevant Influential User Posts; wrote 
    the project readme file; Handled general project management tasks to keep the team on schedule and ensure we included all required 
    components in our deliverables. ''')
    
    st.markdown('''**_Oleg Nikolsky_** - Co-authored the idea for the Next Big Thing and created the initial high level project design; 
    Designed, developed, tested, and evaluated Step 1: Find Category from Thing, and Step 5: CRF Find New Terms; setup and
    maintained project GitHub; ''')
    
    st.markdown('''**_Cody Crow_** - Designed, developed, tested Step 3: Finding Influencers, Drafted final project video presentation
    and coordinated recording and production of final video, created intitial instance of streamlit and blog outline.''')