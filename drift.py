#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import codecs
import argparse
from jinja2 import Template
from markdown import Markdown

SOURCE_PATH = os.path.abspath(os.path.join('.', 'stardrifter'))
BUILD_PATH = os.path.abspath(os.path.join('.', 'build'))


class MarkdownReader(object):
    file_extensions = ['md', 'markdown', 'mkd']
    extensions = ['extra', 'meta', 'tables']

    def _parse_metadata(self, meta):
        """Return the dict containing document metadata"""
        md = Markdown(extensions=self.extensions)
        output = {}
        for name, value in meta.items():
            name = name.lower()
            if name == "summary":
                summary_values = "\n".join(str(item) for item in value)
                summary = md.convert(summary_values)
                output[name] = summary
            else:
                output[name] = value[0]
        return output

    def read(self, source_path):
        """Parse content and metadata of markdown files"""
        text = codecs.open(source_path, encoding='utf').read()
        md = Markdown(extensions=set(self.extensions + ['meta']))
        content = md.convert(text)

        metadata = self._parse_metadata(md.Meta)
        return content, metadata


def quiet_mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def build():
    reader = MarkdownReader()
    quiet_mkdir(BUILD_PATH)
    template = Template(codecs.open('base.html', encoding='utf').read())
    for filename in os.listdir(SOURCE_PATH):
        base, ext = os.path.splitext(filename)
        if ext == '.md':
            quiet_mkdir(os.path.join(BUILD_PATH, base))
            source = os.path.join(SOURCE_PATH, filename)
            destination = os.path.join(os.path.join(BUILD_PATH, base, 'index.html'))
            body, metadata = reader.read(source)
            metadata.update({'body': body})
            with codecs.open(destination, 'w', encoding='utf-8') as fd:
                fd.write(template.render(metadata))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Build Stardrifter and other tools')
    parser.add_argument('command', choices=['build', 'clean'])
    args = parser.parse_args()
    if args.command == 'build':
        build()
    else:
        sys.exit('todo')
