import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

mdl_rf = jb.load('random_forest_20200422.pkl.z')
mdl_lgbm = jb.load('lgbm_20200422.pkl.z')
title_vec = jb.load('title_vectorizer_20200422.pkl.z')

def compute_prediction(data):
    feature_array = compute_features(data)
    
    if feature_array is None:
        return 0
    
    p_rf= mdl_rf.predict_proba(feature_array)[0][1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[0][1]
    
    p = 0.3*p_rf + 0.7*p_lgbm
    
    return p

def compute_features(data):
    if 'watch-view-count' not in data:
        return None
    
    publish_date = clean_date(data['watch-time-text'])
    if publish_date is None:
        return None
    
    views = clean_views(data['watch-view-count'])
    title = data['watch-title']
    
    features = dict()
    
    features['time_since_published'] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
    features['views'] = views
    features['views_per_day'] = features['views'] /features['time_since_published']
    del features['time_since_published']
    
    vectorized_title = title_vec.transform([title])
    
    num_features = csr_matrix(np.array([features['views'], features['views_per_day']]))
    feature_array = hstack([num_features, vectorized_title])
    
    return feature_array

def clean_date(date):
    raw_date_str = re.search(r'([A-z]{3}) (\d+), (\d+)', date) 
    if raw_date_str is None:
        return None
    
    raw_date_str_list = list(raw_date_str.groups())
    if len(raw_date_str_list[1]) == 1:
        raw_date_str_list[1] = '0' + raw_date_str_list[1]
        
    clean_date_str = ' '.join(raw_date_str_list)
    
    return pd.to_datetime(clean_date_str, format='%b %d %Y')

def clean_views(views):
    raw_views_str = re.search(r'(\d+,?\d*,?\d*)', views)
    if raw_views_str is None:
        return 0
    
    raw_views_str = raw_views_str.group().replace(',', '')
    
    return int(raw_views_str)

    