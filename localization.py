import os
class Localization:
    def __init__(self, element: int, user_language):
        self.element = element
        self.lang_list = os.listdir('local')
        self.set_language = user_language
        if user_language in self.lang_list:
            self.set_language = user_language
        elif user_language == 'ru':
            self.set_language = 'uk'
        else:
            self.set_language = 'en'

    def __str__(self):
        with open(f'Languages/{self.set_language}.txt', 'r') as file:
            funct = (eval(file.read()))
            return funct[self.element]