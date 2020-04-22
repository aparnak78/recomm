#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
df=pd.read_csv('studentInfo.csv')
df.head()


# In[3]:


import matplotlib.pyplot as plt
import os
import warnings

from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model

warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size=0.2, random_state=42)


# In[5]:


train.head()


# In[6]:


test.head()


# In[7]:


n_users=len(df.id_student.unique())
n_users


# In[8]:


n_courses=len(df.course_id.unique())


# In[9]:


n_courses


# In[78]:


# creating course embedding path
course_input = Input(shape=[1], name="Course-Input")
course_embedding = Embedding(1133, 5, name="Course-Embedding")(course_input)
course_vec = Flatten(name="Flatten-Courses")(course_embedding)

# creating user embedding path
user_input = Input(shape=[1], name="User-Input")
user_embedding = Embedding(10000000, 5, name="User-Embedding")(user_input)
user_vec = Flatten(name="Flatten-Users")(user_embedding)


# concatenate features
conc = Concatenate()([course_vec, user_vec])

# add fully-connected-layers
fc1 = Dense(32, activation='sigmoid')(conc)
fc2 = Dense(32, activation='sigmoid')(fc1)
out = Dense(1)(fc2)

# Create model and compile it
model2 = Model( [user_input,course_input], out)
model2.compile('adam', 'mean_squared_error')


# In[79]:


from keras.models import load_model

if os.path.exists('regression_model8.h5'):
    model2 = load_model('regression_model8.h5')
else:
    history = model2.fit([train.id_student,train.course_id], train.final_result, epochs=5, verbose=1)
    model2.save('regression_model8.h5')
    plt.plot(history.history['loss'])
    plt.xlabel("Epochs")
    plt.ylabel("Training Error")


# In[80]:


model2.evaluate([test.id_student, test.course_id], test.final_result)


# In[81]:


predictions = model2.predict([test.id_student.head(10), test.course_id.head(10)])

[print(predictions[i], test.final_result.iloc[i]) for i in range(0,10)]


# In[82]:



# Creating dataset for making recommendations for the first user
course_data = np.array(list(set(df.course_id)))
course_data[:5]


# In[86]:


user = np.array([62122 for i in range(len(course_data))])
user[:5]


# In[87]:


predictions = model2.predict([user, course_data])
[print(predictions[i]) for i in range(0,22)]
predictions = np.array([a[0] for a in predictions])
#[print(predictions[i]) for i in range(0,)]

recommended_course_ids = (-predictions).argsort()[:5]
print("Output recommended courses : ", course_data[recommended_course_ids]) 

recommended_course_ids


# In[66]:


# print predicted scores
print(predictions[recommended_course_ids])


# In[ ]:




