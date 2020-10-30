import nltk
from nltk.corpus import stopwords 
from simhash import Simhash
#nltk.download('stopwords')
str1 = "a dog aren't watching stupid kids. life is tuff. $$$ quotes from my mother's home"
str2 = "a dog aren't watching stupid kids. life is tuff. $$$ quotes from my mother's"

words = nltk.word_tokenize(str1)
new_words= [word for word in words if word.isalnum()]
#print(words)
print(Simhash(str1).value)
print(Simhash(str2).value)
