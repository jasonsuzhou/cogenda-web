#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='sqlite:///migration/cogenda-app.db', debug='False', repository='migration')
