#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np


def recall_at_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    recommended_list = recommended_list[:k]
    
    flags = np.isin(bought_list, recommended_list)
    recall = flags.sum() / len(bought_list)
    
    return recall


def precision_at_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    
    bought_list = bought_list  # Тут нет [:k] !!
    recommended_list = recommended_list[:k]
    
    flags = np.isin(bought_list, recommended_list)
    precision = flags.sum() / len(recommended_list)
    
    return precision


def money_precision_at_k(recommended_list, bought_list, prices_recommended, k=5):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    prices_recommended = np.array(prices_recommended)

    if k < len(recommended_list):
        recommended_list = recommended_list[:k]
        prices_recommended = prices_recommended[:k]

    flags = np.isin(recommended_list, bought_list)
    res = np.dot(flags, prices_recommended) / np.sum(prices_recommended)

    return res

