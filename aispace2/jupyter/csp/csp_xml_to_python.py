#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:21:17 2019

@author: zijiazhang
"""


import itertools
import xml.etree.ElementTree as ET
from ast import literal_eval as make_tuple
from string import Template


def findcontain(elem, tag):
    for child in elem:
        if tag in child.tag:
            return child
    return None


def findallcontain(elem, tag):
    temp = []
    for child in elem:
        if tag in child.tag:
            temp.append(child.text.replace(' ', '_'))
    return temp


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def xml_to_python(path):
    tree = ET.parse(path)

    root = tree.getroot()
    CSP = root.find('CSP')

    domains = {}
    positions = {}
    constraints = []
    name = CSP.find('NAME').text.replace(' ', '_')

    for i in CSP:
        if i.tag == 'VARIABLE':
            mytype = i.get('TYPE')
            if(mytype == 'Integer'):
                pass
            elif(mytype == 'String'):
                pass
            elif(mytype == 'Boolean'):
                pass
            varDomain = []
            for e in i:
                if e.tag == 'NAME':
                    varName = e.text
                if e.tag == 'VALUE':
                    if(mytype == 'Integer'):
                        varDomain.append(int(e.text))
                    elif(mytype == 'String'):
                        varDomain.append(e.text)
                    elif(mytype == 'Boolean'):
                        varDomain.append(str2bool(e.text))
                if e.tag == 'PROPERTY':
                    positions[varName] = make_tuple(e.text.split('=')[1][1:])

            domains[varName] = varDomain
        elif i.tag == 'CONSTRAINT':
            if i.get('TYPE') == 'Custom':
                relatedvar = []
                table = []
                for e in i:
                    if e.tag == 'GIVEN':
                        relatedvar.append(e.text)
                    elif e.tag == 'TABLE':
                        table = e.text.split(" ")
                table = ['T' in x for x in table]
                trueTuples = []
                targetlist = [domains[x] for x in relatedvar]
                allTuple = list(itertools.product(*targetlist))
                for i in range(0, len(allTuple)):
                    if table[i]:
                        trueTuples.append(str(allTuple[i]))
                relatedvarName = ["'" + x + "'" for x in relatedvar]
                constraints.append(Template('Constraint(($var),lambda $vNames: ($vNames) in [$true])').substitute(
                    var=','.join(relatedvarName),
                    vNames=','.join(relatedvar),
                    true=','.join(trueTuples)
                ))
            else:
                relatedvar = []
                complement = False
                for e in i:
                    if e.tag == 'GIVEN':
                        relatedvar.append(e.text)
                    elif e.tag == 'ARGS':
                        if e.text != None and 'complement' in e.text:
                            complement = True
                relatedvarName = ["'" + x + "'" for x in relatedvar]
                if complement:
                    constraints.append(Template('Constraint(($var),NOT($function))').substitute(
                        var=','.join(relatedvarName),
                        function=i.get('TYPE')
                    ))
                else:
                    constraints.append(Template('Constraint(($var),$function)').substitute(
                        var=','.join(relatedvarName),
                        function=i.get('TYPE')
                    ))

    template = """$name = CSP(
        domains=$domains,
        constraints=[$constraints],
        positions=$positions)"""

    print(Template(template).substitute(
        name=name,
        domains=domains,
        constraints=', '.join(constraints),
        positions=positions))
