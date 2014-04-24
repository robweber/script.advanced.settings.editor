Advanced Settings Editor


Updating the Advanced Settings document in XBMC is usually a pain. It involves tedious low-level interaction with the file system. This addon seeks to change that by allowing you to browse and interact with the xml nodes of that document via a GUI menu. 

Navigation:

You navigate through the document as though it was a folder structure. Given the following:

<advancedsettings>
   <log>1</log>
   <videolibrary>
      <backgroundupdate>false</backgroundupdate>
   </videolibrary>
</advancedsettings>

You would see the following when starting the program: 

log
videolibrary

These are the top level elements of the file. Clicking an element with no children will show you it's current value. Clicking on element with children will bring you into that element. For example, clicking on the "videolibrary" element will show you:

backgroundupdate

And that element is clickable to show you it's value. In this way you navigate the tree. 


Context Menu:

The context menu has several different features. 

Add Element - Adds a child element within the current view
Add Child Element - Adds a child element within the selected element. Please note, if you have selected an element with a value, this value is erased when you add children
Change value - only available on elements with no children. Allows you to change the value in the current element
Delete - deletes the selected element, recursive for elements with children
Rename - rename the selected element
