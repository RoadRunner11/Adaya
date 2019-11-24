import re


class Utility():
    """
    Utility is a generic toolbox
    """
    @staticmethod
    def slugify(strings, separator="-", to_lower=True):
        # use regex to replace all the special character to '-'
        chars = re.sub("[^a-zA-Z0-9\n\.]", separator, strings)
        if to_lower:
            chars = chars.lower()
        return strings
