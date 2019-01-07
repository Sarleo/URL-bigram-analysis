# URL-bigram-analysis
Carry out URL parsing and scoring with frequency and site domain to find the top bi gram relationships

Pre Processing:

●	The words are broken down based on their delimiters and the words belonging to a single url or a single sentence are taken as a part of a String. 
●	Words are also broken down based on tokenisation and lemmatisation so that words of the same root form such as play, playing, played, etc. all are counted as a single entry i.e. play.
●	Stopwords such as is,are,may,has, etc are all removed using nltk.stopwords()
●	In case of URLs, the words are considered after the main site domain  and site domains are considered separately.
●	The code may break in case of smileys and other complicated characters, changing the encoding will help in that case. I have kept the general encoding here to fit all the general urls and comments
●	Words less than 2 letters and greater than 10 letters are filtered out 

1.	Comments

Input : a csv file of the following format:
 

The name of header is not important here. But do keep a header.

Output: a csv file of the following format:

 

Scoring: Scores are based on the occurence of two words in the same sentence

2. URL bigram:

Input: Input needs to be in the form of a csv containing URL along with a KPI.
 

The names of headers are not important. But please keep the header and the above format. 

Output:
There will be 2 outputs. 
One will have the top pairs along with their scores. Two scores are calculated. One id based on frequency of occurence and other is based on the sum of KPIs. The last column gives the most associated site domain for the pair based on the number of times the pair is associated with the site domain(frequency of occurence).

 

Second Output has the same parameters with the only difference being the that instead of the associated site domains, it gives the breakdown of various site domains associated based on frequency


 


Scope for Improvement: Sometimes you may need to filter out adsafe feed url from the associated site domain columns
