#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
courses=pd.read_csv("./course.csv")


# In[2]:


courses


# In[3]:


courses.head()


# In[4]:


get_ipython().run_line_magic('pip', 'install scikit-learn')


# In[5]:


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,3))

tfidf = vectorizer.fit_transform(courses["skill"])


# In[6]:


courses.head()


# In[7]:


get_ipython().system('pip install numpy')


# In[8]:


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(skill):
    skill = skill
    query_vec = vectorizer.transform([skill])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argmax(similarity)
    results = courses.iloc[index]
    
    return results


# In[9]:


pip install ipywidgets


# In[10]:


pip install IPython


# In[11]:


import ipywidgets as widgets
from IPython.display import display

skill_input = widgets.Text(
    #value = 'Git',
    placeholder = 'Enter skill :',
    description = 'Skill:',
    disabled = False
)

courses_list = widgets.Output()

def on_type(data):
    with courses_list:
        courses_list.clear_output()
        skill = data["new"]
        if len(skill) > 0:
            display(search(skill))

skill_input.observe(on_type, names='value')


display(skill_input, courses_list)


# In[29]:


def recommendation(skill):
    recommendation = courses[courses["skill"] == skill]["recommendation"].values
    if len(recommendation) > 0:
        return recommendation
    else:
        return None


# In[19]:


#def extract_recommendation(output):
   # recommendation = None
    #for widget in output.children:
       # if isinstance(widget, widgets.Output):
       #     for item in widget.outputs:
       #         if item.output_type == "stream" and item.text.startswith("Recommendation:"):
       #             recommendation = item.text.split("Recommendation:")[1].strip()
    #return recommendation


# In[ ]:





# In[ ]:




