class DecodeInfo:

    def __init__(self, o_data, data, org_enc) -> None:
        super().__init__()
        self.o_data = o_data
        self.data = data
        self.original_encoding = org_enc

    def get_Data(self):
        return self._data

    def set_Data(self, value):
        self._data = value

    def del_Data(self):
        self._data = None

    data = property(get_Data, set_Data, del_Data, 'Раскодированный текст.')

    def get_Original_Data(self):
        return self._o_data

    def set_Original_Data(self, value):
        self._o_data = value

    def del_Original_Data(self):
        self._o_data = None

    o_data = property(get_Original_Data, set_Original_Data, del_Original_Data, 'Исходный текст.')

    def get_Original_Encoding(self):
        return self._org_enc

    def set_Original_Encoding(self, value):
        self._org_enc = value

    def del_Original_Encoding(self):
        self._org_enc = None

    original_encoding = property(get_Original_Encoding, set_Original_Encoding, del_Original_Encoding,
                                 'Исходная кодировка.')
