import xbmc,xbmcvfs
from xml.dom import minidom
import utils as utils

class AdvancedSettings:
    as_file = xbmc.translatePath('special://home/userdata/advancedsettings.xml')
    doc = None
    
    def __init__(self):

        #read in the file, or make a blank one if it doesn't exist            
        if(xbmcvfs.exists(self.as_file)):
            self.doc = minidom.parse(self.as_file)
        else:
            self.doc.minidom.Document()
            topNode = self.doc.createElement('advancedsettings')
            self.doc.appendchild(topNode)

    def listNodes(self,aNode = None):
        result = []
        
        if(aNode == None):
            #use the root node
            result = self.__parseNodes(self.doc.documentElement)
        else:
            result = self.__parseNodes(self.doc.getElementsByTagName(aNode)[0])
            
        return result
                

    def getNode(self,parent,node):
        if(parent == ''):
            parent = None

        #get the top level node
        nodeList = self.listNodes(parent)
        foundNode = None
        
        for aNode in nodeList:
            if(aNode.name == node):
                foundNode = aNode

        return foundNode

    def renameNode(self,node,newName):
        #get the node from the dom
        xmlNode = None

        #get the child
        childNode = self.doc.documentElement.getElementsByTagName(node.name)[0]

        childNode.tagName = newName

        self.writeFile()

    def updateValue(self,node,newValue):
        #get the node from the dom
        xmlNode = None

        #get the child
        childNode = self.doc.documentElement.getElementsByTagName(node.name)[0]

        childNode.firstChild.nodeValue = newValue

        self.writeFile()

    def writeFile(self):
        file = xbmcvfs.File(self.as_file,'w')
        file.write(str(self.doc.toxml()))
        file.close()

    def __parseNodes(self,nodeList):
        result = []

        for node in nodeList.childNodes:
            if(node.nodeType == self.doc.ELEMENT_NODE):
                aSetting = SettingNode(node.nodeName)

                if(len(node.childNodes) > 1):
                    aSetting.hasChildren = True
                else:
                    aSetting.value = node.childNodes[0].nodeValue
                    aSetting.parent = node.parentNode.nodeName
                
                result.append(aSetting)
        return result

class SettingNode:
    name = ''
    value = ''
    hasChildren = False
    parent = ''
    
    def __init__(self,name):
        self.name = name
