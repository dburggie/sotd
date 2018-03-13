
import os
import sys

def cut(text, substrings):
    clean = text
    for substring in substrings:
        clean = findreplace(clean, substring, "")
    return clean

def endswith(string, target):
    if string.rfind(target) + len(target) < len(string):
        return False
    else:
        return True

def precede(string, target, prefix):
    segments = string.split(target)
    acc = segments[0]
    for segment in segments[1:]:
        if not endswith(acc,prefix):
            acc += prefix
        acc += target + segment
    return acc

def remove_empty_lines(string):
    segments = string.split('\n')
    acc = []
    for s in segments:
        if len(s) > 0:
            acc.append(s)
    return '\n'.join(acc)

def cleanlines(string):
    lines = string.split("\n")
    stripped = []
    for line in lines:
        stripped.append(line.lstrip().rstrip())
    non_empty = []
    for line in stripped:
        if len(line) > 0:
            non_empty.append(line)
    return '\n'.join(non_empty)

def snip(string, start, end):
    segments = string.split(start)
    if len(segments) == 1:
        return string
    acc = segments[0]
    for segment in segments[1:]:
        split = segment.split(end,1)
        if len(split) == 1:
            acc += start + segment
            print 'ERROR: snip() found start="' + start + '" but not end="'+ end + '"'
            continue
        else:
            acc += split[1]
    return acc

def findreplace(string, find, replace):
    segments = string.split(find)
    acc = segments[0]
    for segment in segments[1:]:
        acc += replace + segment
    return acc

def extract(string, start, end):
    if not start in string:
        print "extract(): couldn't find '" + start + "' in '" + string + "'"
        print ""
        return ""
    s = string.split(start,1)[1]
    if not end in s:
        print "extract(): couldn't find '" + end + "' in '" + s + "' of '" + string + "'"
        print ""
        return ""
    return s.split(end,1)[0]


def pwd(substring = None):
    l = os.listdir(os.getcwd())
    l.sort()
    if substring != None:
        tmp = []
        for fn in l:
            if substring in fn:
                tmp.append(fn)
        l = tmp
    return l

class Data:
    _author_start = "#AUTHOR="
    _author_end   = "\n"
    _count_start  = "#WORK_COUNT="
    _count_end    = "\n"
    _works_start  = "#BEGIN_WORKS\n"
    _works_sep    = "\n#NEW_WORK\n"
    _works_end    = "\n#END_WORKS"

    def __init__(self, author):
        self.author = author
        self.works = []

    def read_files(self, files, min_length = 6):
        for fn in files:
            w = Work(fn, min_length)
            self.works.append(str(w))

    def __str__(self):
        s = Data._author_start + self.author + Data._author_end
        s += Data._count_start + str(len(self.works)) + Data._count_end
        s += Data._works_start
        s += Data._works_sep.join(self.works)
        s += Data._works_end
        return s

class Work:

    _title_start   = "#WORK_TITLE="
    _title_end     = "\n"
    _count_start   = "#ENTRY_COUNT="
    _count_end     = "\n"
    _entries_start = "#BEGIN_ENTRIES\n"
    _entries_sep   = "\n#NEW_ENTRY\n"
    _entries_end   = "\n#END_ENTRIES"

    def __init__(self, filename = None, min_length = 6):
        self.title = None
        self.entries = []
        if filename != None:
            self.read_file(filename, min_length)

    def read_file(self, filename, min_length = 6):
        f = open(filename, 'r')
        text = f.read()
        f.close()
        self.title = extract(text, Work._title_start, Work._title_end)
        self.entries = []
        entry_text = extract(text, Work._entries_start, Work._entries_end)
        for te in entry_text.split(Work._entries_sep):
            e = Entry(te)
            if e.length < min_length:
                continue
            else:
                self.entries.append(str(e))

    def __str__(self):
        s = Work._title_start + self.title + Work._title_end
        s += Work._count_start + str(len(self.entries)) + Work._count_end
        s += Work._entries_start
        s += Work._entries_sep.join(self.entries)
        s += Work._entries_end
        return s

class Entry:
    _blurb_start  = "#ENTRY_BLURB="
    _blurb_end    = "\n"
    _length_start = "#ENTRY_LENGTH="
    _length_end   = "\n"
    _text_start   = "#BEGIN_ENTRY_TEXT\n"
    _text_end     = "\n#END_ENTRY_TEXT"

    def __init__(self, text = None):
        self.blurb = None
        self.length = None
        self.text = None
        if text != None:
            self.read_text(text)

    def verify(self):
        lines = len(self.text.split('\n'))
        if lines != self.length:
            print "Entry.verify(): length " + str(self.length) + " didn't match line count in:"
            print self.text
            print ""

    def read_text(self, text):
        self.blurb = extract(text, Entry._blurb_start, Entry._blurb_end)
        self.length = int(extract(text, Entry._length_start, Entry._length_end))
        self.text = extract(text, Entry._text_start, Entry._text_end)
        self.verify()

    def __str__(self):
        s = Entry._blurb_start + self.blurb + Entry._blurb_end
        s += Entry._length_start + str(self.length) + Entry._length_end
        s += Entry._text_start + self.text + Entry._text_end
        return s



def indent():
    files = pwd(".dat")
    for fn in files:
        if ".clean" in fn:
            continue

        f = open(fn,'r')
        text = f.read()
        f.close()

        lines = text.split("\n")
        i = 0
        on = False
        while i < len(lines):
            if "END_ENTRY_TEXT" in lines[i]:
                on = False
            if on:
                lines[i] = "  " + lines[i]
            if "BEGIN_ENTRY_TEXT" in lines[i]:
                on = True
            i += 1
        text = '\n'.join(lines)

        ofn = findreplace(fn, '.dat', '.clean.dat')
        f = open(ofn, 'w')
        f.write(text)
        f.close()

def translate():
    files = pwd(".dat")
    for fn in files:
        if ".clean" in fn:
            continue

        f = open(fn,'r')
        text = f.read()
        f.close()

        text = findreplace(text, "TITLE={", "#WORK_TITLE=")
        text = findreplace(text, "}\nCOUNT={", "\n#ENTRY_COUNT=")
        text = findreplace(text, "}\nENTRIES=", "\n#BEGIN_ENTRIES")
        text = findreplace(text, "{\nBLURB={", "\n#ENTRY_BLURB=")
        text = findreplace(text, "}\nBLURB={","#END_ENTRY_TEXT\n#NEW_ENTRY\n#ENTRY_BLURB=")
        text = findreplace(text, "}\nLENGTH={","\n#ENTRY_LENGTH=")
        text = findreplace(text, "}\nTEXT={","\n#BEGIN_ENTRY_TEXT")
        text = findreplace(text, "\n}\n}", "\n#END_ENTRY_TEXT\n#END_ENTRIES")

        f = open(fn,'w')
        f.write(text)
        f.close()

def compile_data(min_length):
    ofn = "sotd.dat"

    files = pwd(".dat")
    if ofn in files:
        files.remove(ofn)

    data = Data("William Shakespeare")
    data.read_files(files)
    text = str(data)

    f = open(ofn, 'w')
    f.write(text)
    f.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "translate":
            translate()
        elif sys.argv[1] == "compile":
            if len(sys.argv) > 2:
                min_length = int(sys.argv[2])
            else:
                min_length = 6
            compile_data(6)

