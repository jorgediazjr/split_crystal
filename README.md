# Split Crystal

### Files
Using dials.find_spots to produce a strong.pickle file with
all the reflections of a diffraction data set (h5 file) and
exporting that strong.pickle to xds format for SPOT.XDS.

The first column in SPOT.XDS are the x-coordinates.
The second column in SPOT.XDS are the y-coordinates.

### Explanation
The purpose for this program is to find split crystals.

This should be used after finding the spots initially.

Current spotfinding algorithms find spots that belong to split crystals.

A fix is needed to find these spots that belong to split crystals.


