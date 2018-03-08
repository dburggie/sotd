
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

class Play:

    _bad_tags = ["<html>","</html>","<head>","</head>","<br>","<p>","</p>","<body>","</body>"]
    _good_tags = [("<title>","</title>"), ("<blockquote>","</blockquote>"), ("<a", "</a>")]

    def __init__(self):
        self.infile = None
        self.outfile = None
        self.text = None
        self.done = False

    def readfile(self,filename):
        if not ".html" in filename:
            print "Play.read(): failing to open " + filename + ": not html"
            return
        self.infile = filename
        self.outfile = filename
        if not ".clean" in filename:
            self.outfile = findreplace(filename, ".html", ".clean.html")
        f = open(filename, 'r')
        self.text = f.read()
        f.close()
        self.done = False

    def write(self):
        if not self.done:
            print "Play.write(): failing because data is not clean"
            return
        f = open(self.outfile,'w')
        f.write(self.text)
        f.close()

    def sanitize(self):
        self.cut_tags()
        self.cleanup()
        self.remove_headers()
        self.cleanup()
        self.remove_italics()
        self.cleanup()
        self.one_tag_per_line()
        self.cleanup()
        self.remove_empty_blockquotes()
        self.cleanup()
        self.match_tags()
        self.done = True

    def cut_tags(self):
        self.text = cut(self.text,Play._bad_tags)
        self.cleanup()

    def remove_headers(self):
        lines = self.text.split("\n")
        temp = []
        for line in lines:
            if not "<h" in line:
                temp.append(line)
        self.text = '\n'.join(temp)

    def cleanup(self):
        self.text = cleanlines(self.text)

    def remove_italics(self):
        self.text = snip(self.text, "<i>", "</i>")

    def one_tag_per_line(self):
        s = self.text
        s = precede(s, "<blockquote>", "\n")
        s = precede(s, "</blockquote>", "\n")
        s = precede(s, "<a", "\n")
        s = findreplace(s, "\n</a>", "</a>")
        self.text = s

    def remove_empty_blockquotes(self):
        self.text = cut(self.text, ["<blockquote>\n</blockquote>"])

    def match_tags(self):
        for pair in Play._good_tags:
            sections = self.text.split(pair[0])[1:]
            for s in sections:
                if not pair[1] in s:
                    e = "Play.match_tags(): "
                    e += "FILE:" + self.infile + " "
                    e += "ERR: could not find '" + pair[1] + "'"
                    print e
                    if s == sections[-1]:
                        print "attempting fix..."
                        self.text += '\n' + pair[1]
                    else:
                        print "FIX MANUALLY"

class Sonnet:

    def __init__(self):
        self.text = None
        self.clean = None
        self.infile = None
        self.outfile = None
        self.number = None
        self.done = False

    def get_number(self):
        s = self.infile
        s = findreplace(s, "sonnet_", "")
        s = findreplace(s, ".html", "")
        self.number = int(s)

    def readfile(self, filename):
        self.infile = filename
        self.outfile = findreplace(filename, ".html", ".clean.html")
        f = open(filename,'r')
        self.text = f.read()
        f.close()
        print "Sonnet.readfile(): read " + str(len(self.text)) + "B from " + self.infile
        self.clean = self.text
        self.get_number()
        self.done = False

    def cleanup(self):
        s = self.clean

        #fix tags
        s = findreplace(s, "<h1>", '<a name="speech"><b>')
        s = findreplace(s, "</h1>", "</b></a>")
        s = findreplace(s, "<blockquote>", "<blockquote>\n")
        s = findreplace(s, "<br>", "")

        #add <a> tags to lines
        processing = False
        lines = s.split("\n")
        clean = []
        counter = 0
        for line in lines:
            if "</blockquote>" in line:
                processing = False
            if processing:
                counter += 1
                sig = '0.' + str(self.number) + '.' + str(counter)
                line = '<a NAME="' + sig + '">' + line + '</a>'
            if "<blockquote>" in line:
                processing = True
            clean.append(line)
        s = clean[0]
        for line in clean[1:]:
            s += '\n' + line

        self.clean = cleanlines(s)
        self.done = True

    def write(self):
        if self.done:
            f = open(self.outfile, 'w')
            f.write(self.clean)
            f.close()
            print "Sonnet.write(): wrote " + str(len(self.clean)) + "B to " + self.outfile
        else:
            print "Sonnet.write(): failed to write: not done processing"


def compile_sonnets():
    outfilename = "sonnets.html"
    files = os.listdir(os.getcwd())
    files.sort()
    s = "<title>The Sonnets</title>\n"
    for fn in files:
        if ".clean.html" in fn:
            print 'compile_sonnets(): appending ' + fn
            f = open(fn,'r')
            s += f.read() + '\n'
            f.close()
        else:
            print 'compile_sonnets(): skipping ' + fn
    f = open(outfilename,'w')
    f.write(s)
    f.close()
    print "compile_sonnets(): " + str(len(s)) + "B written to " + outfilename

def handlefile(fn):
    if not '.html' in fn:
        print "skipping file " + fn + " not html..."
        return
    if "sonnet_" in fn:
        s = Sonnet()
        s.readfile(fn)
        s.cleanup()
        s.write()
        return
    else:
        p = Play()
        p.readfile(fn)
        p.sanitize()
        p.write()
        return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "sonnets":
            compile_sonnets();
            sys.exit()
        fn = sys.argv[1]
        handlefile(fn)
        sys.exit()
    files = os.listdir(os.getcwd())
    files.sort()
    for fn in files:
        handlefile(fn)




