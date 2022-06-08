# keepass-tools

My collections of tools around keepass - in python

## pass_to_keepass.py

A tool to export a [pass](https://www.passwordstore.org/) database to a keepass 
database

```bash
./pass_to_keepass.py --help
usage: pass_to_keepass [-h] [-o OUTPUT] [-p PASSWORD] [-n NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        the KEEPASS database to generate, 'keepass.kdbx' by default
  -p PASSWORD, --password PASSWORD
                        The keepass password name in the pass database, 'keepass' by default
  -n NUMBER, --number NUMBER
                        The max number of password to export
```

