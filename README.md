# Split Crystal

### Files
Using dials.find_spots to produce a strong.pickle file with
all the reflections of a diffraction data set (h5 file) and
exporting that strong.pickle to xds format resulting in the
SPOT.XDS file.

The first column in SPOT.XDS are the x-coordinates.
The second column in SPOT.XDS are the y-coordinates.

### Explanation
The purpose for this program is to find split crystals
in diffraction images.

This program should be used after finding the spots initially using
dials.find_spots.

Current spotfinding algorithms find spots that belong to split crystals
but does not classify these images as containing a split crystal.

A fix is needed to find these spots that belong to split crystals
and inform the user.


