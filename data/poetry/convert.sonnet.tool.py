
import os

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
        if endswith(acc,prefix):
            acc += target + segment
        else:
            acc += prefix + target + segment
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
    if len(non_empty) == 0:
        print "cleanlines(): all lines were empty for some reason"
        return ""
    acc = non_empty[0]
    for line in non_empty[1:]:
        acc += '\n' + line
    return acc

def excise(string, start, end):
    segments = string.split(start)
    if len(segments) == 1:
        return string
    acc = segments[0]
    for segment in segments[1:]:
        split = segment.split(end,1)
        if len(split) == 1:
            acc += start + segment
            print 'ERROR: excise() found start="' + start + '" but not end="'+ end + '"'
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

def clean_sonnets():
    files = os.listdir(os.getcwd())
    files.sort()
    for fn in files:
        if not "sonnet_" in fn or ".clean" in fn or not ".html" in fn:
            print "clean_sonnets(): skipping " + fn
            continue
        else:
            s = Sonnet()
            s.readfile(fn)
            s.cleanup()
            s.write()


if __name__ == "__main__":

    clean_sonnets()
    compile_sonnets()


