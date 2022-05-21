import os, subprocess

def main ():

    def accept_yesno_y (inp):
        if inp.upper() in ['Y', 'YES', 'YE', 'YEAH' 'YUP'] or inp == "":
            return 0, 'yes'
        elif inp.upper() in ['N', 'NO', 'NAH', 'NOPE']:
            return 0, 'no'
        else:
            return -1, "Wrong choice, please choose (Y/n)"

    def accept_yesno_n (inp):
        if inp.upper() in ['Y', 'YES', 'YE', 'YEAH' 'YUP']:
            return 0, 'yes'
        elif inp.upper() in ['N', 'NO', 'NAH', 'NOPE'] or inp == "":
            return 0, 'no'
        else:
            return -1, "Wrong choice, please choose (y/N)"
            

    rc, val = prompt ("Select a choice (Y/n)", accept_yesno_n)
    if val == 'yes':
        print "Okay, running code.."
    

    print (rc, data)

def prompt(prompt, accepted_method):
    rc = None
    while rc == None:
        inp = input(prompt + "=> ")
        rc = accepted_method(inp.strip())
    return rc


def run_command (cmd, bytes=False):
    output = subprocess.run(cmd.split(' '), capture_output=True)
    if not bytes:
        output.stdout = output.stdout.decode('utf-8')
        output.stderr = output.stderr.decode('utf-8')
    return output.stdout, output.stderr


if __name__ == '__main__':
    main()