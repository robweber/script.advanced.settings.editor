import xbmc,xbmcgui,xbmcplugin
import urlparse
import sys
from resources.lib.advancedsettings import AdvancedSettings,SettingNode
import resources.lib.utils as utils

def get_params():
   param = {}

   if(len(sys.argv) > 1):
      for i in sys.argv:
         args = i
         if(args.startswith('?')):
            args = args[1:]
         
         param.update(dict(urlparse.parse_qsl(args)))

   if("node" not in param):
      param['node'] = None

   if("command" not in param):
      param['command'] = 0

   if('parent' not in param):
      param['parent'] = ''

   return param

class EditorGUI:
   params = None
   as_file = AdvancedSettings()
   
   def __init__(self,params):
      self.params = params

   def shouldRun(self):
      result = True
      
      #check if file exists
      if(not self.as_file.exists()):

         #as if the user would like to create one
         confirm = xbmcgui.Dialog().yesno(utils.getString(30023),utils.getString(30024))

         if(confirm):
            self.as_file.createFile()
         else:
            #don't continue
            result = False

      return result

   def showGUI(self):
      context_url = "%s?%s"
       
      #list the nodes
      command = int(self.params['command'])
      if(command == 0):
         topLevel = self.as_file.listNodes(self.params['node'])
         
         for node in topLevel:
            utils.log(node.name + " " + str(node.hasChildren))
            if(node.hasChildren):
               #if this is a top level node of a larger set
               item = xbmcgui.ListItem(str(node.name),"")
               item.addContextMenuItems([(utils.getString(30001),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=5&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30002),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=6&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30004),'Xbmc.RunPlugin(%s?%s)' % (sys.argv[0],"command=4&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30005),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=2&node=" + node.name + "&parent=" + node.parent))])
               ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=context_url % (sys.argv[0],"command=0&node=" + node.name),listitem=item,isFolder=True)
            else:
               #if this is an item with a value
               item = xbmcgui.ListItem(str(node.name),"")
               item.addContextMenuItems([(utils.getString(30001),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=5&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30002),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=6&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30003),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=3&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30004),'Xbmc.RunPlugin(%s?%s)' % (sys.argv[0],"command=4&node=" + node.name + "&parent=" + node.parent)),(utils.getString(30005),"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=2&node=" + node.name + "&parent=" + node.parent))])

               ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=context_url % (sys.argv[0],"command=1&node=" + node.name + "&parent=" + node.parent),listitem=item,isFolder=False)

         #if no elements (blank) create a link to start the first one
         if(len(topLevel) == 0):
            item = xbmcgui.ListItem(utils.getString(30001),"")
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=context_url % (sys.argv[0],"command=6&node=advancedsettings&parent="),listitem=item,isFolder=False)


         xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
         
      elif(command == 1):
         #show information about the currently selected node
         selectedNode = self.as_file.getNode(self.params['parent'],self.params['node'])

         xbmcgui.Dialog().ok(selectedNode.name,utils.getString(30006) + ": " + selectedNode.value)

      elif(command == 2):
         #rename selected node
         selectedNode = self.as_file.getNode(self.params['parent'],self.params['node'])
         
         newName = xbmcgui.Dialog().input(utils.getString(30005) + ' ' + selectedNode.name)

         self.as_file.renameNode(selectedNode,newName)

         #refresh the view
         xbmc.executebuiltin('Container.Refresh')

      elif(command == 3):
         #change the selected node value
         selectedNode = self.as_file.getNode(self.params['parent'],self.params['node'])
         
         newValue = xbmcgui.Dialog().input('New Value ' + selectedNode.name)

         self.as_file.updateValue(selectedNode,newValue)

         #refresh the view
         xbmc.executebuiltin('Container.Refresh')

      elif(command == 4):
         #delete the selected node (if confirmed)
         selectedNode = self.as_file.getNode(self.params['parent'],self.params['node'])
         
         confirm = xbmcgui.Dialog().yesno(utils.getString(30004) + ' ' + selectedNode.name,utils.getString(30020))

         if(confirm):
            self.as_file.deleteNode(selectedNode)

            #refresh the view
            xbmc.executebuiltin('Container.Refresh')

      elif(command == 5 or command == 6):
         #add an element
         nodeName = xbmcgui.Dialog().input(utils.getString(30021))
         nodeValue = xbmcgui.Dialog().input(utils.getString(30022))

         newNode = SettingNode(nodeName)
         newNode.value = nodeValue
         newNode.parent = self.params['node']

         #add element to this node
         if(command == 5):
            self.as_file.addNode(self.params['parent'],newNode)
         else:
            #add child element to selected node
            self.as_file.addNode(self.params['node'],newNode)

         xbmc.executebuiltin('Container.Refresh')


params = get_params()

gui = EditorGUI(params)

if(gui.shouldRun()):
   gui.showGUI()
else:
   xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
