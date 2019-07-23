import random
from random import randrange
from pyrhyme.rhyme import rhymes_with

#TODO: alliterative interface

BALLAD_RHYTHM = (
    ("01", "01", "01", "01",),
    ("01", "01", "01", ),
    ("01", "01", "01", "01",),
    ("01", "01", "01", ),
)

IAMBIC_PENTAMETER = ("01", "01", "01", "01", "01")

RHYTHMS = (
    ("10", "01"),
    ("100" , "1"),
    ("1" , "001"),
    ("1" , "1", "01"),
    ("10", "1", "1"),
    #("1" , "0", "01"), 
    #("10", "0", "1"),
)

POSSIBLE_RHYTHMS = (
    "001",
    "010",
    "01",
    "100",
    "10",
    "11",
    "1",
)
RHYTHMIZER_ERROR = "something is getting stuck in the rhythmizer. at the time of writing this, the primary issue was single 0s at the end: that's why it catches them and changes them to 1s. whatever issue you're facing now is something i didn't face"

ROSES_LENGTH = 4
POEM_LENGTH = 4
SONNET_LENGTH = 14
#only have word lists for >= 3 syllable words
MAX_WORD_LENGTH = 3

def rhythmizer(rhythm, max_word_length=MAX_WORD_LENGTH):
    if len(rhythm) == 1:
        return rhythm

    i = 0
    slices = []
    while i < len(rhythm):
        # - 1 negates the + 1; keels it under the max length
        slice_size = randrange(max_word_length - 1) + 1
        while i + slice_size > len(rhythm):
            slice_size = randrange(max_word_length - 1) + 1
            #retry until the slice works
        rhythm_slice = rhythm[i:i+slice_size]
        if rhythm_slice in POSSIBLE_RHYTHMS:
            slices.append(rhythm_slice)
            i += slice_size
        elif rhythm_slice == "0":
            #TODO: implement weak single syllable words
            slices.append("1")
            i += slice_size
        else:
            raise Exception(RHYTHMIZER_ERROR)

    return slices

def ballad_rhythmizer(basic=True):
    l = ("01","01","01","01")
    s = ("01","01","01")
    if basic:
        return (l,s,l,s)
    else:
        l = "".join(l)
        s = "".join(s)
        return (
            rhythmizer(l),
            rhythmizer(s),
            rhythmizer(l),
            rhythmizer(s),
        )

def find_rhyme(word, rhythmic_words):
    rhyming_words = rhymes_with(word)
    possible_words = [
        possibility for possibility in rhythmic_words 
        if possibility in rhyming_words
    ]
    try:
        return possible_words[randrange(len(possible_words))]
    except ValueError:
        print(word)
        raise Exception("didn't find any rhymes!")

def gen_line(rhythms, rhyme=None):
    line = []
    for i, word in enumerate(rhythms):
        possible_words = [word.rstrip() for word in open(f"{word}.txt").readlines()]
        if rhyme and i == (len(rhythms) - 1):
            word = find_rhyme(rhyme, possible_words)
        else:
            word = possible_words[randrange(len(possible_words))]
        line.append(word)
    return {
        "line": " ".join(line),
        "last_word": word,
    }

def main(
    poem_length=POEM_LENGTH,
    rhythms=RHYTHMS,
    lines=None,
    rhyme_scheme=None,
):
    poem = []
    rhymes_schemed = {}

    for line in range(poem_length):
        rhymed = False
        line_data = {}
        try:
            line_data["line"] = lines[line]
            line_data["last_word"] = line_data["line"].split()[-1]
        except:
            try:
                #get the rhyme
                rhyme = rhymes_schemed[rhyme_scheme[line]]
                rhymed = True
            except KeyError:
                pass
                
            if rhymed:
                line_data = gen_line(rhythms[line], rhyme=rhyme)
            else:
                line_data = gen_line(rhythms[line], rhyme=None)
        finally:
            if not rhymed:
                try:
                    rhymes_schemed[rhyme_scheme[line]] = line_data["last_word"]
                except KeyError:
                    pass
        poem.append(line_data["line"])

    return "\n".join(poem)


if __name__ == "__main__":
    poem = ""
    ballad = 0
    roses = 1
    sonnet = 0

    if ballad:
        rhythms = ballad_rhythmizer(basic=False)
        poem = main(
            poem_length=4,
            rhythms=rhythms,
            rhyme_scheme="abcb",
        )
    elif roses:
        roses_rhythms = [
            RHYTHMS[randrange(len(RHYTHMS))]
            for line in range(ROSES_LENGTH)
        ]
        poem = main(
            poem_length=ROSES_LENGTH,
            rhythms=roses_rhythms,
            lines=["roses are red",
                   "violets are blue"],
            rhyme_scheme="abcb",
        )
    elif sonnet:
        poem = main(
            poem_length=SONNET_LENGTH,
            rhythms=[IAMBIC_PENTAMETER for line in range(SONNET_LENGTH)],
            rhyme_scheme="ababcdcdefefgg"
        )

    print(poem)
