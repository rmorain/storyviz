from __future__ import unicode_literals

"""
Performs keyword extraction on story.
Return list of strings.
Strings are associated keywords.
"""

# from rake_nltk import Rake
import spacy
from spacy import displacy
import unicodedata
from spacy.lang.en.stop_words import STOP_WORDS

spacy.prefer_gpu()

# class StoryInterpreterRake:
#     def __init__(self):
#         self.r = Rake()

#     def get_keywords(self, story):
#         print(story)
#         keywords_list = self.r.extract_keywords_from_text(story)

#         return self.r.get_ranked_phrases()

        
class StoryInterpreter:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def get_pps(self, doc):
        "Function to get PPs from a parsed document."
        pps = []
        for token in doc:
            # Try this with other parts of speech for different subtrees.
            if token.pos_ == 'ADP':
                pp = ' '.join([tok.orth_ for tok in token.subtree])
                pps.append(pp)
        return pps

    def remove_duplicates(self, keywords):
        for i, w in enumerate(keywords):
            for j, k in enumerate(keywords):
                if i != j and k in w:
                    print(k)
                    keywords.pop(j)

    def clean_keywords(self, keywords):
        clean_keys = []
        for i, k in enumerate(keywords):
            doc = self.nlp(k)
            for token in doc:
                if token.is_stop == True:
                    print(token)
                    continue
                if len(clean_keys) <= i:
                        clean_keys.append(str(token))
                else:
                    clean_keys[i] += " " + str(token)
        self.remove_duplicates(clean_keys)
        return clean_keys

    def get_keywords(self, story):
        story = unicode(story)
        print(story)
        doc = self.nlp(story)
        pps = self.get_pps(doc)
        # displacy.serve(doc, style="dep")
        nouns = []
        for chunk in doc.noun_chunks:
            nouns.append(chunk.root.text)
        #     print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
        # print(self.get_pps(doc))
        for i, noun in enumerate(nouns):
            for pp in pps:
                if noun in pp:
                    nouns[i] = pp
        clean_keys = self.clean_keywords(nouns)
        return map(str, clean_keys)
