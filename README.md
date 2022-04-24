# Next Big Thing Capstone Project
![NBT Logo](https://github.com/legolego/MADS_698_Capstone/blob/main/assets/NextBigThingLogoDraft2.png?raw=true) 

Capstone project for University of Michigan's Master of Applied Data Science program created by Cody Crow, Kim Di Camillo and Oleg Nikolsky. Given a user-entered item, the tool mines Reddit data to identify what popular Redditors are currently discussing that are "like" the original item.

# Getting Started
### Clone the repo
Clone this repository to get started.
```
git clone https://github.com/legolego/MADS_698_Capstone.git
```

### Prereqs
Get all of the dependencies needed by running the following in the MADS_698_Capstone directory:
```
pip3 install -r requirements.txt
```
#### Installation Notes
Note that our tool was built using Python 3.7.

Depending on your version of Python, the installation of pickle5 may fail as it is already included in higher versions of Python. If this happens, just disregard the error message.

Additionally, the installation of wordcloud may require a wheel file that is specific to your operating system. You can go to this website to find the file location and run a pip3 install on the direct link: 
[Wordcloud Wheel Files](https://github.com/sulunemre/word_cloud/releases/tag/2)

### Tools
Our project uses the following tools. We have included some links to the documentation:


| Tool | Use | Link |
| ------ | ------ | ------ |
| Reddit | Main data source. APIs to access subreddit, submission, comment, and user data | https://praw.readthedocs.io/en/stable/ https://github.com/pushshift/api https://github.com/mattpodolak/pmaw#description |
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
We have created a user specifically for this project that is usable by others, but you will probably want to set up your own Reddit account and register your own app. This can be done here:

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

# Running the Next Big Thing
There are several ways you can run the tool:

### Single Function Execution
A notebook with a single function has been created to run the full pipeline with a set of predefined parameters. Here are the required steps:
1. Open `find_next_big_thing.ipynb` 
2. Go to the "Call Next Big Thing Function" section
3. Replace the existing item, 'Covid-19', with the item you are interested in
4. Run the notebook 

Note that a full run on the Next Big Thing usually takes between 2 and 3 hours to complete.

### Step-By-Step Execution
We also have a notebook that runs the code in a more modular fashion, allowing you to execute the 5 steps of the process separately. This version also allows you to change parameter values if you wish. Here are the required steps:
1. Open `NBT_Pipeline.ipynb` 
2. Go to the "Set Parameter Values" section and edit any parameter values that you would like to change. All parameters have comments describing what they are used for. Be sure to set the mvp_flag to False if you want to generate new results - see more details on this below
3. Go to the "What are we finding the Next Big Thing of?" section and set the variable `term` to the item you are interested in
4. Run the notebook step by step, or all at once
 
### Other Execution Notes
#### MVP Flag
The project is designed to create output pickle files after Steps 2, 3, 4, and 5 to allow for modular runs and quick viewing of results that were previously run. This is done through the use of the mvp_flag. In most of our functions this flag is an input parameter and indicates if a previously generated pickle file should be used instead of generating new results. The pickle files are named based on the `wiki_term` generated in Step 1. If the flag is set to True, the function will look for a pickle file for that step containing the `wiki_term`.

#### Workaround for Memory Issues
While testing the project we sometimes had trouble with the 5GB RAM limit on our free instance of Deepnote. The code would often have a memory issue while in Step 5. If this happens you can use the following workaround:
1. Open `NBT_Pipeline.ipynb`
2. Run the import statement in the "Standard Python Library Imports" section
3. Run the Step 5 import:
   ```
   import Step5_CRF_Find_New_Terms as crfnt
   ```
4. Edit the following line in the "Identify Next Big Thing" section:
   ```
   df_final = crfnt.calculate_final_results_for_wiki_term(wiki_term, mvp_flag)
   ```
   to read:
   ```
   df_final = crfnt.calculate_final_results_for_wiki_term('your wiki_term', False)
   ```
   You can find the value of `wiki_term` for your item in the last cell of the "Get initial Wikipedia data about our user entry" section.
   
5. Execute the cell block you just changed and the remaining cells in the notebook

# Next Big Thing Output
The output of the tool is a list of the top 10 items currently being discussed on Reddit that are siblings of your original item entered, along with the count of occurrences found by the Conditional Random Field (CRF) model we employed. The data is also presented in a word cloud shaped as Snoo, Reddit's alien mascot. In the Snoo word cloud, all items found as part of the CRF model are represented, with the size of the item indicating its frequency of occurrence.

# Streamlit Application
We published an application in Streamlit where you can see the results for pre-generated examples such as Squid Game, Dogecoin, Elon Musk and more. There is also a blog we wrote describing our project and results. You can check it out here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/legolego/mads_698_capstone/main/streamlit/next_big_thing.py)

