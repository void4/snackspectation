from random import choice, randint
import re

from hyphen import Hyphenator
from jellyfish import soundex, metaphone, match_rating_codex, match_rating_comparison, damerau_levenshtein_distance
from pronouncing import rhymes

#h_de = Hyphenator('de_DE')

words = open("google-10000-english.txt").read().splitlines()
#print(words)

h_en = Hyphenator('en_US')

def common(a,b):
    return len(set(a) & set(b))

def a0():
    a = choice(words)#"Snack"
    b = choice(words)#"Expectation"

    #print(a,b)

    sa = h_en.syllables(a)
    sb = h_en.syllables(b)

    #print(sa, sb)

    fa = a if len(sa) == 0 else sa[0]
    fb = b if len(sb) == 0 else sb[0]

    if fa == fb or len(sb) in [0,1] or len(sa) != 1:
        # Same first syllable, skip
        return

    xa = soundex(fa)
    xb = soundex(fb)

    ma = metaphone(fa)
    mb = metaphone(fb)
    #print(xa, xb)
    xc = common(xa, xb)
    mc = common(ma, mb)
    if xc + mc > 2:
        #print(xc, mc)
        print(fa+"".join(sb[1:]), "=", a, "+", b)

def a1():
    a = choice(words)
    sa = h_en.syllables(a)
    if len(sa) < 2:
        return

    rh = rhymes(sa[0])
    if len(rh) == 0:
        return
    print(choice(rh) + "".join(sa[1:]))

firstsyls = [[h_en.syllables(w)[0], w] for w in words if len(h_en.syllables(w)) == 1]#>0
mrc = [[match_rating_codex(w[0]), w[0], w[1]] for w in firstsyls]
#print(mrc)

def similar_sounding(syl):

    fmrc = match_rating_codex(syl)

    #allw = [[match_rating_comparison(sa[0], c[0]), c[1]] for c in mrc]
    #allw = [c for c in allw if c[0]]

    allw = [[damerau_levenshtein_distance(fmrc, c[0]), c[1], c[2]] for c in mrc]
    rh = sorted(allw, key=lambda x:x[0], reverse=False)
    #print(rh)
    if len(rh) == 0:
        return

    return choice(rh[:len(rh)//100])

def text2words(text):
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)

def a2():
    a = choice(words)
    sa = h_en.syllables(a)
    if len(sa) < 3:#<2
        return

    #choice(allw)[1]
    #print(len(rh))
    first = similar_sounding(sa[0])
    print(first[1] + "".join(sa[1:]), "=", first[2], "+", a)

def sentence(text):
    words = text2words(text)
    result = ""
    for w in words:
        if len(w) > 1:
            sw = h_en.syllables(w)
            if len(sw) < 1:
                result += " " + w
            else:
                first = similar_sounding(sw[0])
                result += " " + first[1] + "".join(sw[1:])
        else:
            result += w +" "

    result = result.replace("  ", " ")[1:]

    print(result)
    return result

def sentence2(text):
    words = text2words(text)
    result = ""
    for w in words:
        if len(w) > 1:
            sw = h_en.syllables(w)
            if len(sw) < 2:
                result += " " + w
            else:
                index = randint(0, len(sw)-1)
                first = similar_sounding(sw[index])[1]
                sw[index] = first
                result += " " + "".join(sw)
        else:
            result += w +" "

    result = result.replace("  ", " ")[1:]

    print(result)
    return result

for i in range(1000):
    a2()

"""
import sys
current = sys.argv[1]
for i in range(250):
    current = sentence2(current)
"""
