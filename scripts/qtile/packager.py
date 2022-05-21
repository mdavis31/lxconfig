import os, subprocess
import glob

VERSION = "1.0"
QTILE_PATH = os.path.expanduser("~/.config/qtile")
BACKUP = True
PACKAGE_FILES = [
    "config.py",
    "autostart.sh"
]

def main ():
    print ("##### Packager (v%s) => %s #####" % (VERSION, QTILE_PATH))

    if BACKUP:
        dirList = glob.glob("archive/*/")
        largest = 0
        for i in dirList:
            digit = get_digit(i)
            if digit != '':
                if int(digit) > largest:
                    largest = int(digit)
        index = largest + 1
        newDir = "archive/bak.%03i" % (index)
        for i in PACKAGE_FILES:
            out, err = unload_file (i, newDir)
            if err != "":
                print (err)

    for i in PACKAGE_FILES:
        out, err = load_file (i)
        if err != "":
            print (err)


def unload_file (fname, fdir):
    print ("unloading file <%s> into <%s>" % (fname, fdir))
    if not os.path.isdir (fdir):
        run_command ("mkdir %s" % fdir)
    return run_command ("cp %s/%s %s/%s" % (QTILE_PATH, fname, fdir, fname))

def load_file (fname):
    print ("loading file <%s>" % fname)
    return run_command ("cp %s %s/%s" % (fname, QTILE_PATH, fname))

def run_command (cmd, bytes=False):
    output = subprocess.run(cmd.split(' '), capture_output=True)
    if not bytes:
        output.stdout = output.stdout.decode('utf-8')
        output.stderr = output.stderr.decode('utf-8')
    return output.stdout, output.stderr
    
def get_digit(name):
    name = name.strip ('/')
    result = ''
    while name[-1].isdigit():
        result = name[-1] + result
        name = name[:-1]
    print (result)
    return result


if __name__ == '__main__':
    main()