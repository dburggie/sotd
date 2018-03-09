import os, sys

def pwd():
    files = os.listdir(os.getcwd())
    files.sort()
    return files

def get_italics(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    acc = []
    for l in lines:
        if "<i>" in l:
            acc.append(l)
    return acc

def remove_stage_directions(lines):
    stage_dirs = ["Enter", "Exit", "Exeunt", "Flourish", "Re-enter"]
    acc = []
    for l in lines:
        save = True
        for sd in stage_dirs:
            if sd in l:
                save = False
        if save:
            acc.append(l)
    return acc

def process(filenames):
    outfilename = "italics.note"
    acc = []
    for fn in filenames:
        if not ".html" in fn:
            print "skipping " + fn
            continue
        italics = get_italics(fn)
        italics = remove_stage_directions(italics)
        for l in italics:
            acc.append(fn + ":" + l)
    f = open(outfilename,'w')
    f.write('\n'.join(acc))
    f.close()

        


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filenames = sys.argv[1]
    else:
        filenames = pwd()
    process(filenames)
