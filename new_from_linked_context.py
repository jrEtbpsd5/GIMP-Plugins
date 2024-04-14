#!/usr/bin/env python

'''

Python plug-in for GIMP.

Function
--------
Similar to the command New from visible... but with linked layers only. 
Makes a copy of all linked layers, and merges the copies. Masks are applied. 
A new layer called new_from_linked is created like the visible layer of 
New from visible. All layers are then unlinked.

Usage
-----
Link several layers, the active layer being the lowest linked layer (in the 
layer stack). All the linked layers must be in the same layer group. 
Then right-clic (contextual menu) on the active layer and New from linked. 
The new layer, new_from_linked, appears just above the active layer. 

Prerequisites
-------------
- Basic Gimp 2.8+ (because of layer groups)
- there must be linked layers, the lowest one in the stack being the active 
  layer


Version
-------
version 1: Released February 26, 2023.
version 2: Bug related to group corrected. Released September 30, 2023.
version 3: Rewritten the register module. Released October 1, 2023.
version 4: Replaced the line with pdb.gimp_image_merge_layer_group() for 
           less requirements. Released November 18, 2023.

.........................................................................

Tested with Gimp 2.10.21 (Windows 10).

 ----------------------------------------------------------------

 COPYRIGHT NOTICE
 ----------------

 This program is free software you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program if not, you can view the GNU General Public
 License version 3 at the web site http://www.gnu.org/licenses/gpl-3.0.html
 Alternatively you can write to the Free Software Foundation, Inc., 675 Mass
 Ave, Cambridge, MA 02139, USA.

 -------------------------------------------------------------------

'''

from gimpfu import *
import os
import re
import sys


def python_new_from_linked_context(image, start_layer):

	# To start a group undo
	pdb.gimp_image_undo_group_start(image)
	
	# Save the interface context so that it can
	# be restored when the plug-in is done.
	pdb.gimp_context_push()

	# Defines some variables
	numlayers = len(image.layers)
	pos = -1
	lie = 0

	"""
	There are two cases: active layer is in image and 
	active layer is in a layer group.	
	The position of the active layer in image/group is saved. 
	Then the plugin recursively tests if layers above 
	the active one (in image/group) are linked. 
	If a layer is linked, it is duplicated and the 
	copy is added to a new auxiliary group (lies). 
	At the end, lies is merged and the resulting layer is 
	renamed new_from_linked	
	"""

	# Defines a new layer group lies
	lies = pdb.gimp_layer_group_new(image)
	
	# Tests if active layer is in a group
	parent = pdb.gimp_item_get_parent(start_layer)
	# If in a group, lists the layers in the group
	if parent is not None:
		# Identifies the parent
		pere = pdb.gimp_item_get_parent(start_layer)
		# Inserts lies in the parent group
		pdb.gimp_image_insert_layer(image, lies, pere, -1)	
		# Gets the childrens of the group
		num_children, child_ids = pdb.gimp_item_get_children(pere)
		# Looks for the position of the active layer inside the group
		for i in range(num_children):	
			if pere.layers[i] == start_layer:
				pos = i
		# Tests if layers above active one are linked
		for p in range(pos, -1, -1):
			cal_temp = pere.layers[p]
			lie = pdb.gimp_item_get_linked(cal_temp)
			# If a layer is linked it is duplicated and the copy is added to the 
			# group lies
			if (lie == 1):
				layer_copy = pdb.gimp_layer_copy(cal_temp, 1)
				pdb.gimp_image_insert_layer(image, layer_copy, lies, 0)

				# If the copy has a mask, it is applied
				if pdb.gimp_layer_get_apply_mask(layer_copy):
					pdb.gimp_layer_remove_mask(layer_copy, 0)

				# The layer and its copy are unlinked
				pdb.gimp_item_set_linked(layer_copy, FALSE)
				pdb.gimp_item_set_linked(cal_temp, FALSE)


	# If the active layer is not in a group,
	else:
		# lies is inserted under the active layer, 
		pdb.gimp_image_insert_layer(image, lies, None, pos)
		# Identifies position of active layer
		for i in range(len(image.layers)):
			if (image.layers[i] == start_layer):
				pos = i

		# Tests if layers above active one are linked
		for p in range(pos, -1, -1):
			cal_temp = image.layers[p]
			lie = pdb.gimp_item_get_linked(cal_temp)

			# If a layer is linked it is duplicated and the copy is added to the 
			# group lies
			if (lie == 1):
				layer_copy = pdb.gimp_layer_copy(cal_temp, 1)
				pdb.gimp_image_insert_layer(image, layer_copy, lies, 0)

				# If the copy has a mask, it is applied
				if pdb.gimp_layer_get_apply_mask(layer_copy):
					pdb.gimp_layer_remove_mask(layer_copy, 0)

				# the layer and its copy are unlinked
				pdb.gimp_item_set_linked(layer_copy, FALSE)
				pdb.gimp_item_set_linked(cal_temp, FALSE)

	# merges the layers in group lies		   
	num_children, child_ids = pdb.gimp_item_get_children(lies)
	debut = num_children - 1
	for p in range(debut, 0, -1):
		enfant = lies.layers[p-1] 
		fusbas = pdb.gimp_image_merge_down(image, enfant, 1)
		
	# put the resulting layer outside of the group
	pdb.gimp_image_reorder_item(image, fusbas, lies.parent, pos)
	# remove lies
	pdb.gimp_image_remove_layer(image, lies)
	
	# renames the new layer
	pdb.gimp_item_set_name(fusbas, "new_from_linked")

	# Restore the interface context.
	pdb.gimp_context_pop()

	# To end the group undo
	pdb.gimp_image_undo_group_end(image)
	
	# update display
	pdb.gimp_displays_flush()



register(
	"python_fu_new_from_linked_context",
	"Merge copies of each linked layer like New from visible",
	"The active layer must be the lowest linked layer",
	"Jacques",
	"Jacques P.",
	"2024",
	"New from linked layers",
	"",
	[
		(PF_IMAGE, "image", "Input image", None),
		(PF_DRAWABLE, "drawable", "Input drawable", None),
	],
	[],
	python_new_from_linked_context,
	menu="<Layers>/",
)


main()
