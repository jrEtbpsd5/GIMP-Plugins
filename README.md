# GIMP-Plugins
Some Python plug-ins for GIMP that I find useful. They work with GIMP 2.8+
and don't necessitate other plug-in.

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
via the context menu of the layer (right-clic).


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

### Prerequisites
- Basic Gimp 2.8+ (because of layer groups)
- there must be linked layers, the lowest one in the stack being the active 
  layer. All the linked layers must be in the same layer group. 
