#!/usr/bin/python

import os
import sys

def extract(string, start, end):
    if not start in string:
        print("extract(): couldn't find '" + start + "' in '" + string + "'")
        print("")
        return "" 
    i = string.find(start)
    i += len(start)
    s = string[i:]
    if not end in s:
        print("extract(): couldn't find '" + end + "' in '" + s + "' of '" + string + "'")
        print("")
        return s
    j = s.find(end)
    return s[:j]

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
    _works_end    = "\n#END_WORKS\n"

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
            print("Entry.verify(): length " + str(self.length) + " didn't match line count in:")
            print(self.text)
            print("")

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

def find_caps(s):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    lines = s.split("\n")
    for l in lines:
        if len(l) > 0 and l[0] == '#':
            continue
        for c in l:
            if c in lower and c not in upper:
                break
        else:
            print(l)

def compile_data(min_length):
    ofn = "sotd.clean.dat"

    files = pwd(".dat")
    if ofn in files:
        files.remove(ofn)

    data = Data("William Shakespeare")
    data.read_files(files, min_length)
    text = str(data)

    f = open(ofn, 'w')
    f.write(text)
    f.close()

if __name__ == "__main__":
    l = len(sys.argv)
    if l > 1:
        if sys.argv[1] == "compile":
            if l > 2:
                compile_data(int(sys.argv[2]))
            else:
                compile_data(6)
        elif sys.argv[1] == "caps":
            f = open(sys.argv[2], 'r')
            s = f.read()
            f.close()
            find_caps(s)
    else:
        compile_data(6)

