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
    "Reader for markdown documents"
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
    "HTML Writer, builds documentation"
    def __init__(self, build_path, template):
        self.build_path = build_path
        self.template = template
        quiet_mkdir(self.build_path)

    def write(self, base, data):
        "Write content to the destination path"
        path_prefix = '..'
        quiet_mkdir(os.path.join(self.build_path, base))
        if base != 'intro':
            destination = os.path.join(os.path.join(self.build_path, base, 'index.html'))
        else:
            # special case: intro is the root index
            path_prefix = '.'
            destination = os.path.join(os.path.join(self.build_path, 'index.html'))
        data.update({'path_prefix': path_prefix})
        with codecs.open(destination, 'w', encoding='utf') as fd:
            fd.write(self.template.render(data))


def quiet_mkdir(path):
    "Make dirs without warning"
    try:
        os.makedirs(path)
    except OSError:
        pass


NAVIGATION = (
    ('you', 'You'),
    ('ship', 'Your ship'),
    ('galaxy', 'Galaxy Generator'),
)


def build():
    "Build the documents"
    reader = MarkdownReader()
    writer = HTMLWriter(BUILD_PATH, Template(codecs.open('base.html', encoding='utf').read()))
    for filename in os.listdir(SOURCE_PATH):
        base, ext = os.path.splitext(filename)
        if ext == '.md':
            source = os.path.join(SOURCE_PATH, filename)
            body, metadata = reader.read(source)
            metadata.update({
                'body': body,
                'navigation': NAVIGATION,
                'current': base})
            writer.write(base, metadata)
    # copy the full static files in build
    shutil.rmtree(os.path.join(BUILD_PATH, 'static'))
    shutil.copytree('static', os.path.join(BUILD_PATH, 'static'))


def clean():
    "Clean build directories. Warning! there's no 'undo'."
    if raw_input('Are you sure? [y/N] ').lower() == 'y':
        for item in os.listdir(BUILD_PATH):
            fullpath = os.path.join(BUILD_PATH, item)
            if item.startswith('.'):
                continue
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath, ignore_errors=True)
            else:
                os.unlink(fullpath)


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
