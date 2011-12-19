# -*- coding: utf-8 -*-
from netzob.Common.TypeConvertor import TypeConvertor

#+---------------------------------------------------------------------------+
#|         01001110 01100101 01110100 01111010 01101111 01100010             | 
#+---------------------------------------------------------------------------+
#| NETwork protocol modeliZatiOn By reverse engineering                      |
#| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
#| @license      : GNU GPL v3                                                |
#| @copyright    : Georges Bossert and Frederic Guihery                      |
#| @url          : http://code.google.com/p/netzob/                          |
#| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
#| @author       : {gbt,fgy}@amossys.fr                                      |
#| @organization : Amossys, http://www.amossys.fr                            |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+ 
#| Standard library imports
#+---------------------------------------------------------------------------+
import re
from lxml.etree import ElementTree
from lxml import etree

#+---------------------------------------------------------------------------+
#| Local Imports
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Field :
#|     Class definition of a field
#| @author     : {gbt,fgy}@amossys.fr
#| @version    : 0.2
#+---------------------------------------------------------------------------+
class Field(object):
    
    #+-----------------------------------------------------------------------+
    #| Constructor
    #+-----------------------------------------------------------------------+
    def __init__(self, name, encapsulation_level, index, regex, selected_type, description="", color="black"):
        self.name = name
        self.encapsulation_level = encapsulation_level
        self.index = index
        self.regex = regex
        self.selected_type = selected_type
        self.description = description
        self.color = color
    
    def getEncodedVersionOfTheRegex(self):
        return TypeConvertor.encodeNetzobRawToGivenType(self.regex, self.selected_type)  
    
    def isRegexStatic(self):
        if self.regex.find("{") == -1:
            return True
        else:
            return False
    def isRegexOnlyDynamic(self):
        if re.match("\(\.\{\d?,\d+\}\)", self.regex) != None:
            return True
        else:
            return False    
        
    
    
    def getName(self):
        return self.name
    def getEncapsulationLevel(self):
        return self.encapsulation_level
    def getRegex(self):
        return self.regex
    def getSelectedType(self):
        return self.selected_type
    def getDescription(self):
        return self.description
    def getColor(self):
        return self.color
    def getIndex(self):
        return self.index
    
    def setName(self, name):
        self.name = name
    def setEncapsulationLevel(self, level):
        self.encapsulation_level = level
    def setRegex(self, regex):
        self.regex = regex
    def setSelectedType(self, type):
        self.selected_type = type
    def setDescription(self, description):
        self.description = description
    def setColor(self, color):
        self.color = color
    def setIndex(self, index):
        self.index = index
    
    
    def save(self, root, namespace):
        xmlField = etree.SubElement(root, "{" + namespace + "}field")
        xmlField.set("name", str(self.getName()))
        xmlField.set("encapsulation_level", str(self.getEncapsulationLevel()))
        xmlField.set("index", str(self.getIndex()))
        
        xmlFieldRegex = etree.SubElement(xmlField, "{" + namespace + "}regex")
        xmlFieldRegex.text = str(self.getRegex())
        
        xmlFieldRegex = etree.SubElement(xmlField, "{" + namespace + "}selectedType")
        xmlFieldRegex.text = str(self.getSelectedType())
        
        xmlFieldRegex = etree.SubElement(xmlField, "{" + namespace + "}description")
        xmlFieldRegex.text = str(self.getDescription())
        
        xmlFieldRegex = etree.SubElement(xmlField, "{" + namespace + "}color")
        xmlFieldRegex.text = str(self.getColor())
    
    @staticmethod
    def createDefaultField():
        return Field("Default", 0, 0, "(.{,})", "binary")
    
    @staticmethod
    def loadFromXML(xmlRoot, namespace, version):
        if version == "0.1" :
            field_name = xmlRoot.get("name")
            field_encapsulation_level = int(xmlRoot.get("encapsulation_level"))
            field_index = int(xmlRoot.get("index"))
            
            field_regex = xmlRoot.find("{" + namespace + "}regex").text
            field_selectedType = xmlRoot.find("{" + namespace + "}selectedType").text
            
            field = Field(field_name, field_encapsulation_level, field_index, field_regex, field_selectedType)
            
            if xmlRoot.find("{" + namespace + "}description") != None :
                field_description = xmlRoot.find("{" + namespace + "}description").text
                field.setDescription(field_description)
            
            if xmlRoot.find("{" + namespace + "}color") != None :
                field_color = xmlRoot.find("{" + namespace + "}color").text
                field.setColor(field_color)
            
            return field
            
        return None
        
        
        
        
