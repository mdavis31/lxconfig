# Commands (Bash)

**KDE Settings Saver:**
    
    $ python -m konsave 
    -l                  #list profiles
    -s <name>           #save profile
    -s <name> -f        #save (overwrite)
    -a <name>           #apply profile
    -i, -e              #import, export (.knsv)

**Fedora Grub Update:**

    #UEFI:
    $ sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg

**Fedora RPM-Fusion Install:**

    # Free releases
    $ sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm 
    
    # Non-free releases
    $ sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
 