#!/usr/bin/env python

'''

selection_within_layer.py.
Python plug-in for GIMP.

Function
--------
It's the script sg-select-within-layer.scm written in Python. The function is the same: to select a whole layer and to keep this selection to use it on another layer (which is not possible with Select > Select All). If there is already a selection, the new selection replaces it.


Usage
-----

Right-clic on the layer (context menu of the layer) and choose
"Selection within layer".


Prerequisites
-------------
- basic Gimp 2.8+



Version
-------
version 1: Released on March 2, 2024.


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
import sys


def python_selection_within_layer(image, start_layer):
	# To start a group undo
	pdb.gimp_image_undo_group_start(image)
	
	# Save the interface context so that it can
	# be restored when the plug-in is done.
	pdb.gimp_context_push()
	
	# Compute the width, the height and the coordinates of the upper left
	# corner of the active layer
	calque = pdb.gimp_image_get_active_layer(image)
	larg = pdb.gimp_drawable_width(calque)
	haut = pdb.gimp_drawable_height(calque)
	offset_x, offset_y = pdb.gimp_drawable_offsets(calque)
	
	# create a rectangular selection with same width, height and origin
	pdb.gimp_image_select_rectangle(image, 2, offset_x, offset_y, larg, haut)

	# Restore the interface context.
	pdb.gimp_context_pop()
	
	# To end the group undo
	pdb.gimp_image_undo_group_end(image)
	
	# update display
	pdb.gimp_displays_flush()


register(
	"python_fu_selection_within_layer",
	"Select a whole layer",
	"The selection can be used on another layer",
	"Jacques",
	"Jacques P.",
	"2024",
	"Selection within layer",
	"",
	[
	 (PF_IMAGE, "image", "Input image", None),
	 (PF_DRAWABLE, "start_layer", "Input layer", None),
	],
	[],
	python_selection_within_layer,
	menu="<Layers>/",
)

main()
