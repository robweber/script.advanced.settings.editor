import xbmc,xbmcgui,xbmcplugin
import urlparse
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

   print(param)
   if("node" not in param):
      param['node'] = None

   if("command" not in param):
      param['command'] = 0

   if('parent' not in param):
      param['parent'] = ''

   return param

params = get_params()

context_url = "%s?%s"

as_file = AdvancedSettings()


#list the nodes
command = int(params['command'])
if(command == 0):
   topLevel = as_file.listNodes(params['node'])
   
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

   xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
   
elif(command == 1):
   #show information about the currently selected node
   selectedNode = as_file.getNode(params['parent'],params['node'])

   xbmcgui.Dialog().ok(selectedNode.name,utils.getString(30006) + ": " + selectedNode.value)

elif(command == 2):
   #rename selected node
   selectedNode = as_file.getNode(params['parent'],params['node'])
   
   newName = xbmcgui.Dialog().input(utils.getString(30005) + ' ' + selectedNode.name)

   as_file.renameNode(selectedNode,newName)

   #refresh the view
   xbmc.executebuiltin('Container.Refresh')

elif(command == 3):
   #change the selected node value
   selectedNode = as_file.getNode(params['parent'],params['node'])
   
   newValue = xbmcgui.Dialog().input('New Value ' + selectedNode.name)

   as_file.updateValue(selectedNode,newValue)

   #refresh the view
   xbmc.executebuiltin('Container.Refresh')

elif(command == 4):
   #delete the selected node (if confirmed)
   selectedNode = as_file.getNode(params['parent'],params['node'])
   
   confirm = xbmcgui.Dialog().yesno(utils.getString(30004) + ' ' + selectedNode.name,utils.getString(30020))

   if(confirm):
      as_file.deleteNode(selectedNode)

      #refresh the view
      xbmc.executebuiltin('Container.Refresh')

elif(command == 5 or command == 6):
   #add an element
   selectedNode = as_file.getNode(params['parent'],params['node'])

   nodeName = xbmcgui.Dialog().input(utils.getString(30021))
   nodeValue = xbmcgui.Dialog().input(utils.getString(30022))

   newNode = SettingNode(nodeName)
   newNode.value = nodeValue
   newNode.parent = selectedNode.name

   #add element to this node
   if(command == 5):
      as_file.addNode(selectedNode.parent,newNode)
   else:
      #add child element to selected node
      as_file.addNode(selectedNode.name,newNode)

   xbmc.executebuiltin('Container.Refresh')
 
