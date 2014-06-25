# -*- coding: utf-8 -*-

"""
Jinja2 extensions for use Markdown in templates.
"""

import jinja2
import jinja2.ext
import markdown2


class Markdown2Extension(jinja2.ext.Extension):
    tags = set(['markdown2'])

    def __init__(self, environment):
        super(Markdown2Extension, self).__init__(environment)
        environment.extend(markdowner=markdown2.Markdown()) 


    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmarkdown2'],
            drop_needle=True
        )
        return jinja2.nodes.CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body
        ).set_lineno(lineno)


    def _markdown_support(self, caller):
        print self.environment.markdowner.convert(caller()).strip()
        return self.environment.markdowner.convert(caller()).strip()