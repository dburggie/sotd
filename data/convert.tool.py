
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
    def __init__(self, author):
        self.author = author
        self.works = []

    def add_work(self, work):
        self.works.append(work)

    def __str__(self):
        s = "AUTHOR={" + self.author + "}/n"
        s += "WORK_COUNT={" + str(len(self.works)) + "}\n"
        s += "WORKS={\n"
        for w in self.works:
            s += str(w) + '\n'
        s += '}'
        return s

class Work:
    def __init__(self, filename = None, min_length = 6):
        self.title = None
        self.entries = []
        if filename != None:
            self.read_file(filename, min_length)

    def read_file(self, filename, min_length = 6):
        f = open(filename, 'r')
        text = f.read()
        title_line = text.split('\n',1)[0]
        self.title = extract(title_line, '{', '}')
        text_entries = text.split("BLURB")[1:]
        for te in text_entries:
            e = Entry("BLURB" + te)
            if e.length < min_length:
                continue
            else:
                self.entries.append(e)
    def __str__(self):
        s = "TITLE={" + self.title + "}\n"
        s += "COUNT={" + str(len(self.entries)) + "}\n"
        s += "ENTRIES={\n"
        for e in self.entries:
            s += str(e) + '\n'
        s += "}"
        return s

class Entry:
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
        self.blurb = extract(text, "BLURB={","}")
        self.length = int(extract(text, "LENGTH={","}"))
        self.text = extract(text, "TEXT={\n","\n}")
        self.verify()

    def __str__(self):
        s = "BLURB={" + self.blurb + "}\n"
        s += "LENGTH={" + str(self.length) + "}\n"
        s += "TEXT={\n" + self.text + "\n}"
        return s


if __name__ == "__main__":
    outfile = "sotd.dat"
    files = pwd(".dat")
    data = Data("William Shakespeare")
    for fn in files:
        w = Work(fn)
        data.add_work(w)
    f = open(outfile, 'w')
    f.write(str(data))
    f.close()






