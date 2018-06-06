from decodetools.decode_info import DecodeInfo
from decodetools.dictionaries import RussianDict, EngDict


class Decoder:
    encodings = [
        'latin_1',  # ISO-8859-1
        'cp1251',  # Windows-1251
        'cp861',  # IBM861
        'utf-8'  # UTF-8
    ]

    @staticmethod
    def decode(data: str) -> DecodeInfo:
        return Decoder.__decode(data)

    @staticmethod
    def __decode(data: str):
        for current_encoding in Decoder.encodings:
            try:
                result = bytes(data, encoding=current_encoding).decode(encoding='utf-8')
            except UnicodeEncodeError:
                continue
            except UnicodeDecodeError:
                continue
            if Decoder.__check(result):
                return DecodeInfo(data, result, current_encoding)
        # bytes(data, encoding='cp1251').decode(encoding='utf-8')
        return DecodeInfo(data, data, 'unknown')  # РџСЂРёРІРµС‚, РјРёСЂ!

    @staticmethod
    def __check(data: str) -> bool:
        substr_list = data.split(sep=' ')
        r = RussianDict()
        e = EngDict()  # todo engDict
        for substr in substr_list:
            substr = substr.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':',
                                                                                                        '').replace(';',
                                                                                                                    '')
            if r.has(substr):
                return True
            elif e.has(substr):
                return True
        return False
