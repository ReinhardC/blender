# Weird Blender plugin

Let's you copy/paste a node to many materials at once. Intended for texture baking but can maybe be used for other things later.

Installation: download weird_blender.zip, install using Edit->Preferences->Add-ons->Install, select ZIP

Usage MultiCopy: Right-click Image Texture Node in node editor, select "Weird Blender->MultiCopy" (Works at the moment for Image Texture Nodes only, will be extended)
       
Usage MultiPaste: After copying, go to the outliner, select several Materials, right click, select "Weird Blender->MultiPaste" to paste the copied node into all the selected Materials. It will be activated automatically so it can be used for baking after that.
  
Usage MultiKill: If you want to delete the copied Node from several Materials, select the Materials, then use "Weird Blender->MultiKill"
