import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ipywidgets as widgets
from IPython.display import display

courses=pd.read_csv("course.csv")

vectorizer = TfidfVectorizer(ngram_range=(1,3))

tfidf = vectorizer.fit_transform(courses["skill"])

def search(skill):
    skill = skill
    query_vec = vectorizer.transform([skill])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argmax(similarity)
    results = courses.iloc[index]
    
    return results

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

def recommendation(skill):
    recommendation = courses[courses["skill"] == skill]["recommendation"].values
    if len(recommendation) > 0:
        return recommendation
    else:
        return None
