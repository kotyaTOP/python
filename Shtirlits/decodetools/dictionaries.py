from abc import ABCMeta, abstractmethod


class Dict:
    word_dict = None

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def has(self, data: str) -> bool: raise NotImplementedError

    @staticmethod
    def load(f_name):
        with open(f_name, 'r') as f:
            w_dict = str(f.read()).split(' ')
        return w_dict


class RussianDict(Dict):

    def __init__(self) -> None:
        super().__init__()
        # self.word_dict = self.load('../dictionaries/rus.txt')  # fixme doesnt work :(
        self.word_dict = ['привет', 'мир']

    def has(self, data: str) -> bool:
        for word in self.word_dict:
            if word == data.lower():
                return True
        return False


class EngDict(Dict):

    def __init__(self) -> None:
        super().__init__()
        # self.word_dict = self.load('../dictionaries/eng.txt')  # fixme doesnt work :(
        self.word_dict = ['hello', 'world']

    def has(self, data: str) -> bool:
        for word in self.word_dict:
            if word == data.lower():
                return True
        return False
