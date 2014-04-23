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
      if(node.hasChildren):
         #if this is a top level node of a larger set
         item = xbmcgui.ListItem(str(node.name),"")
         item.addContextMenuItems([('Rename',"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=2&node=" + node.name + "&parent=" + node.parent))])
         ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=context_url % (sys.argv[0],"command=0&node=" + node.name),listitem=item,isFolder=True)
      else:
         #if this is an item with a value
         item = xbmcgui.ListItem(str(node.name),"")
         item.addContextMenuItems([('Change Value',"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=3&node=" + node.name + "&parent=" + node.parent)),('Rename',"Xbmc.RunPlugin(%s?%s)" % (sys.argv[0],"command=2&node=" + node.name + "&parent=" + node.parent))])

         ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=context_url % (sys.argv[0],"command=1&node=" + node.name + "&parent=" + node.parent),listitem=item,isFolder=False)

   xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
   
elif(command == 1):
   #show information about the currently selected node
   selectedNode = as_file.getNode(params['parent'],params['node'])

   xbmcgui.Dialog().ok(selectedNode.name,'Value: ' + selectedNode.value)

elif(command == 2):
   #rename selected node
   selectedNode = as_file.getNode(params['parent'],params['node'])
   
   newName = xbmcgui.Dialog().input('Rename ' + selectedNode.name)

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
