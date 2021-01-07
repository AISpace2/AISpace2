#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:33:52 2019

@author: zijiazhang
"""
import re
import xml.etree.ElementTree as ET
from string import Template
def xml_to_python(path):
    f = open(path)
    data = f.read()
    """
    Fix Syntax Error in the XML File
    """
    while True:
        search = re.search('TYPE=([^"^>]*)>',data,re.IGNORECASE)
        if not search:
            break;
        matched_String = search.group(1)
        total_String = search.group(0)
        data = data.replace(total_String, 'TYPE="'+matched_String+'">')
    
    data = data.replace('<?xml VERSION="0.01" ?>','<?xml version="1.0" ?>')
    
    """
    Parse XML File
    """
    root = ET.fromstring(data)
    
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")
    
    """
    String Templates
    """
    STRIPSTEMPLATE = '"$name":Strips($preCondition,$effect)'
    DOMAIN_TEMPLATE = 'STRIPS_domain($variables,{$strips})'
    PROBLEM_TEMPLATE = """from aipython.stripsProblem import Planning_problem, STRIPS_domain, Strips
planning = Planning_problem($Domain,$Start,$Goal,positions = $position)"""
    
    
    VariableIDNameMap ={}
    VariablesDomain = {}
    Positions = {}
    Strips = []
    
    for sub in root:
        if sub.tag == 'VARIABLES':
            variables = sub
        elif sub.tag == 'ACTIONS':
            actions = sub
        elif sub.tag == 'STATES':
            states = sub
    """
    Parse Variables
    """
    for var in variables:
        varType =  var.get('TYPE')
        varID = int(var.find('ID').text);
        varName =var.find('NAME').text;
        varPosition = (float(var.find('POSITION').find('XPOS').text),
                       float(var.find('POSITION').find('YPOS').text))
        varValues = []
        values = var.findall('VALUE')
        for value in values:
            if varType == 'Boolean':
                varValues.append(str2bool(value.text))
            elif varType == 'Integer':
                varValues.append(int(value.text))
            elif varType == 'String':
                varValues.append(value.text)
        VariablesDomain[varName] = set(varValues)
        VariableIDNameMap[varID] = (varName,varType)
        Positions[varName] = varPosition
    
    """
    Parse Strips
    """
    
    for action in actions:
        actName = action.find('NAME').text
        actPosition = (float(var.find('POSITION').find('XPOS').text),
                       float(var.find('POSITION').find('YPOS').text))
        preCoditions = action.find('PRECONDITIONS')
        postConsitions = action.find('POSTCONDITIONS')
        preCondition = {}
        postCondition = {}
        for pair in preCoditions:
            variableID = int(pair.find('VARIABLE_ID').text)
            varValue = pair.find('VALUE').text
            varName, varType = VariableIDNameMap[variableID]
            if varType == 'Boolean':
                varValue=str2bool(varValue)
            elif varType == 'Integer':
                varValue=int(varValue)
            preCondition[varName] = varValue
        for pair in postConsitions:
            variableID = int(pair.find('VARIABLE_ID').text)
            varValue = pair.find('VALUE').text
            varName, varType = VariableIDNameMap[variableID]
            if varType == 'Boolean':
                varValue=str2bool(varValue)
            elif varType == 'Integer':
                varValue=int(varValue)
            postCondition[varName] = varValue
        actionString = Template(STRIPSTEMPLATE).substitute(
                name = actName,
                preCondition = preCondition,
                effect = postCondition
                )
        Strips.append(actionString)
        Positions['action'] = actPosition
    
    """
    Parse States
    """
    
    for state in states:
        stateType = state.find('TYPE').text
        variables = state.findall('PAIR')
        s = {}
        for pair in variables:
            variableID = int(pair.find('VARIABLE_ID').text)
            varValue = pair.find('VALUE').text
            varName, varType = VariableIDNameMap[variableID]
            if not varValue == '  ---  ':
                if varType == 'Boolean':
                    varValue=str2bool(varValue)
                elif varType == 'Integer':
                    varValue=int(varValue)
                s[varName] = varValue
        if stateType == 'START':
            startState = s
        if stateType == 'GOAL':
            goalState = s
    
    
    
    domain = Template (DOMAIN_TEMPLATE).substitute(
            variables = VariablesDomain,
            strips = ','.join(Strips))
    
    
   
    
    problem = Template(PROBLEM_TEMPLATE).substitute(
            Domain = domain,
            Start = startState,
            Goal = goalState,
            position = Positions
            )
    print(problem)
    
