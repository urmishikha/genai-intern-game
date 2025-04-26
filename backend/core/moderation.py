from better_profanity import profanity

class Moderation:
    def __init__(self):
        profanity.load_censor_words()

    def has_profanity(self, text: str) -> bool:
        return profanity.contains_profanity(text)