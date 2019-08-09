# Split Crystal

### Files
Using dials.find_spots to produce a strong.pickle file with
all the reflections of a diffraction data set (h5 file) and
exporting that strong.pickle to xds format resulting in the
SPOT.XDS file.

The first column in SPOT.XDS are the x-coordinates.
The second column in SPOT.XDS are the y-coordinates.

### Explanation
1. The purpose for this program is to find split crystals
in diffraction images.

2. This program should be used after finding the spots initially using
dials.find_spots.

3. Current spotfinding algorithms find spots that belong to split crystals
but does not classify these images as containing a split crystal.

4. A fix is needed to find these spots that belong to split crystals
and inform the user.

### Algorithm
1. Extract all the spots from SPOT.XDS
2. Compare the distance between each spot and every spot.
3. If the distance calculated between two spots is less than user-specified
distance in angstroms or default, both spots are saved as (x,y) coordinate pair.
