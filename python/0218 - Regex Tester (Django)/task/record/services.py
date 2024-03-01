import re


class RegexService:
    @staticmethod
    def match(*, regex, text):
        return bool(re.match(regex, text))
