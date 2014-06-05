#!/usr/bin/env python
#-*- coding:utf-8 -*-

from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='sqlite:///migration/cogenda-app.db', debug='False', repository='migration')
