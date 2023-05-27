import os


class Lang:

    def __init__(self, lang_type: str, element: int):
        self.element = element
        self.__lang_list = os.listdir('local')
        self.lang_settings = 'en'
        if lang_type in self.__lang_list:
            self.lang_settings = lang_type

    def __str__(self):
        with open(f'local/{self.lang_settings}', 'r') as file:
            return list(eval(file.read()))[self.element]
