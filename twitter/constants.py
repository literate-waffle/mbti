from itertools import product

MBTI_TYPES = {a + b + c + d for a, b, c, d in product("EI", "NS", "FT", "PJ")}
assert len(MBTI_TYPES) == 16
