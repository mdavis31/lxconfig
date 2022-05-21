import os

PATH = "/home/michael/Downloads/"
GPG_KEYRINGS = {
    'manjaro': 'gitlab.manjaro.org/packages/core/manjaro-keyring/-/raw/master/manjaro.gpg'
}

def main ():
    print ("*** PYTHON ISO VERIFICATION ***\n")

    isoList = searchDirectory (PATH)
    for index, i in enumerate (isoList):
        print (f"({index+1}) {i}")
    inp = int (input ("Select the ISO from above: "))
    iso = isoList[inp-1]
    print ()

    print ("(1) SHA1, (2) SHA256, (3) SHA512, (4) MD5")
    inp = int (input ("Select the correct algorithm from above: "))
    algoType = "md5sum" if inp == 4 else ("sha512sum" if inp == 3 else "sha256sum" if inp == 2 else "sha1sum")

    print ()

    algo = input (f"Copy and Paste the {algoType}: ")

    print ()

    gpg = iso + ".sig"
    inp = input (f"Enter the filename of the GPG (default {gpg}): ")
    if inp != '':
        gpg = inp

    # import all the keyrings
    print (os.popen ("gpg --keyserver keyserver.ubuntu.com --search-keys Manjaro Build Server"))
    print (os.popen ("gpg --keyserver hkps://keys.openpgp.org --recv-keys 003DB8B0CB23504F"))

    
    isoFull = f"{PATH}/{iso}"
    gpgFull = f"{PATH}/{gpg}"
    isoCheck = False
    gpgCheck = False

    print ("\nChecking ISO against the algorithm...")
    sys = os.popen(f"{algoType} -b {PATH}/{iso}").read()
    print (sys)
    if sys.startswith(algo):
        print ("SUCCESS!")
        isoCheck = True
    else:
        print ("FAILED!")
    

    print ("Verifying the GPG signature...")
    sys = os.popen(f"gpg --verify {gpgFull} {isoFull}").read()
    #print (sys, str (sys).find ("Good"))
    #if sys.find("Good signature") != -1:
    #    print ("sdasd")
    #    print ("SUCCESS!")



def searchDirectory (path):
    isoList = []
    for file in os.listdir(path):
        if file.endswith(".iso"):
            isoList.append (str (file))
    return isoList

if __name__ == '__main__':
    main()