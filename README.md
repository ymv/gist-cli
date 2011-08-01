Gist-cli is a small python module, and a command line client for making gists.  It works from a list of files, or from stdin.

To Install:

    # Not yet on pypi
    git clone http://github.com/mikelietz/gist-cli.git
    cd gist-cli
    python setup.py install

To Use:

    $ mkgist README.md
    $ # on a mac, this will replace the contents of your clipboard with the
    $ # gist url
    $ pbpaste | mkgist | pbcopy
    $ # a whole folder, or really any list of files can be sent.
    $ cd ~/path/to/stuff/to/share
    $ mkgist *
    $ # private gists
    $ pbpaste | mkgist -p
    $ # From stdin interactively
    $ mkgist
    O HAI!
    (ctrl+d to send EOF)
    $ 
    
    

This expects to find the following block in ~/.gitconfig to post via your account:

```
[github]
user = <your username>
password = <your password>
```

Note also that if your existing .gitconfig has tabs in there, you'll need to strip those out.

This can take a list of files, or can accept input from stdin and creates a gist (and prints the url)

Other options:

    usage: gist [-h] [--description DESCRIPTION] [--private]
                [infile_list [infile_list ...]]

    Create a github gist from a file, or from stdin

    positional arguments:
      infile_list - Not Required, if ommitted, will accept from stdin

    optional arguments:
      -h, --help            show this help message and exit
      --description DESCRIPTION, -d DESCRIPTION
      --private, -p

if you run setup.py, it will install the mkgist binary.
