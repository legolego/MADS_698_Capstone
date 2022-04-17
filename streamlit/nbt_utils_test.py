import numpy as np
import pickle
import pandas as pd
import datetime as dt
import os
from pathlib import Path
import re
import requests
import time
from collections import Counter


def get_mvp_terms():
    file_path = Path(__file__).parents[1] / 'output_step5/'
    file_list = os.listdir(file_path)
    term_list = []
    for f in file_list:
        if f.startswith("crf_results_"):
            term_list.append(f.rstrip(".csv").lstrip("crf_results_").replace("_"," "))
    return pd.Series(term_list)
