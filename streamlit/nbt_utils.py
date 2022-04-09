import graphviz

import wikipedia # used for search of terms, provides: DisambiguationError

import wikipediaapi # used because can get categorymembers in a given category
wiki_wiki = wikipediaapi.Wikipedia('en')

# Might be able to use pywikibot for everything, or at least more
# https://stackoverflow.com/questions/71023854/how-to-find-subcategories-and-subpages-on-wikipedia-using-pywikibot
import pywikibot as pw # used to get AND filter hidden categories for an article


import stanza
stanza.download('en') # download English model

nlp = stanza.Pipeline(lang='en', processors='tokenize,lemma,pos,depparse')

# https://www.sbert.net/docs/pretrained_models.html
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L12-v2')

import numpy as np
import pickle

import datetime as dt

import re
import requests
import time
from collections import Counter





def get_stanza_dict_of_first_sentence(wiki_summary_text):
    # Using stanza instead of nltk to save memory
    doc = nlp(wiki_summary_text)
    return doc.sentences[0].to_dict()


def graph_sent(sent_dict):    
    id_word = {}
    root_id = 0
    for word in sent_dict:
        if word['upos'] != 'PUNCT':
            if word['head'] == 0:
                root_id = str(word['id']) 
            id_word[str(word['id'])] = str(word['id']) + ':' + word['text']

    # Create Digraph object
    sent_tree = graphviz.Digraph()

    # Add just the nodes from first traversal of dict
    for k, v in id_word.items(): 
        # Add nodes
        # https://graphviz.org/doc/info/shapes.html
        if k == root_id:
            sent_tree.node(k, v, shape='star')    
        else:
            sent_tree.node(k, v, shape='egg')


    # Traverse dict again to add all the relationships
    for word in sent_dict:
        if (word['upos'] != 'PUNCT') & (str(word['head']) != '0'):        
            sent_tree.edge(str(word['id']), str(word['head']), label=word['deprel'])

    # Visualize the graph
    return sent_tree

def get_wikipedia_search_results(search_term):
    search_results = wikipedia.search(search_term)[:7]

    clean_results = []
    for term in search_results:
        try:
            page = wikipedia.page(term, auto_suggest=False) 
            clean_results.append(term)
        except wikipedia.DisambiguationError:
            pass
    return clean_results

def get_categories_from_wiki_article(article):
    # use pywikibot because it can filter hidden 'meta' categories that aren't needed
    # https://stackoverflow.com/questions/54526821/how-to-identify-wikipedia-categories-in-python
    site = pw.Site("en", "wikipedia")
    non_hidden = [
        cat.title()[:]
        for cat in pw.Page(site, article).categories()
        if 'hidden' not in cat.categoryinfo
    ]
    
    return(non_hidden)

get_categories_from_wiki_article('Cryptocurrency')

def get_best_categories_for_term(wiki_term, wiki_cats, nlp_cat_phrase):
    # remove parens and anyting inside them
    wiki_term = re.sub(r'\([^)]*\)', '', wiki_term)
    print('wiki_cats:', wiki_cats)
    print('')

    # https://stackoverflow.com/questions/65199011/is-there-a-way-to-check-similarity-between-two-full-sentences-in-python
    rem_term_cats = [' '.join([wiki_term])] + wiki_cats
    rem_first = model.encode(rem_term_cats)

    print("Remove wiki-cats too close to actual term(first term)")
    print(rem_term_cats)
    cos_remove = util.pytorch_cos_sim(rem_first, rem_first)[0].numpy()
    print(cos_remove)
    rem_idx = np.where(cos_remove > .7)[0]
    #because first item is our search term here, but we need to remove items from wiki_cats, so subtract 1
    rem_idx_from_wiki_cats = rem_idx[1:]-1
    print(rem_idx_from_wiki_cats)
    wiki_cats = [j for i, j in enumerate(wiki_cats) if i not in rem_idx_from_wiki_cats]
    print('after rem:', wiki_cats)


    keep_cat_cats = [' '.join(nlp_cat_phrase)] + wiki_cats
    keep_first = model.encode(keep_cat_cats)

    print("Keep wiki-cats not too far to found category(first term)")
    print(keep_cat_cats)
    keep_cos = util.pytorch_cos_sim(keep_first, keep_first)[0].numpy()
    print(keep_cos)
    keep_idx = np.where(keep_cos > .7)[0]

    keep_idx_from_wiki_cats = keep_idx[1:]-1

    print('keep idx:', keep_idx_from_wiki_cats)
    print('pre-last-filt:', wiki_cats)

    # if we got anything with a decent score, keep those, otherwise everything
    
    if len(keep_idx_from_wiki_cats) >= 2:
        wiki_cats = [j for i, j in enumerate(wiki_cats) if i in keep_idx_from_wiki_cats]
    else:
        # keep Top 5 categories iof filtering doesn't return much
        cats_cos = list(zip(keep_cat_cats, keep_cos))
        top_cats_cos = sorted(cats_cos, key=lambda x: x[1], reverse=True)[1:6]
        wiki_cats = [i[0] for i in top_cats_cos]



    print('post-last-filt:', wiki_cats)

    return wiki_cats
	
	
def get_first_unambiguous_wiki_term_and_page(search_term):
    search_results = wikipedia.search(search_term)

    first_wiki_term = search_results[0]    
    #https://github.com/goldsmith/Wikipedia/issues/295
    try:
        page = wikipedia.page(first_wiki_term, auto_suggest=False)    
    except wikipedia.DisambiguationError:
        print("Oops! DisambiguationError, trying next result")
        first_wiki_term = search_results[1]
        page = wikipedia.page(first_wiki_term, auto_suggest=False)

    print('first_wiki_term:', first_wiki_term)
    return first_wiki_term, page
	

	
def get_nlp_category_phrase(wiki_page):
    
    wiki_page_text = wiki_page.summary
    # # Using stanza instead of nltk to save memory
    # doc = nlp(wiki_page_text)
    # first_sentence = doc.sentences[0]
    # #first_sentence.text
    sent_dict = get_stanza_dict_of_first_sentence(wiki_page_text)

    # Look for the ROOT word of the dependency tree
    # hopefully not the first word
    root_id = 0
    root_word = ''
    for word in sent_dict:
        if word['head'] == 0:
            root_id = word['id']
            root_word = word['text']
            break    

    # print("first root id:", root_id)
    # print("first root word:", root_word)            

    # Lost TV series for some reason has ROOT as first word
    if root_id in [1]:
        for word in sent_dict:
            if (word['head'] == 1) & (word['deprel'] in ['nsubj:pass', 'parataxis']):
                root_id = word['id']                
                root_word = word['text']
                break

    # print("new root id:", root_id)
    # print("new root word:", root_word)

    # Get all modifiers of ROOT word, loop up to 3 times to get enough words
    all_dep_ids = []

    for i in range(3):  # at most 3 loops
        cur_dep_ids = []
        for word in sent_dict:
            if ((word['head'] in all_dep_ids + [root_id]) & (word['deprel'] in ['obl', 'compound','amod','nmod','conj','appos'])):
                cur_dep_ids.append(word['id'])

        all_dep_ids.extend(cur_dep_ids)
        #print(i, all_dep_ids)
        if len(all_dep_ids) > 2:    # bring back at least 4 words, if we have more, then they're too far away
            break
    #print(all_dep_ids)
    all_dep_ids.append(root_id)

    category_phrase_dict = dict()
    for word in sent_dict:
        if (word['id'] in all_dep_ids):
            category_phrase_dict[word['id']] = word['text']

    #print(category_phrase_dict)

    nlp_category_phrase = []
    for k,v in category_phrase_dict.items():
        nlp_category_phrase.append(v)
    #print('**', search_term, '**', first_wiki_term, '**', nlp_category_phrase)
    #print(wiki_page.categories)

    # print(nlp_category_phrase)
    index_root_word = nlp_category_phrase.index(root_word)
    
    # this was an attempt to cut off the phrases at the root word, but some continue past it, iPhone for example
    #nlp_category_phrase = nlp_category_phrase[:index_root_word+1]

    print('nlp phrase:', nlp_category_phrase)
    return nlp_category_phrase
	
def get_category_from_search_term(search_term):   
    
    first_wiki_term, wiki_page = get_first_unambiguous_wiki_term_and_page(search_term)

    nlp_category_phrase = get_nlp_category_phrase(wiki_page)

    raw_wiki_cats = get_categories_from_wiki_article(first_wiki_term)

    best_wiki_cats = get_best_categories_for_term(first_wiki_term, raw_wiki_cats, nlp_category_phrase)

    expanded_year_wiki_cats = get_all_combined_wiki_cats(best_wiki_cats)

    return nlp_category_phrase, expanded_year_wiki_cats, best_wiki_cats, first_wiki_term
	
def get_all_combined_wiki_cats(list_wiki_cats):
    combined_wiki_cats = list_wiki_cats
    for year_cats in expand_years_in_cats_to_modern(list_wiki_cats):
        combined_wiki_cats = list(set(combined_wiki_cats + year_cats))
    return combined_wiki_cats
    
    
def expand_years_in_cats_to_modern(list_wiki_cats):
    new_year_cats_to_add = []
    # SSLError: HTTPSConnectionPool(host='en.wikipedia.org', port=443)

    for cat in list_wiki_cats:    
        print("****", cat)
        try:
            new_year_cats_to_add.append(return_new_year_cats(cat))

        except requests.exceptions.SSLError:
            print("SSLError exception caught!!!!!!!!!!!!!!!")
            time.sleep(5)
            new_year_cats_to_add.append(return_new_year_cats(cat))   

    return new_year_cats_to_add

def return_new_year_cats(wiki_cat):
    year_pattern = re.compile('(19|20)\d{2}s?')
    check_for_year = re.search(year_pattern, wiki_cat)

    curr_year = dt.datetime.now().year

    new_cat_list = []

    if check_for_year != None:
        print('found', check_for_year.group(0), 'in category:', wiki_cat)        
        found_year = check_for_year.group(0)

        if 's' in found_year:
            new_category = wiki_cat.replace(found_year, '2020s')
            print(new_category)
            #check category exists
            pages_in_new_cat = len(get_wiki_wiki_pages_for_cat_members(new_category).categorymembers.keys())
            if pages_in_new_cat > 0:
                # add cat to existing list
                print(pages_in_new_cat, 'exists!')
                new_cat_list.append(new_category)
        else:
            for pot_year in [str(x) for x in [curr_year - i for i in range(5)]]:
                
                print(pot_year)
                new_category = wiki_cat.replace(found_year, pot_year)
                #check category exists
                pages_in_new_cat = len(get_wiki_wiki_pages_for_cat_members(new_category).categorymembers.keys())
                if pages_in_new_cat > 0:
                    # add cat to existing list
                    print(pages_in_new_cat, 'exists!')
                    new_cat_list.append(new_category)
                

    return new_cat_list

def get_wiki_wiki_pages_for_cat_members(category):
    wiki_cat = ''
    try:
        wiki_cat = wiki_wiki.page(category)        
    except requests.exceptions.SSLError:
        print("SSLError exception caught!!!!!!!!!!!!!!!")
        time.sleep(5)
        wiki_cat = wiki_wiki.page(category)
    return wiki_cat