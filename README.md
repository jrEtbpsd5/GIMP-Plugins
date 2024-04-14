# GIMP-Plugins
Some Python plug-ins for GIMP that I find useful. They work with GIMP 2.8+
and don't necessitate other plug-in. They have been tested on Windows 10 and
on Debian 11.
<br>

## Mask from linked.

### Function

Adds to active layer a mask initialised with the alpha channel of
another layer which must be linked.	 If active layer has already
a mask, this mask is modified. At the end the linked layer is unlinked.


### Usage

Link the layer which transparency you want to use.
Click on the layer which mask you want to modify.
Layer > Mask > Mask from linked layer.
The context version: mask_from_linked_context.py is accessible
via the context menu of the active layer (right-clic).


### Prerequisites
- basic Gimp 2.8+
- at least two layers, the active one and another layer which must be 
  linked (no other linked layer!)
<br>

## New from linked

### Function

Similar to the command "New from visible..." but with linked layers only. 
Makes a copy of all linked layers, and merges the copies. Masks are applied. 
A new layer called new_from_linked is created like the visible layer of "New 
from visible". All layers are then unlinked.

### Usage

Link several layers, the active layer being the lowest linked layer (in the 
layer stack). Then Layer > New from linked. The new layer, new_from_linked, appears 
just above the active layer. 
The context version: new_from_linked_context.py is accessible
via the context menu of the active layer (right-clic).

### Prerequisites
- Basic Gimp 2.8+ (because of layer groups)
- there must be linked layers, the lowest one in the stack being the active 
  layer. All the linked layers must be in the same layer group. 

<br>

## Selection within layer

### Function

It's the script in Scheme from [saulgoode](https://chiselapp.com/user/saulgoode/repository/script-fu/wiki?name=sg-select-within-layer) 
rewritten in Python. The function is the same: to select a whole layer and to keep this selection to use it on another layer (which is 
not possible with "Select > Select All"). 
If there is already a selection, the new selection replaces it.

### Usage

Right-clic on the layer (context menu of the layer) and choose "Selection within layer". This is
the only difference with original script which is in the Select menu.

### Prerequisites
- basic Gimp 2.8+

