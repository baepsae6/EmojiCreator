#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[12]:


import numpy as np
import emoji
import re
import encoder
from scipy import spatial
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')


# In[16]:





# In[17]:


class Emoji(object):
    def __init__(self):
        self.encoder = encoder.Encoder()
        self.emoji_dict = emoji.unicode_codes.EMOJI_ALIAS_UNICODE
        self.stopwords = stopwords.words('english')
        self.stopwords.extend(['I','You', 'you', 'me'])
        self.vectors_encoded = self.emoji_encoded()
        
    def sentence_preprocessed(self, sentence):
        tokenized_sentence = nltk.word_tokenize(sentence)
        sentence = [w for w in tokenized_sentence if not w in self.stopwords]
        return sentence
    
    def emoji_encoded(self):
        emoji_list = list(self.emoji_dict.keys())
        emoji_list = [re.sub("[: ()]", "", i) for i in emoji_list]
        emoji_list = [re.sub("[_ , ]", " ", i) for i in emoji_list]
        list_encoded_emoji = [self.encoder.encode(i)[0] for i in emoji_list]
        list_encoded_emoji = np.stack(list_encoded_emoji)
        
        return list_encoded_emoji
    
    def cosine_similarity_emoji(self, sentence, emoji):

        output_similarity = self.encoder.cosine_similarity(self.encoder.encode(sentence),emoji)
        if np.min(output_similarity[1]) < 0.3:
            emoji_index = np.argmin(output_similarity[1])
            output = list(self.emoji_dict.values())[emoji_index]
            return output
        else:
            return None
    
    def output_emoji(self, sentence):
        sentence_preprocessed = self.sentence_preprocessed(sentence)
        output = self.cosine_similarity_emoji(sentence_preprocessed, self.vectors_encoded)
        return output


# In[18]:


emoji = Emoji(encoder)


# In[22]:


emoji.output_emoji('I love stars')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




