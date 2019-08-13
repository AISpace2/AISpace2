#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 20:13:50 2019

@author: zijiazhang
"""

import xml.etree.ElementTree as ET
tree = ET.parse('/Users/zijiazhang/sample.xml')
root = tree.getroot()
graph = root[0]

result = 'Search_problem_from_explicit_graph(';
nodes = set()
nodemap = {}
start = '';
goal = set();
hmap = {}
Edges = []
positions = {}

for element in graph:
    if(element.tag == 'NODE'):
        name = element.find('NAME').text
        index = element.find('INDEX').text
        nodetype = element.find('TYPE').text
        heuristic = float(element.find('HEURISTICVALUE').text)
        xpos = float(element.find('XPOS').text)
        ypos = float(element.find('YPOS').text)
        positions[name] = (xpos,ypos)
        nodes.add(name);
        nodemap[index] = name;
        hmap[name] = heuristic
        if(nodetype == 'START'):
            start = name
        elif(nodetype == 'GOAL'):
            goal.add(name)
    if(element.tag == 'EDGE'):
        startIndex = element.find('STARTINDEX').text
        endIndex = element.find('ENDINDEX').text
        cost = float(element.find('COST').text)
        temp = 'Arc'
        temp+= str((nodemap[startIndex],nodemap[endIndex],cost))
        Edges.append(temp)


from string import Template

template = """Search_problem_from_explicit_graph(
    nodes=$nodes,
    arcs=[$arcs],
    start=$start,
    goals=$goals,
    hmap=$hmap,
    positions=$positions)"""

print(Template(template).substitute(
        nodes=nodes,
        arcs=', '.join(Edges),
        start=start.__repr__(),
        goals=goal,
        hmap=hmap,
        positions = positions))
#print(result + str(nodes) + str(start) + str(goal) + str(hmap))