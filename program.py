#!/usr/bin/env python3

import os
import shutil
import sys

from xml.dom import minidom
from yattag import Doc, indent

def get_xml_attribute(source, attribute_name):
    if source.hasAttribute(attribute_name):
        return source.attributes[attribute_name].firstChild.data
    else:
        return None

def get_xml_elements(source, tag_name):
    return source.getElementsByTagName(tag_name)

def get_xml_element(source, tag_name):
    el = source.getElementsByTagName(tag_name)

    return el[0] if el else None

def get_xml_element_value(source, tag_name):
    return source.getElementsByTagName(tag_name)[0].firstChild.data

def get_xml_elements_values(source, tag_name):
    els = source.getElementsByTagName(tag_name)

    texts = []

    for el in els:
        texts.append(el.firstChild.data)

    return texts

if len(sys.argv) == 1 or len(sys.argv) > 3:
    print('Wrong number of parameters! For usage help, use \'./program.py -h\'')

    sys.exit()

if len(sys.argv) == 2:
    if sys.argv[1] == '-h':
        print('The proper usage is: \'./program.py <source> <target>\'')
        print()
        print('For example: \'./program.py ./examples/example_documentation ./site\'')
    else:
        print('Not enough parameters! For usage help, use \'./program.py -h\'')

    sys.exit()

source_dir = sys.argv[1]

if source_dir[-1] == '/':
    source_dir = source_dir[:-1]

target_dir = sys.argv[2]

if target_dir[-1] == '/':
    target_dir = target_dir[:-1]

xml = minidom.parse(source_dir + '/main.xml')
content = get_xml_element(xml, 'content')

doc, tag, text = Doc().tagtext()

language = get_xml_element_value(content, 'language')
site_name = get_xml_element_value(content, 'site_name')

target_htmldata_dir = target_dir + '/.htmldata'

stylesheet_name = get_xml_element_value(content, 'stylesheet_name')
source_stylesheet_path = 'stylesheets/' + stylesheet_name + '.css'
target_stylesheet_path = target_htmldata_dir + '/style.css'

source_content_dir = source_dir + '/content'
target_content_dir = target_htmldata_dir + '/content'

if not os.path.exists(target_dir):
    os.makedirs(target_dir, exist_ok = True)

if not os.path.exists(target_htmldata_dir):
    os.makedirs(target_htmldata_dir, exist_ok = True)

shutil.copy(source_stylesheet_path, target_stylesheet_path)

doc.asis('<!DOCTYPE html>')
with tag('html', lang = language):
    with tag('head'):
        with tag('title'):
            text(site_name)
        doc.asis('<meta charset="UTF-8">')
        doc.asis('<meta name="viewport" content="height=device-width, initial-scale=0.9">')
        doc.asis('<link rel="stylesheet" href=".htmldata/style.css">')
    with tag('body'):
        with tag('header'):
          with tag('h1'):
            text(site_name)

        introduction = get_xml_element(content, 'introduction')

        if introduction:
            with tag('section', id = 'introduction'):
                with tag('h2'):
                    text('Introduction')

            is_auto = get_xml_attribute(introduction, 'auto') == 'true'

            if is_auto:
                introduction_path = source_content_dir + '/introduction.html'

                if os.path.exists(introduction_path):
                    file = open(introduction_path, 'r', encoding='utf-8')
                    data = file.read()

                    if data:
                        doc.asis(data)
                    else:
                        text('No introduction text found!')
                else:
                    text('No introduction text found!')

            else:
                paras = get_xml_elements_values(introduction, 'p')

                if paras:
                    for p in paras:
                        with tag('p'):
                            doc.asis(p)
                else:
                    text('No introduction text found!')

        with tag('section', id = 'legend'):
            with tag('h2'):
                text('Legend')

            with tag('ul'):
                legend = ['✔️ — Guide complete',
                          '🛠️ — Guide incomplete',
                          '⚠️ — Guide contains errors',
                          '🚫 — Guide not started yet']

                for s in legend:
                    with tag('li'):
                        text(s)

        with tag('main', id = 'guides'):
            with tag('h2'):
                text('Guides')

            guides = get_xml_element(content, 'guides')

            if guides:
                categories = get_xml_elements(guides, 'category')

            if guides and categories:
                statuses = {'Complete': '✔️', 'Incomplete': '🛠️', 'With errors': '⚠️', 'Not started': '🚫'}

                for c in categories:
                    name = get_xml_attribute(c, 'name')
                    category_id = get_xml_attribute(c, 'id')

                    with tag('div', id = category_id):
                        with tag('h3'):
                            text(name)

                        entries = get_xml_elements(c, 'entry')

                        if entries:
                            with tag('table'):
                                for e in entries:
                                    name = get_xml_attribute(e, 'name')
                                    entry_id = get_xml_attribute(e, 'id')
                                    status = get_xml_attribute(e, 'status')
                                    completeness = get_xml_attribute(e, 'completeness')

                                    with tag('tr'):
                                        with tag('td'):
                                            text(statuses[status])
                                        with tag('td'):
                                            text(completeness)
                                        with tag('td'):
                                            if status == 'Not started' or completeness == '0%':
                                                href = '#';
                                            else:
                                                href = '.htmldata/pages/' + category_id + '/' + entry_id + '.html'

                                            with tag('a', href = href):
                                                text(name)
                        else:
                            with tag('p'):
                                text('There are no guide entries!')
            else:
                with tag('p'):
                    text('There are no guide categories!')


result = indent(doc.getvalue())

file = open(target_dir + '/index.html', 'w', encoding='utf-8')
file.write(result)