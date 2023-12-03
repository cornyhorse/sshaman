import sys

from cli import sshaman_cli
from tui import tree

if __name__ == '__main__':
    if len(sys.argv) == 1:
        tree.main()
    else:
        sshaman_cli.cli()
