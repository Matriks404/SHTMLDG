#!/usr/bin/env python3

import os
import shutil
import sys

from xml.dom import minidom
from yattag import Doc, indent

def get_xml_attribute(source, attribute_name):
    return source.attributes[attribute_name].firstChild.data

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

language = get_xml_element_value(content, 'language');
site_name = get_xml_element_value(content, 'site_name')

stylesheet_name = get_xml_element_value(content, 'stylesheet_name')
stylesheet_filename = 'stylesheets/' + stylesheet_name + '.css'

if not os.path.exists(target_dir):
    os.makedirs(target_dir, exist_ok = True)

if not os.path.exists(target_dir + '/.htmldata'):
    os.makedirs(target_dir + '/.htmldata', exist_ok = True)

shutil.copy(stylesheet_filename, target_dir + '/.htmldata/style.css')

doc.asis("<!DOCTYPE html>")
with tag('html', lang = language):
    with tag('head'):
        with tag('title'):
            text(site_name)
        doc.asis('<meta charset="UTF-8">')
        doc.asis('<link rel="stylesheet" href=".htmldata/style.css">')
    with tag('body'):
        with tag('header'):
          with tag('h1'):
            text(site_name)

        introduction = get_xml_element(content, 'introduction')

        if introduction:
            paras = get_xml_elements_values(introduction, 'text')

            if paras:
                with tag('section', id = 'introduction'):
                    with tag('h2'):
                        text('Introduction')

                    for p in paras:
                        with tag('p'):
                            doc.asis(p)

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
                statuses = {'Complete': '✔️', 'Incomplete': '🛠️', 'Errors': '⚠️', 'Not Started': '🚫'}

                for c in categories:
                    name = get_xml_attribute(c, 'name')
                    id = get_xml_attribute(c, 'id')

                    with tag('div', id = id):
                        with tag('h3'):
                            text(name)

                        entries = get_xml_elements(c, 'entry')

                        if entries:
                            with tag('table'):
                                for e in entries:
                                    name = get_xml_element_value(e, 'name')
                                    filename = get_xml_element_value(e, 'filename')
                                    status = get_xml_element_value(e, 'status')
                                    completeness = get_xml_element_value(e, 'completeness')

                                    with tag('tr'):
                                        with tag('td'):
                                            text(statuses[status]) #temp
                                        with tag('td'):
                                            text(completeness)
                                        with tag('td'):
                                            with tag('a', href = '.htmldata/pages/' + id + '/' + filename + '.html'):
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