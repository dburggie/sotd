

# What we need to do:
# Each speach is within a <blockquote></blockquote> pair
# Each speach block is preceded by the speaker like this:
#       <a NAME=speech1><b>ANTIOCHUS</b></a>
#
# Each line of a speach goes like this
#       <a NAME=1.1.1>Young Prince of Tyre, you have at large received</a><br>

# that attribute tag contains act, scene, and line number in that order
# sometimes there's a speach with no speaker, which would go to CHORUS
# if Scene number is 0 for a line, it is PROLOGUE

# TITLE={Pericles, Prince of Tyre}
# SPEAKER={CHORUS}
# ACT={1.0.1-42}
# LENGTH={42}
# TEXT={
# To sing a song that old was sung,
# From ashes ancient Gower is come;
# Assuming man's infirmities,
# To glad your ear, and please your eyes.
# ...
# What now ensues, to the judgment of your eye
# I give, my cause who best can justify.
# }

# safely ignore things in <i> tags
# probably safe to ignore things in <p> tags, too

# Extract text in <blockquote> tags
# extract lines and act,scene,line_no info from inside <a> tags
# Exctract speaker from just before the <blockquote> block, if possible


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

class Sanitizer:
    def __init__(self, filename):
        self.filename = filename
        self.original_contents = ""
        self.sanitized_contents = ""
        self.sanitized = False
        self.report("__init__")

    def report(self, function):
        print "Sanitizer."+function+"(): sanitized length: "+str(len(self.sanitized_contents))

    def read(self):
        f = open(filename, 'r')
        self.original_contents = f.read()
        f.close()
        self.sanitized_contents = self.original_contents
        self.sanitized = False
        self.report("read")

    def write(self):
        if not self.sanitized:
            print "### skipping Sanitizer.write(), call Sanitizer.sanitize() first"
            return
        newfilename = findreplace(self.filename, '.html', '.clean.html')
        f = open(newfilename,'w')
        f.write(self.sanitized_contents)
        f.close()
        self.report("write")

    # remove all <html>,</html>,<head>,</head>,<br>,<p>,</p>,<body>,</body> tags
    # remove all lines starting with <h
    # remove everything within <i></i> pairs
    # ensure <blockquote>,</blockquote>, and <a have a newline before them
    # remove newline characters preceding a </a>
    # remove empty <blockquote> blocks
    def sanitize(self):
        self.cut_tags()
        self.remove_headers()
        self.remove_italics()
        self.one_tag_per_line()
        self.remove_empty_blockquotes()
        self.sanitized = True
        self.report("sanitize")

    def cut_tags(self):
        tags= []
        tags.append("<html>")
        tags.append("</html>")
        tags.append("<head>")
        tags.append("</head>")
        tags.append("<br>")
        tags.append("<p>")
        tags.append("</p>")
        tags.append("<body>")
        tags.append("</body>")
        self.sanitized_contents = cut(self.sanitized_contents,tags)
        self.report("cut_tags")
        self.cleanup()

    def remove_headers(self):
        lines = self.sanitized_contents.split("\n")
        temp = []
        for line in lines:
            if line.find("<h") < 0:
                temp.append(line)
        if len(temp) == 0:
            self.sanitized_contents = ""
            return
        acc = temp[0]
        for line in temp[1:]:
            acc += '\n' + line
        self.sanitized_contents = acc
        self.report("remove_headers")
        self.cleanup()

    def cleanup(self):
        self.sanitized_contents = cleanlines(self.sanitized_contents)
        self.report("cleanup")

    def remove_italics(self):
        self.sanitized_contents = excise(self.sanitized_contents, "<i>", "</i>")
        self.report("remove_italics")
        self.cleanup()

    def one_tag_per_line(self):
        wip = self.sanitized_contents
        wip = precede(wip, "<blockquote>", "\n")
        wip = precede(wip, "</blockquote>", "\n")
        wip = precede(wip, "<a", "\n")
        wip = findreplace(wip, "\n</a>", "</a>")
        self.sanitized_contents = wip
        self.report("one_tag_per_line")
        self.cleanup()

    def remove_empty_blockquotes(self):
        wip = self.sanitized_contents
        wip = cut(wip, ["<blockquote>\n</blockquote>"])
        self.sanitized_contents = wip
        self.report("remove_empty_blockquotes")
        self.cleanup()

        

if __name__ == "__main__":
    files = os.listdir(os.getcwd())
    files.sort()
    for filename in files:
        if filename.find(".html") < 0:
            continue
        if endswith(filename,".clean.html"):
            continue
        s = Sanitizer(filename)
        s.read()
        s.sanitize()
        s.write()




# second pass extract








