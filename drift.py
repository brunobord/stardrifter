#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""Stardrifter building document script.

This script builds HTML documents out of the Markdown files and stores them in
the `build` directory.

Usage:

    python drift.py build

You can cleanup the `build` directory by using the "clean" command, too.

    :license: BSD, see LICENSE for details
    :copyright: 2013 by Bruno Bord
"""
import os
import sys
import shutil
import codecs
import datetime
import logging
import argparse
from jinja2 import Template
from markdown import Markdown

SOURCE_PATH = os.path.abspath(os.path.join('.', 'stardrifter'))
BUILD_PATH = os.path.abspath(os.path.join('.', 'build'))
STATIC_PATH = os.path.join(BUILD_PATH, 'static')
VENDOR_PATH = os.path.join(BUILD_PATH, 'vendor')

now = datetime.datetime.now()


class MarkdownReader(object):
    "Reader for markdown documents"
    file_extensions = ['md', 'markdown', 'mkd']
    extensions = ['extra', 'meta', 'tables', 'toc', 'admonition']

    def __init__(self, fragment_path):
        self.fragments = {}
        for filename in os.listdir(fragment_path):
            logging.debug("Fragment: %s" % filename)
            if filename.endswith('.md'):
                self.fragments[filename] = codecs.open(os.path.join(fragment_path, filename), encoding='utf').read()

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
        for key in self.fragments:
            text = text.replace("~~%s~~" % key, self.fragments[key])
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
        data.update({
            'path_prefix': path_prefix,
            'date': now.strftime("%a, %d %b %Y %H:%M")
        })
        with codecs.open(destination, 'w', encoding='utf') as fd:
            fd.write(self.template.render(data))


def quiet_mkdir(path):
    "Make dirs without warning"
    try:
        os.makedirs(path)
    except OSError:
        pass


NAVIGATION = (
    {'caption': 'Prepare'},
    {'url': "quickstart", 'caption': 'Quickstart'},
    {'url': 'you', 'caption': 'Your character'},
    {'url': 'ship', 'caption': 'Your ship'},
    {'caption': 'Play'},
    {'url': 'adventure', 'caption': 'Adventure', 'children': (
        {'url': 'marketplace', 'caption': 'Marketplace'},
        {'url': 'travel', 'caption': 'Space Travel'},
    )},
    {'url': 'galaxy', 'caption': 'Galaxy Generator'},
    {'url': 'advanced', 'caption': 'Advanced play'},
    {'url': "credits", 'caption': "Credits"},
)


def build():
    "Build the documents"
    logging.info('Start building')
    reader = MarkdownReader(os.path.join(SOURCE_PATH, 'fragments'))
    writer = HTMLWriter(BUILD_PATH, Template(codecs.open('templates/base.html', encoding='utf').read()))
    for filename in os.listdir(SOURCE_PATH):
        base, ext = os.path.splitext(filename)
        if ext == '.md':
            source = os.path.join(SOURCE_PATH, filename)
            body, metadata = reader.read(source)
            metadata.update({
                'body': body,
                'navigation': NAVIGATION,
                'current': base})
            logging.info('Writing %s' % base)
            writer.write(base, metadata)
    # copy the full static files in build
    if os.path.exists(STATIC_PATH):
        shutil.rmtree(STATIC_PATH)
    if os.path.exists(VENDOR_PATH):
        shutil.rmtree(VENDOR_PATH)
    logging.info('Copying static files')
    shutil.copytree('static', STATIC_PATH)
    shutil.copytree('vendor', VENDOR_PATH)
    logging.info("Done")


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
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.command == 'build':
        build()
    elif args.command == 'clean':
        clean()
    else:
        sys.exit('todo')
