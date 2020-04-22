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
n_courses


# In[9]:


from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import LSTM

# creating user embedding path
user_input = Input(shape=[1], name="User-Input")

model = Sequential()
model.add(Embedding(1133,output_dim=5))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])


# In[11]:


from keras.models import load_model

if os.path.exists('lstm_model4.h5'):
    model = load_model('lstm_model4.h5')
else:
    history = model.fit(train.course_id, train.final_result, batch_size=16, epochs=5)
    model.save('lstm_model3.h5')
    plt.plot(history.history['loss'])
    plt.xlabel("Epochs")
    plt.ylabel("Training Error")


# In[12]:


model.evaluate([test.id_student], test.final_result,batch_size=16)


# In[13]:


predictions = model.predict([test.course_id.head(10)])

[print(predictions[i], test.final_result.iloc[i]) for i in range(0,10)]


# In[14]:



# Creating dataset for making recommendations for the first user
course_data = np.array(list(set(df.course_id)))
course_data[:5]


# In[15]:


course = np.array([1114 for i in range(len(course_data))])
course[:5]


# In[16]:


predictions = model2.predict([course, course_data])
[print(predictions[i]) for i in range(0,22)]
predictions = np.array([a[0] for a in predictions])
#[print(predictions[i]) for i in range(0,)]

recommended_course_ids = (-predictions).argsort()[:5]
print("Output recommended courses : ", course_data[recommended_course_ids]) 

recommended_course_ids


# In[ ]:




