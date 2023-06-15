import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

courses = pd.read_csv("course.csv")

vectorizer = TfidfVectorizer(ngram_range=(1, 3))

tfidf = vectorizer.fit_transform(courses["skill"])

def search(skill):
    skill = skill.lower()  # Convert skill to lowercase for case-insensitive matching
    query_vec = vectorizer.transform([skill])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argmax(similarity)
    results = courses.iloc[index]

    return results

def recommendation(skill):
    recommendation = courses[courses["skill"] == skill]["recommendation"].values
    if len(recommendation) > 0:
        return recommendation
    else:
        return None
    
# Sample list of skills
skills_list = ["Python", "Machine Learning", "Data Analysis"]

for skill in skills_list:
    print(f"Skill: {skill}")
    results = search(skill)
    print(results)
    recommendation_loop = recommendation(skill)
    if recommendation_loop:
        print(f"Recommendation: {recommendation_loop}\n")
    else:
        print("No recommendation found.\n")

