#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:34:54 2019

@author: mackenziemitchell
"""

# !pip install vaderSentiment
# !pip install spacy
import nltk
from nltk.corpus import stopwords
import pandas as pd
import pickle
import seaborn as sns
from nltk import FreqDist
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

def process_article(article):
    tokens = nltk.word_tokenize(article)
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stopwords_list]
    return (stopwords_removed)

stopwords_list = stopwords.words('english') + list(string.punctuation)
stopwords_list += ["''", '""', '...','.' ,'``','1','2','3','4','5','6'
                   ,'7','8','9',"'s","'",'’',"n't","'ve","'m"]

sp = spacy.load('en')

with open('pickles/df0.pickle', 'rb') as f:
    dfr = pickle.load(f)
    
corpus1=dfr['content']
corpus=nltk.Text(dfr['content'])

#Tokenizing and Removing Stop Words & Lemmatizing
#processed_data is a list of lists. each smaller list represents a tokenized
#review where stop words have been removed
processed_data = list(map(process_article, corpus))

#articles_contact is one list containing all words in the tokenized 
#corpus with stopwords removed, can be repeated, not all words unique
articles_concat = []
for article in processed_data:
    articles_concat += article
    
lemcontent=[]
for review,u in zip(processed_data,dfr['url']):
    words=[]
    sentence=sp(' '.join(review))
    for word in sentence:
        words.append(word.lemma_)
    if words not in lemcontent:
        lemcontent.append({'url':u,'processed_review':words})
        
lemmasdf=pd.DataFrame(lemcontent)

lemwords=[]
words=' '.join(articles_concat)
words=sp(words)
for word in words:
    lemwords.append(word.lemma_)
    
lemmas_freqdist = FreqDist(lemwords)
# lemmas_freqdist.most_common(200)

maximum_frequncy = max(lemmas_freqdist.values())
weightedic={}
for word in lemmas_freqdist.keys():
    weightedic[word] = (lemmas_freqdist[word]/maximum_frequncy)
#Sentence importance
sentence_scores = {}
for sent in list(dfr.content):
    for word in sent.split(' '):
        if word in weightedic.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = weightedic[word]
                else:
                    sentence_scores[sent] += weightedic[word]

sent_scores=[]
for s,u in zip(list(dfr.content),dfr.url):
    for sent,score in zip(sentence_scores.keys(),sentence_scores.values()):
        if sent==s:
            sent_scores.append({'url':u,'sentence':sent,'score':score})
sentscoredf=pd.DataFrame(sent_scores)

articles_freqdist = FreqDist(articles_concat)
# articles_freqdist.most_common(200)

#Getting Sentiment Scores

dfr.sort_values('url',inplace=True)
new=[]
for p,u,t,us in zip(processed_data,dfr.url,dfr.title,dfr.user):
    new.append({'url':u,'content':' '.join(p),'title':t,'user':us})
newdf=pd.DataFrame(new)
newdf.drop_duplicates(inplace=True)
len(newdf)
analyzer = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyzer.polarity_scores(sentence)
#     print("{:-<40} {}".format(sentence, str(score)))
    return score['pos']

sentiments=[]
for (ur,t,c,u) in zip(newdf.url,newdf.title,newdf.content,newdf.user):
    sentiments.append({'url':ur,'tsentiment':sentiment_analyzer_scores(t),'csentiment':sentiment_analyzer_scores(c),'user':u})
sentimentsdf=pd.DataFrame(sentiments)

sentimentsdf.sort_values('url',inplace=True)
sentimentsdf.drop_duplicates(inplace=True)

avg_sent_by_url=sentimentsdf.groupby('url').mean()
avg_sent_by_url.sort_values('url',inplace=True)
len(avg_sent_by_url)

avgsent,sent=[],[]
for (au,c,t) in zip(avg_sent_by_url.index,avg_sent_by_url['csentiment'],avg_sent_by_url['tsentiment']):
    for u,uu,tt,tc in zip(dfr.url,sentimentsdf.url,sentimentsdf.tsentiment,sentimentsdf.csentiment):
        if uu==au:
            avgsent.append({'url':au,'avg_content_sent':c,'avg_title_sent':t,'title_sentiment':tt,'content_sentiment':tc})
#     for u,c,t in zip(sentimentsdf.url,sentimentsdf.csentiment,sentimentsdf.tsentiment):
#         if u==au:
#             sent.append({'url':au,'title_sentiment':t,'content_sentiment':c})
avgsentdf=pd.DataFrame(avgsent)
sentiments=pd.DataFrame(sent)


dfr.groupby('user').mean()

need=pd.DataFrame(dfr.groupby('url')['rating'].mean())
need['rating_count']=pd.DataFrame(dfr.groupby('url')['rating'].count())
need.reset_index(inplace=True)
with open('pickles/forstreamlit.pickle', 'wb') as f:
    pickle.dump(need, f, pickle.HIGHEST_PROTOCOL)
    
ratings_mean_count=pd.DataFrame(dfr.groupby('prodName')['rating'].mean())
ratings_mean_count['rating_count']=pd.DataFrame(dfr.groupby('prodName')['rating'].count())
ratings_mean_count.sort_values(by='rating_count',ascending=False)

avgsentdf.drop_duplicates(inplace=True)
# avgsentdf.reset_index(inplace=True)
# avgsentdf.drop(columns=['content_sent','title_sent'],inplace=True)
avgsentdf

sns.distplot(ratings_mean_count['rating_count'])

sns.distplot(ratings_mean_count['rating'])

sns.jointplot(x='rating', y='rating_count', data=ratings_mean_count, alpha=0.4)

avgt=[]
avgc=[]
df1=dfr
for u in df1.url:
    for (ua,t,c) in zip(avgsentdf.url,avgsentdf.avg_title_sent,avgsentdf.avg_content_sent):
        if u==ua:
#             avgt.append({'url':u,'avg_title_sent':t,'avg_content_sent':c})
            avgt.append(t)
            avgc.append(c)
            
sentimentsdf.drop_duplicates(inplace=True)
df1=dfr
df1.drop_duplicates(inplace=True)
df1['average_content_sentiment']=avgc
df1['average_title_sentiment']=avgt
df1['content_sentiment']=list(sentimentsdf['csentiment'])
df1['title_sentiment']=list(sentimentsdf['tsentiment'])

df1.reset_index(inplace=True)
df1.drop(columns='index',inplace=True)


import seaborn as sns
plt.figure(figsize=(10,10))
sns.scatterplot(x='rating',y='content_sentiment',data=df1)
plt.savefig('Visuals/RatingContentSentimentPlot.png')

plt.figure(figsize=(10,10))
sns.scatterplot(x='rating',y='title_sentiment',data=df1)
plt.savefig('Visuals/RatingTitleSentimentPlot.png')


plt.figure(figsize=(10,10))
sns.scatterplot(x='rating',y='average_content_sentiment',data=df1)
plt.savefig('Visuals/RatingAvgContentSentimentPlot.png')

plt.figure(figsize=(10,10))
sns.scatterplot(x='rating',y='average_title_sentiment',data=df1)
plt.savefig('Visuals/RatingAvgTitleSentimentPlot.png')

#Word Clouds
def plot_wordcloud(wordcloud,title):
    plt.figure(figsize=(10,10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    plt.savefig('{}WordCloud.png'.format(title))
    
wordcloud = WordCloud().generate(str(corpus[7:]))
#Whole Corpus
plot_wordcloud(wordcloud,'WholeCorpus')
plt.savefig('WCWordCloud.png')
#Processed Corpus
lemwords=[]
words=' '.join(articles_concat)
words=sp(words)
for word in words:
    lemwords.append(word.lemma_)
al=' '.join(lemwords)
wordcloud = WordCloud().generate(al)
plot_wordcloud(wordcloud)
