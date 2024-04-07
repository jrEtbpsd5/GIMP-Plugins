#!/usr/bin/env python

'''

Python plug-in for GIMP.

Function
--------
Adds to active layer a mask initialised with the alpha channel of
another layer which must be linked.	 If active layer has already
a mask, this mask is modified. At the end the linked layer is unlinked.


Usage
-----

Link the layer which transparency you want to use.
Right-clic on the layer which mask you want to modify and select 
"Mask from linked layer"


Prerequisites
-------------
- basic Gimp 2.8+
- at least two layers, the active one and another
layer which must be linked (no other linked layer!)


Version
-------
version 1: Released on October 7, 2022.
version 2: Improved linked layer search. Released on October 8, 2022.
version 3.1: Added a pop-up message for when a linked layer isn't found.
Released October 12, 2022.
version 3.2: plug-in is now in context menu of Layer Window (right-clic on
the active layer). Released October 14, 2022. 
version 4: added the possibility to undo. Released March 8, 2024. 

.........................................................................

Tested with Gimp 2.10.8 (Debian 10) and with Gimp 2.10.21 (Windows 10).

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
import sys


def find_linked_layer(layer, is_found):
	"""
	Recursively search the layer
	palette for a linked layer.

	group layer or GIMP image
		to search

	is_found: bool
		When True the recursion backs out.

	Return: tuple
		layer, bool
		(linked layer or last layer, success flag)
	"""
	if is_found:
		# Back-out of recursion.
		return layer, True

	for i in layer.layers:
		is_linked = pdb.gimp_item_get_linked(i)
		if is_linked:
			# Back-out of the recursion.
			return i, True

		# Both image and group layer have this attribute, 'layers'.
		if hasattr(i, 'layers'):
			i, is_found = find_linked_layer(i, is_found)
		if is_found:
			return i, True
	return layer, is_found


def python_mask_from_linked_context(image, start_layer):
	
	# To start a group undo
	pdb.gimp_image_undo_group_start(image)
	
	# Save the interface context so that it can
	# be restored when the plug-in is done.
	pdb.gimp_context_push()

	# reset default foreground-background colors
	pdb.gimp_context_set_default_colors()

	# rename active layer as calqueactif
	calqueactif = pdb.gimp_image_get_active_layer(image)

	# search for linked layer
	calquedessous, is_found = find_linked_layer(image, False)

	# calquedessous is now the name of the linked layer

	if is_found:
		# activate calquedessous (the linked layer)
		pdb.gimp_image_set_active_layer(image, calquedessous)

		# test if calquedessous has a mask
		masqueunder = pdb.gimp_layer_get_mask(calquedessous)
		if pdb.gimp_item_is_valid(masqueunder) == 1:

			# if yes, duplicate calquedessous
			layer_copy = pdb.gimp_layer_copy(calquedessous, 0)
			pdb.gimp_image_insert_layer(image, layer_copy, None, 0)

			# apply the mask of the copy
			pdb.gimp_layer_remove_mask(layer_copy, MASK_APPLY)

			# Alpha to selection on the copy
			pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, layer_copy)

			# delete copy of calquedessous
			pdb.gimp_image_remove_layer(image, layer_copy)

		else:
			# if no mask, Alpha to selection on calquedessous
			pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, calquedessous)

		# in both cases active selection is alpha channel selection

		# activate calqueactif
		pdb.gimp_image_set_active_layer(image, calqueactif)

		# define masqueactif as its mask
		masqueactif = pdb.gimp_layer_get_mask(calqueactif)

		# test if calqueactif has already a mask
		# and if no create a mask from active selection:
		if pdb.gimp_item_is_valid(masqueactif) != 1:
			masque = pdb.gimp_layer_create_mask(
				calqueactif,
				ADD_MASK_SELECTION
			)

			# add the mask to calqueactif
			pdb.gimp_layer_add_mask(calqueactif, masque)

		# if yes:
		else:
			# invert selection
			pdb.gimp_selection_invert(image)

			# set mask of calqueactif as active
			pdb.gimp_layer_set_edit_mask(calqueactif, 1)
			masque = pdb.gimp_image_get_active_drawable(image)

			# fill it with black inside the selection
			pdb.gimp_drawable_edit_fill(masque, FILL_FOREGROUND)

		# deselect all
		pdb.gimp_selection_none(image)

		# unlink the linked layer
		pdb.gimp_item_set_linked(calquedessous, 0)

	# if no linked layer, display error message
	else:
		pdb.gimp_message_set_handler(MESSAGE_BOX)
		pdb.gimp_message("NO LINKED LAYER\nPLEASE LINK A LAYER")

	# Restore the interface context.
	pdb.gimp_context_pop()

	# To end the group undo
	pdb.gimp_image_undo_group_end(image)
	
	# update display
	pdb.gimp_displays_flush()


register(
	"python_fu_mask_from_linked_context",
	"Adds a layer mask initialised with alpha channel of another layer",
	"Adds a layer mask initialised with alpha channel of the linked layer",
	"Jacques",
	"Jacques P.",
	"2024",
	"Mask from linked layer",
	"",
	[
		(PF_IMAGE, "image", "Input image", None),
		(PF_DRAWABLE, "drawable", "Input drawable", None),
	],
	[],
	python_mask_from_linked_context,
	menu="<Layers>/",
)


main()
