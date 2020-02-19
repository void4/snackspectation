from random import choice

from hyphen import Hyphenator
from jellyfish import soundex
#h_de = Hyphenator('de_DE')

words = open("google-10000-english.txt").read().splitlines()
print(words)
h_en = Hyphenator('en_US')

def common(a,b):
    return len(set(a) & set(b))

for i in range(1000):
    a = choice(words)#"Snack"
    b = choice(words)#"Expectation"

    #print(a,b)

    sa = h_en.syllables(a)
    sb = h_en.syllables(b)

    #print(sa, sb)

    fa = a if len(sa) == 0 else sa[0]
    fb = b if len(sb) == 0 else sb[0]

    if fa == fb or len(sb) in [0,1]:
        # Same first syllable, skip
        continue

    xa = soundex(fb)
    xb = soundex(fb)

    #print(xa, xb)
    c = common(xa, xb)
    print(c)
    print(fa+"".join(sb[1:]), "=", a, "+", b)
