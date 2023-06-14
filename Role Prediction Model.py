import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
#import warnings
#warnings.filterwarnings('ignore')
import re     #Regex - To clean data by substitution of symbols
import nltk
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('./UpdatedResumeDataSet.csv')

#Pre-processing

#Cleaning resume content
def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) # remove anything that is not within the ASCII range
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText
df['Cleaned'] = df['Resume'].apply(lambda x:cleanResume(x))

# Encode Category
label = LabelEncoder()
df['Encoded_Category'] = label.fit_transform(df['Category'])
df.head()

# Vectorizing the cleaned columns. 
# TfidfVectorizer --> Term Frequency Inverse Document Frequency 
# Inverse Document Frequency --> Finds rare words and assigns a special number to it.
text = df['Cleaned'].values
y = df['Encoded_Category'].values
word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english',
    max_features=1500)
word_vectorizer.fit(text)
X = word_vectorizer.transform(text)

# Train Test Data and Modeling

# Separate train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=24, test_size=0.2)

# Model Training
model = OneVsRestClassifier(KNeighborsClassifier())
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

'''print(f'---------------------------------\n| Training Accuracy   :- {(model.score(X_train, y_train)*100).round(2)}% |')
print(f'---------------------------------\n| Validation Accuracy :- {(model.score(X_test, y_test)*100).round(2)}% |\n---------------------------------')'''

#----------------------------------------------------------------------------------------------------------#


#Function to predict role(category) when a new resume is given
def predict_category(cleaned_resume_text):
    print(model.predict(cleaned_resume_text))


