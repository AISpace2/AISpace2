#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 12:21:09 2019

@author: zijiazhang
"""

import xml.etree.ElementTree as ET
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
            temp.append(child.text)
    return temp


def XML_to_Python(path):
    try:
        tree = ET.parse(path)
    except:
        print('Error Reading Files')
        return
    root = tree.getroot()

    for ch in root:
        if 'NETWORK' in ch.tag:
            prob = ch
    names = set()
    domain = {}
    probTable = {}
    givenTable = {}
    for element in prob:
        if 'NAME' in element.tag:
            probname = findcontain(prob, 'NAME').text.replace(' ', '_')
        elif 'VARIABLE' in element.tag:
            temp = findallcontain(element, 'OUTCOME')
            name = findcontain(element, 'NAME').text.lower().capitalize()
            names.add(name)
            domain[name] = temp
        elif 'DEFINITION' in element.tag:
            name = findcontain(element, 'FOR').text.lower().capitalize()
            given = findallcontain(element, 'GIVEN')
            probs = findcontain(element, 'TABLE').text
            probTable[name] = probs.split(' ')
            givenTable[name] = given

    domainNames = []
    domains = []
    for i in names:
        t = (i, domain[i])
        temp = i + " = Variable" + str(t)
        domains.append(temp)
        domainNames.append(i)

    factorNames = []
    factors = []
    for i in names:
        probability = '[' + ','.join(probTable[i]) + ']'
        given = '[' + ','.join(givenTable[i]) + ']'
        factor = "f_" + i.lower() + " = Prob(" + i + "," + given + "," + probability + ")"
        factors.append(factor)
        factorNames.append("f_" + i)

    template = '\n'.join(domains) + " \n" + "\n".join(factors) + "\n" + probname + """ = Belief_network(
        vars=[$vars],
        factors=[$probs],
        positions=$positions)"""

    print(Template(template).substitute(
        vars=','.join(domainNames),
        probs=',' .join(factorNames),
        positions=[]))
