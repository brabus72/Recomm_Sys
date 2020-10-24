#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def prefilter_items(data, take_n_popular, item_mean_cost):
    """Предфильтрация товаров"""  
     
    popularity = data.groupby('item_id')['quantity'].sum().reset_index()
    popularity.sort_values('quantity', ascending=False, inplace=True)
    top_popular = popularity.head(40).item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    print(data['item_id'].nunique())
    

    top_notpopular = popularity.loc[popularity['quantity'] < 10].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    print(data['item_id'].nunique())
    
    
    data = data[data['sales_value'] / data['quantity'] > 0.5]
    print(data['item_id'].nunique())
    
    
    data = data[data['sales_value'] / data['quantity'] < 35]
    print(data['item_id'].nunique())

    # Уберем товары дешевле 1 доллара
    data = data[data['sales_value'] > 1]


    purchases_last_week = data.groupby('item_id')['week_no'].max().reset_index()
    weeks = purchases_last_week[purchases_last_week['week_no'] > data['week_no'].max() - 4].item_id.tolist()
    data = data[data['item_id'].isin(weeks)]
    print(data['item_id'].nunique())

    return data, top_popular



def postfilter_items(user, data, data_t, item_features, col, N, item_mean_cost, all_rec, top, userid, id_to_itemid, popular_exp_item):
    '''Условия фильтрации списка рекомендаций
    - 2 новых товара (юзер никогда не покупал)
    - 1 дорогой товар > 7 долларов (price = sum(sales_value) / sum(quantity))
    - Все товары из разных категорий (категория - sub_commodity_desc)'''
    
    bought_list = data.loc[data['user_id']==user, 'actual'].values[0]
    recommendations = data.loc[data['user_id']==user, col].values[0]
    exp_item = item_mean_cost.loc[item_mean_cost['mean_price'] > 7,'item_id'].values
    
    if user in userid:
        all_rec = all_rec[userid[user]]
    else:
        all_rec = []
        
    # Создадим разные категории
    CATEGORY_NAME = 'sub_commodity_desc'
    categories_used = []
    categories_diff = []
    
    exp_product = []
    new_product = []

    rec_unique = []
    
    # Условия для уникальности рекомендаций
    for i in range(len(recommendations)):
        item = recommendations[i]
        if item not in rec_unique:
            rec_unique.append(item)
            
    for i in range(len(all_rec)):
        if (i < len(all_rec)):
            item = id_to_itemid[all_rec[i]]
            if (item not in rec_unique):
                rec_unique.append(item)

    if len(rec_unique) == 0:
        return []
    

    # 1 дорогой товар > 7 долларов
    i = 0
    for item in rec_unique:
        if item in exp_item:
            exp_product.append(item)
            category = item_features.loc[item_features['item_id'] == item, CATEGORY_NAME].values[0]
            categories_used.append(category)
            rec_unique.remove(item)
            break

    if len(exp_product) == 0:
        exp_product.append(popular_exp_item)
        category = item_features.loc[item_features['item_id'] == popular_exp_item, CATEGORY_NAME].values[0]
        categories_used.append(category)

        
    # 2 новых товара (юзер никогда не покупал)
    i = 0
    for item in rec_unique:
        category = item_features.loc[item_features['item_id'] == item, CATEGORY_NAME].values[0]
        if (not item in bought_list) & (category not in categories_used):
            new_product.append(item)
            categories_used.append(category)
            rec_unique.remove(item)                                          
        if len(new_product) == 2:
            break       
            
    if len(new_product) < 2:
        for item in top:
            category = item_features.loc[item_features['item_id'] == item, CATEGORY_NAME].values[0]
            if (not item in bought_list) & (category not in categories_used):
                new_product.append(item)        
            if len(new_product) == 2:
                break          
                   
    for item in rec_unique:
        category = item_features.loc[item_features['item_id'] == item, CATEGORY_NAME].values[0]
        if category not in categories_used:
            categories_diff.append(item)
        rec_unique.remove(item)
        categories_used.append(category)
        
        
    final_recommendations = categories_diff[:2] + new_product[:2] + exp_product[:1]
    if len(exp_product) < 1:
        print('0 of exp_product', user)
    if len(new_product) < 2:
        print('0 of new_product', user)
    return final_recommendations

