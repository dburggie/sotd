
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
        self.clean_metadata()
        self.match_tags()
        self.done = True

    def clean_metadata(self):
        # some lines are noted as '<a NAME=ENTRY>' others as '<a name="ENTRY">'
        # make uniformly '<a name="ENTRY">'
        lines = self.text.split('\n')
        acc = []
        for l in lines:
            if "<a NAME=" in l:
                metadata, text = l.split('=',1)[1].split('>',1)
                l = '"'.join(["<a name=",metadata, ">" + text])
            acc.append(l)
        self.text = '\n'.join(acc)

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
                        print s

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

def compile_plays():
    files = []
    for fn in pwd():
        if ".clean" in fn:
            files.append(fn)
    for fn in files:
        w = Work()
        w.read_html(fn)
        w.parse_html()
        w.write()

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
    elif ".clean.html" in fn:
        w = Work()
        w.read_html(fn)
        w.parse_html()
        w.write()
    else:
        p = Play()
        p.readfile(fn)
        p.sanitize()
        p.write()
        return




def itoRN(i):
    translator = ["","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV"]
    if i > 0 and i < len(translator):
        return translator[i]
    else:
        print "itoRN: couldn't translate " + str(i) + ": out of bounds"


# read from html text that looks like this:
# <a name="speechX"><b>SPEAKER</b></a>
# <blockquote>
# <a name="a.s.{l}">LINE_0</a>
# ...
# <a name="a.s.{l+n}">LINE_N</a>
class Entry:
    def __init__(self, title, html, entry_type):
        self.title = title
        self.html = html

        self.blurb = None
        self.length = None
        self.text = None

        if entry_type == "sonnet":
            self.parse_sonnet()
        elif entry_type == "speech":
            self.parse_speech()
        else:
            print "Entry.__init__(): couldn't figure out how to parse type " + str(t)

    def verify(self):
        lines = self.html.split('\n')
        if not len(lines) > 1:
            print "Entry.verify(): what is happening"
            print self.title
            print self.html
            return
        verified = True
        verified &= '<a name="speech' in lines[0] and "</a" in lines[0]
        verified &= '<blockquote>' in lines[1]
        for l in lines[2:]:
            verified &= '<a name="' in l and '</a>' in l
        if not verified:
            print "Entry.verify(): doesn't look parsable:"
            print self.title
            print self.html

    def parse_speech(self):
        self.verify()
        self.get_length()
        self.get_speech_blurb()
        self.get_text()

    def parse_sonnet(self):
        self.verify()
        self.get_length()
        self.get_sonnet_blurb()
        self.get_text()

    def get_speaker(self):
        s = self.html.split('\n')[0]
        s = snip(s, "<a", "<b>")
        s = snip(s, "</b>", "</a>")
        return s

    # get a,s from '<a name="a.s.l"><b>TEXT</b></a>'
    def get_act_scene(self):
        s = self.html.split('\n')[2]
        s = s.split('"')[1]
        asl = s.split('.')
        if len(asl) < 3:
            print "Entry.get_act_scene(): TITLE: " + self.title + " READ_ERROR"
            return ""
        act, scene, line = asl
        if act == "0":
            act = "PROLOGUE"
        else:
            act = "Act " + itoRN(int(act))
        if scene == "0":
            return act + ", PROLOGUE"
        else:
            scene = "Scene " + itoRN(int(scene))
        return act + ", " + scene

    def get_length(self):
        self.length = len(self.html.split('\n')) - 2

    def get_text(self):
        lines = self.html.split('\n')[2:]
        acc = []
        for l in lines:
            l = snip(l, "<a", ">")
            l = findreplace(l, "</a>", "")
            acc.append(l)
        self.text = '\n'.join(acc)

    def get_speech_blurb(self):
        self.blurb = self.get_speaker()
        self.blurb += " - "
        self.blurb += self.title
        self.blurb += " - "
        self.blurb += self.get_act_scene()

    def get_sonnet_blurb(self):
        self.blurb = "William Shakespeare, " + self.get_speaker()

    def __str__(self):
        s = "BLURB={" + self.blurb + "}\n"
        s += "LENGTH={" + str(self.length) + "}\n"
        s += "TEXT={\n" + self.text + "\n}"
        return s

class Work:
    def __init__(self):
        self.outfile = None
        self.infile = None
        self.title = None
        self.count = 0
        self.html = None
        self.text = None
        self.done = False
        self.entry_type = None

    def read_html(self, filename):
        if not ".html" in filename:
            print "Work.read_html(): " + filename + " doesn't look like html"
            return

        if "sonnet" in filename:
            self.entry_type = "sonnet"
        else:
            self.entry_type = "speech"

        self.infile = filename
        self.outfile = filename.split('.')[0] + ".dat"

        f = open(filename,'r')
        self.html = f.read()
        f.close()

    def parse_html(self):
        self.title, body = self.html.split("</title>\n", 1)
        self.title = findreplace(self.title, "<title>", "")

        entries_html = body.split("</blockquote>")
        entries = []

        for html in entries_html:
            html = remove_empty_lines(html)
            if len(html) == 0:
                continue
            entries.append(str(Entry(self.title, html, self.entry_type)))
        
        self.text = "TITLE={" + self.title + "}\n"
        self.text += "COUNT={" + str(len(entries)) + "}\n"
        self.text += "ENTRIES={\n" + '\n'.join(entries) + "\n}"
        self.done = True

    def write(self):
        if not self.done:
            print "Work.write(): have nothing to write"
            return
        f = open(self.outfile, 'w')
        f.write(self.text)
        f.close()
        print "Work.write(): wrote " + str(len(self.text)) + "B to " + self.outfile
        return


def pwd():
    l = os.listdir(os.getcwd())
    l.sort()
    return l

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "sonnets":
            compile_sonnets()
            sys.exit()
        if sys.argv[1] == "compile":
            compile_plays()
            sys.exit()
        fn = sys.argv[1]
        handlefile(fn)
        sys.exit()
    for fn in pwd():
        if not ".clean" in fn:
            handlefile(fn)




