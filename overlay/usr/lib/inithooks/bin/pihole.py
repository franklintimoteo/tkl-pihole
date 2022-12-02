#!/usr/bin/python3
"""Reconfigure defaults configs Pi-hole and set admin password

Option:
    --pass=     unless provided, will ask interactively
"""

import sys
import getopt
import subprocess
from subprocess import call

from libinithooks.dialog_wrapper import Dialog


def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                        ['help', 'pass='])
    except getopt.GetoptError as e:
        usage(e)
    
    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val

    if not password:
        d = Dialog('TurnKey GNU/Linux - First boot configuration')
        password = d.get_password(
            "Pi-hole password",
            "Enter new for the Pi-hole 'admin' account")
    
    call(['pihole', '-a', '-p', password])

    basicinstall="/etc/.pihole/automated install/basic-install.sh"
    call(['sed', '-ri', '/  "\$\{opt1a\}"  "\$\{opt1b\}" ./d', basicinstall])
    call(['pihole', 'reconfigure'])
    call(['git', 'checkout', basicinstall])

if __name__ == "__main__":
    main()
