"""
Performs keyword extraction on story.
Return list of tuples.
Tuples are associated keywords.
"""

from rake_nltk import Rake


class StoryInterpreter:
    def __init__(self):
        self.r = Rake()

    def get_keywords(self, story):
        print(story)
        keywords_list = self.r.extract_keywords_from_text(story)
<<<<<<< HEAD
        return self.r.get_ranked_phrases()
=======
        return self.r.get_ranked_phrases()
>>>>>>> fa09b87f0ceb81cb2738af1c5fd6ad74f57a025c
