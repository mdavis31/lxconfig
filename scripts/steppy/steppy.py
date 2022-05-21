import os, subprocess

def accept_yesno (inp):
    if inp.upper() in ['Y', 'YES', 'YE', 'YEAH' 'YUP']:
        return 0, 'yes'
    elif inp.upper() in ['N', 'NO', 'NAH', 'NOPE']:
        return 0, 'no'
    else:
        return -1, "wrong choice"

def accept_yesno_y (inp):
    inp = inp if inp != "" else "Y"
    return accept_yesno(inp)

def accept_yesno_n (inp):
    inp = inp if inp != "" else "N"
    return accept_yesno(inp)

def main ():

    git_email = "mdavis@parrsridge.com"
    git_name = "Michael Davis"

    rc, val = prompt ("Would you like to load the following git info (Y/n)?\n  %s - %s" % (git_name, git_email), accept_yesno)
    if val == 'yes':
        print (run_command (f'git config --global user.email "{git_email}"'))
        print (run_command (f'git config --global user.name "{git_name}"'))
    

    #print (run_command (f'ssh-keygen -t ed25519 -C "{git_email}"'))
    #print (run_command (f'sudo ssh-add ~/.ssh/id_ed25519'))
    
    print (rc, val)

def prompt(prompt, accepted_method):
    rc = -1
    while rc == -1:
        inp = input(prompt + " => ")
        rc, val = accepted_method(inp.strip())
    return rc, val


def run_command (cmd, bytes=False):
    output = subprocess.run(cmd.split(' '), capture_output=True)
    if not bytes:
        output.stdout = output.stdout.decode('utf-8')
        output.stderr = output.stderr.decode('utf-8')
    return output.stdout, output.stderr


if __name__ == '__main__':
    main()