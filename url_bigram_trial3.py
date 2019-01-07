# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 17:43:24 2018

@author: saranshmohanty
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:59:40 2018

@author: saranshmohanty
"""

import pandas as pd
import re
import glob
import os 
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
import numpy as np
from nltk.stem.snowball import  SnowballStemmer
import nltk
import csv
from nltk.tokenize import RegexpTokenizer
from string import digits
import operator
#import operator.itemgetter
'''
Array lookup
A_temp- first row of the raw data
A - URL Split + Lemmetizer
B - numbers removed
C - punctuations removed
user_count- second row of the raw data
'''


nltk.download('stopwords')
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('wordnet')
stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()

####################################change directory###########################
os.chdir('C:/Users/saranshmohanty/Desktop/misc csv 23 oct')
count=0
A=[]
A_temp=[]
user_count=[]

#############################change file name#############################
with open('Saransh_Auto_Test.csv','r') as csvfile:
    sv_reader = csv.reader(csvfile, delimiter=',')
    for row in sv_reader:
        A_temp.append(str(row[0]))
        user_count.append(row[1])
user_count[0]=0
#removes delimiters and then form a sentence

#########################################################find url function###########################3
def find_sd(raw_url):
    i=raw_url
    slash=[]
    dots=[]
    for j in range(0,len(i)):
        if i[j]=='/':
           
            slash.append(j)
        if i[j]=='.':
            dots.append(j)
    if len(slash)> 2:
        sdd=i[dots[0]:slash[2]]
    return sdd
#############################################end#######################################################
postsd="1"
A_temp1=[]
########################words after site domain##############################
for i in A_temp:
    slash=[]
    for j in range(0,len(i)):
        if i[j]=='/':
            slash.append(j)
    if len(slash)> 2:
            #sd=i[dots[0]:slash[2]]
        postsd=i[slash[2]:]
            #print(postsd)
    A_temp1.append(postsd)

A=[]
for i in A_temp1:
    b=re.split('; |, |\*|\n |/|-|@|:',i)
    c=' '.join(word for word in b)
    A.append(c)
#print("!")

B=[]
stop = list(stopwords.words('english'))

my_dict={}
word_freq={}
for i in A:
    j=word_tokenize(i)
    #print(len(j))
    #print(j[0])
    k=" "
    for l in j:
        remove_digits = str.maketrans('', '', digits)
        res = l.translate(remove_digits)
        m=lemmatiser.lemmatize(res)
        if m not in stop:
            #print(m)
            k+=" "
            k+=m
            k=k.lower()
    B.append(k)
    
C=[]
for i in B:
    tokenizer = RegexpTokenizer(r'\w+')
    #removes the punctuations
    alpha=tokenizer.tokenize(i)
    if alpha in ['http','com','www','org','in','co','https','true','undefined','c','d'] and len(alpha)>1:
        print("http found")
    else:
        C.append(alpha)
        

from collections import defaultdict  # available in Python 2.5 and newer
urls_d = defaultdict(int)

condition=['adsafe','htt','adsaf','adsa','bidurl','adsafe_','adsafe_u','adsafe_ur','.co','','.com','http','com','www','org','in','co','https','true','false','http','com','www','org','in','co','https','FALSE','TRUE','@']
sd_list=[]


###if you wish to filter out any phrase, add it to the condition array above##############

#################scoring stuff#############################
for alpha in range(len(C)):
    sd_score={}
    i=C[alpha]
    j=0
    k=0
    for beta in sd_list:
        if beta in A_temp[alpha]:
            if beta in sd_score.keys():
                sd_score[beta]+=1
            if beta not in sd_score.keys():
                sd_score[beta]=1
    for j in range(0,len(i)):
        for k in range(j,len(i)):
            a=min([i[j],i[k]])
            #print(j)
            b=max([i[j],i[k]])
            #print(k)
            if(a,b) in my_dict and a!=b and a not in condition and b not in condition and len(a)>1 and len(b)>1 and len(a)<10 and len(b)<10:
                my_dict[(a,b)]+=0
                word_freq[(a,b)]+=1
            if(a,b) not in my_dict and a!=b and a not in condition and b not in condition and len(a)>1 and len(b)>1 and len(a)<10 and len(b)<10:
                my_dict[(a,b)]=0
                word_freq[(a,b)]=1
                

final_tupple=[]          
for keys in my_dict.keys():
    sd_score={}
    try:
        x,y=keys
        ind=[]
        ind_count=0
        freq_count=0
        for i in range(0,len(A_temp)):
            if x in A_temp[i] and y in A_temp[i]:
                sd_temp=find_sd(A_temp[i])
                if sd_temp in sd_score and sd_temp not in condition:
                    
                    sd_score[sd_temp]+=int(user_count[i])+1
                if sd_temp not in sd_score and sd_temp not in condition:
                    sd_score[sd_temp]=int(user_count[i])+1
                if sd_temp in condition:
                    sd_score[sd_temp]=-1000
                max_sd=max(sd_score.items(), key=operator.itemgetter(1))[0]
                
                ind.append(i)
              
        for i in ind:
            ind_count+=int(user_count[i])
            freq_count+=1
        my_dict[(x,y)]+=ind_count
        if x==y or x in condition or y in condition or len(x)<=2 or len(x)>=10 or len(y)<=2 or len(y)>=10 :
            my_dict[(x,y)]-=1000
        final_tupple.append((x,y,my_dict[(x,y)],word_freq[(x,y)],max_sd))
    except:
        continue

       
temp2=[]
for i in final_tupple:
    x,y,a,b,c=i
    if x not in condition and y not in condition and a>=0 :
        temp2.append((x,y,a,b,c))
    else:
        continue
    
###################################check if something is present in condition###########
'''
for i in temp2:
    x,y,c,d,e=i
    if x in condition:
        print(x)
    if y in condition:
        print(y)
'''
temp1=[]
temp1=pd.DataFrame(list(temp2))
temp1.columns=['word1','word2','KPI','freq count','associated sd']
temp=[]
temp=temp1.sort_values(by=['KPI'],ascending=False)
temp.to_csv('word_assoc.csv',index=False)



###############################################################second dataset########################################
########################sd breakup###############################
sd_freq={}

tupple_cat=[]
for i in final_tupple:
    a,b,c,d,e=i
    if int(c)>0:
        tupple_cat.append((a,b,c,d))
sd_list=[]
temp=[]
for k in A_temp:
    #print(str(k))
    beta=str(k)
    #temp.append(str(k))
    i=k
    slash=[]
    dots=[]
    sdd=""
    for j in range(0,len(i)):
        if i[j]=='/':
           slash.append(j)
        if i[j]=='.':
            dots.append(j)
    if len(slash)> 2:
        sdd=i[dots[0]:slash[2]]
        #print("HI")
    #sdd=""
    #sdd=find_sd(str(k))
    if sdd not in sd_list and sdd not in condition:
        sd_list.append(sdd)


break_sd=[]
for i in tupple_cat:
    a,b,c,d=i
    sd_freq={}
    for j in sd_list:
        #print(j)
        for gamma in range(len(A_temp)):
            #aa=a_temp.replace(str(j),"")
            #print(aa)
            if str(a) in C[gamma] and str(b) in C[gamma] and j in A_temp[gamma]:
                if j in sd_freq.keys():
                    sd_freq[j]+=1
                else:
                    sd_freq[j]=1
                #print("true")
    for k in sd_freq.keys():
        #print(sd_freq[k])
        if c>0 and str(k) not in condition:
            break_sd.append((a,b,c,d,k,sd_freq[k]))
        sd_freq[k]=0

##############################dataframe 2#################################################
final_panda=[]
final_panda=pd.DataFrame(list(break_sd))
final_panda2=[]
final_panda3=[]
for i in break_sd:
    a,b,c,d,e,f=i
    if c>0:
        final_panda3.append(i)
final_panda2=pd.DataFrame(list(final_panda3))
final_panda2.columns=['word1','word2','KPI sum','total_freq','urls','frequency_sd']
final_panda4=[]
final_panda4=final_panda2.sort_values(by=['KPI sum'],ascending=False)
final_panda4.to_csv('url_breakdown.csv',index=False)
        
#############################################end of code########################################33
    
    

