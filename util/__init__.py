class DummyObject:
    pass


class Numoji:
    numojis = { 0: '0️⃣', 1: '1️⃣',
        2: '2️⃣', 3: '3️⃣', 4: '4️⃣',
        5: '5️⃣', 6: '6️⃣', 7: '7️⃣',
        8: '8️⃣', 9: '9️⃣', 10: '🔟'}

    @classmethod
    def get_int(cls, emoji):
        for i, e in cls.numojis.items():
            if e == emoji:
                return i

    @classmethod
    def get_emoji(cls, num):
        return cls.numojis[num]