#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import shutil
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
        md = Markdown(extensions=self.extensions)
        content = md.convert(text)

        metadata = self._parse_metadata(md.Meta)
        return content, metadata


class HTMLWriter(object):
    def __init__(self, build_path, template):
        self.build_path = build_path
        self.template = template
        quiet_mkdir(self.build_path)

    def write(self, base, data):
        quiet_mkdir(os.path.join(self.build_path, base))
        destination = os.path.join(os.path.join(self.build_path, base, 'index.html'))
        with codecs.open(destination, 'w', encoding='utf') as fd:
            fd.write(self.template.render(data))


def quiet_mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def build():
    reader = MarkdownReader()
    writer = HTMLWriter(BUILD_PATH, Template(codecs.open('base.html', encoding='utf').read()))
    for filename in os.listdir(SOURCE_PATH):
        base, ext = os.path.splitext(filename)
        if ext == '.md':
            source = os.path.join(SOURCE_PATH, filename)
            body, metadata = reader.read(source)
            metadata.update({'body': body})
            writer.write(base, metadata)


def clean():
    if raw_input('Are you sure? [y/N] ').lower() == 'y':
        shutil.rmtree(BUILD_PATH, ignore_errors=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Build Stardrifter and other tools')
    parser.add_argument('command', choices=['build', 'clean'])
    args = parser.parse_args()
    if args.command == 'build':
        build()
    elif args.command == 'clean':
        clean()
    else:
        sys.exit('todo')
