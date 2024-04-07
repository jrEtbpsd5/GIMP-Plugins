# GIMP-Plugins
Python plug-ins for GIMP

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
-------------
- basic Gimp 2.8+
- at least two layers, the active one and another layer which must be 
  linked (no other linked layer!)
