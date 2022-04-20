# Next Big Thing Capstone project
Capstone project for University of Michigan's Master of Applied Data Science program by Cody Crow, Kim Di Camillo and Oleg Nikolsky. 
Given a specific item, the tool we built mines Reddit data to identify what popular Redditors are currently discussing that are "like" the original item.

# Getting Started
## Clone the repo
Clone this repository to get started.
```
git clone 
```

## Prereqs
Get all of the dependencies needed by running the following:
```
pip install -r streamlit/requirements.txt
```

## Reddit API Setup
We have created a user specifically for this project that is usable to others, but you will probably want to set up your own Reddit account and register your own app. 
This can be done here:
[Reddit API Access](https://www.reddit.com/wiki/api) 

Once you have your Reddit credential you can replace ours with yours in the file `config.py`

# Pipeline Flow
The tool runs by completing 5 consecutive steps as seen in this flowchart:

For simplicity, the code is labeled with the step name:
- `Step1_Find_Category_From_Thing.ipynb`
- `Step2_Find_Subreddits.ipynb`
- `Step3_Find_Influencers.ipynb`
- `Step4_Find_Influencer_Relevant_Posts.ipynb`
- `Step5_CRF_Find_New_Terms.ipynb`

## Running the Next Big Thing
There are several ways you can run the tool:

### Single Function Execution
A notebook with a single function has been created to run the full pipeline with a set of predefined parameters. 
Run this by performing the following steps:
1. Open `FUNCTION_NBT_Pipeline.ipynb' 
2. Go to the "Call Next Big Thing Function" section
3. Replace the existing item, Covid-19, with the item you are interested in
4. Run the notebook 
Note that a full run on the Next Big Thing usually takes between 2 and 3 hours to complete

### Step-By-Step Execution
We also have a notebook that runs the codes in a more modular fashion, allowing you to run through the 5 steps of the process. This version also allows you to change some of the parameters if you wish.
Run this by performing the following steps:
1. Open `NBT_Pipeline.ipynb' 
2. Go to the "Set Parameter Values" section
3. Edit any parameter values that you would like to change. All parameters have comments describing what they are for
 


#Explain the MVP Flag
#Explain the Streamlit code
#Discuss output
