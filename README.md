# Next Big Thing Capstone Project
Capstone project for University of Michigan's Master of Applied Data Science program created by Cody Crow, Kim Di Camillo and Oleg Nikolsky. Given a user-entered item, the tool we built mines Reddit data to identify what popular Redditors are currently discussing that are "like" the original item.

# Getting Started
### Clone the repo
Clone this repository to get started.
```
git clone https://github.com/legolego/MADS_698_Capstone
```

### Prereqs
Get all of the dependencies needed by running the following:
```
pip install -r requirements.txt
```
### Tools
Our project uses the following tools. We have included some links to the documentation:


| Tool | Use | Link |
| ------ | ------ | ------ |
| Reddit | Main data source. APIs to access subreddit, submission, comment, and user data | https://praw.readthedocs.io/en/latest/getting_started/quick_start.html https://github.com/pushshift/api https://github.com/mattpodolak/pmaw#description |
| Wikipedia | Content source for siblings and training data | https://github.com/goldsmith/Wikipedia |
| Wikipedia API | Wikipedia category members | https://github.com/martin-majlis/Wikipedia-API |
| Pywikibot | Wikipedia category hierarchy  | https://www.mediawiki.org/wiki/Manual:Pywikibot |
| Stanza | Dependency parsing and part-of-speech tagging | https://stanfordnlp.github.io/stanza/ |
| Sentence Transformers | Text comparison via cosine similarity using the all-MiniLM-L6-v2 HuggingFace Model | https://www.sbert.net/   https://www.sbert.net/docs/pretrained_models.html|
| Pycrfsuite | Conditional Random Field (CRF) model | https://github.com/scrapinghub/python-crfsuite |
| Rapidfuzz | Fuzzy matching to find known items from a whitelist in unseen text | https://github.com/maxbachmann/RapidFuzz |
| Graphviz | Visualization of the dependency structure of parsed sentences | https://graphviz.org/ |
| Wordcloud | Visualization of final output | https://amueller.github.io/word_cloud/ |
 



### Reddit API Setup
We have created a user specifically for this project that is usable by others, but to avoid overlapping result sets you will probably want to set up your own Reddit account and register your own app. This can be done here:
[Reddit API Access](https://www.reddit.com/wiki/api) 

Once you have your Reddit credentials you can replace ours with yours in the file `config.py`

# Pipeline Flow
The tool runs by completing 5 consecutive steps as seen in this flowchart:
![Flow Summary Doc](https://github.com/legolego/MADS_698_Capstone/blob/main/assets/readme_flowchart.png?raw=true) 

For simplicity, the code is labeled with the step name:
- `Step1_Find_Category_From_Thing.ipynb`
- `Step2_Find_Subreddits.ipynb`
- `Step3_Find_Influencers.ipynb`
- `Step4_Find_Influencer_Relevant_Posts.ipynb`
- `Step5_CRF_Find_New_Terms.ipynb`

## Running the Next Big Thing
There are several ways you can run the tool:

#### Single Function Execution
A notebook with a single function has been created to run the full pipeline with a set of predefined parameters. Here are the required steps:
1. Open `FUNCTION_NBT_Pipeline.ipynb` 
2. Go to the "Call Next Big Thing Function" section
3. Replace the existing item, Covid-19, with the item you are interested in
4. Run the notebook 

Note that a full run on the Next Big Thing usually takes between 2 and 3 hours to complete.

#### Step-By-Step Execution
We also have a notebook that runs the code in a more modular fashion, allowing you to execute the 5 steps of the process separately. This version also allows you to change parameter values if you wish. Here are the required steps:
1. Open `NBT_Pipeline.ipynb` 
2. Go to the "Set Parameter Values" section and edit any parameter values that you would like to change. All parameters have comments describing what they are used for
3. Go to the "What are we finding the Next Big Thing of?" secton and set the variable `term` to the item you are interested in
4. Run the notebook step by step, or all at once
 


# Explain the MVP Flag
# Explain the Streamlit code
# link to the Streamlit app/blog
# Discuss output










