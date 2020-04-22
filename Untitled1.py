#!/usr/bin/env python
# coding: utf-8

# In[55]:


import numpy as np
import pandas as pd
df=pd.read_csv('studentInfo2.csv')
df.head()


# In[57]:


import matplotlib.pyplot as plt
import seaborn as sns 
sns.set_style("white")
get_ipython().run_line_magic('matplotlib', 'inline')


# In[58]:


df.groupby('code_module')['final_result'].mean().head()


# In[59]:


df.groupby('code_module')['final_result'].count().sort_values(ascending=False).head()


# In[60]:


credits=pd.DataFrame(df.groupby('code_module')['final_result'].mean())
credits['number_of_students']=pd.DataFrame(df.groupby('code_module')['studied_credits'].count())
credits.head()


# In[62]:


def make_bar_chart(dataset, attribute, bar_color='#3498db', edge_color='#2980b9', title='Title', xlab='X', ylab='Y', sort_index=False):
    if sort_index == False:
        xs = dataset[attribute].value_counts().index
        ys = dataset[attribute].value_counts().values
    else:
        xs = dataset[attribute].value_counts().sort_index().index
        ys = dataset[attribute].value_counts().sort_index().values
        
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title, fontsize=24, pad=20)
    ax.set_xlabel(xlab, fontsize=16, labelpad=20)
    ax.set_ylabel(ylab, fontsize=16, labelpad=20)
    
    plt.bar(x=xs, height=ys, color=bar_color, edgecolor=edge_color, linewidth=2)
    plt.xticks(rotation=45)
    
    
make_bar_chart(df, 'code_module', title='number of students', xlab='Course', ylab='Counts')


# In[63]:


matrix = df.pivot_table(
    index='id_student',
    columns='code_module',
    values='final_result'
).fillna(0)
matrix.head()


# In[64]:


num_ratings = pd.DataFrame(df.groupby('code_module').count()['studied_credits']).reset_index()
df = pd.merge(left=df, right=num_ratings, on='code_module')
df.rename(columns={'studied_credits_x': 'studied_credits', 'studied_credits_y': 'numofstudents'}, inplace=True)


# In[65]:


df.sort_values(by='numofstudents', ascending=False)[:10]


# In[70]:


def get_similar_courses(course, n_ratings_filter=0, n_recommendations=5):
    similar = matrix.corrwith(matrix[course])
    corr_similar = pd.DataFrame(similar, columns=['correlation'])
    corr_similar.dropna(inplace=True)
    
    orig = df.copy()
    
    corr_with_movie = pd.merge(
        left=corr_similar, 
        right=orig, 
        on='code_module')[['code_module', 'correlation', 'numofstudents']].drop_duplicates().reset_index(drop=True)
    
    result = corr_with_movie[corr_with_movie['numofstudents'] > n_ratings_filter].sort_values(by='correlation', ascending=False)
    
    return result.head(n_recommendations)


# In[73]:


get_similar_courses('AAA2013J')


# In[ ]:




