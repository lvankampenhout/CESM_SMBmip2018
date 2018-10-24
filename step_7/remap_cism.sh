# File containing lat,lon of 4 km CISM grid
CISM_GRID=/glade/p/cesmdata/cseg/inputdata/glc/cism/Greenland/glissade/init/greenland_4km_epsg3413_c171126.nc

# SCRIP of 1 km target grid
TARGET_GRID=/gpfs/u/home/lvank/github/smbmip_processing/step_2/dst_SCRIP.nc

# Thickness file
THK_FILENAME=/gpfs/fs1/scratch/lvank/archive/f.e20.FHIST.f09_001/glc/hist/f.e20.FHIST.f09_001.cism.h.1980-01-01-00000.nc

# Do only once
cdo remapbil,$TARGET_GRID -setgrid,$CISM_GRID -select,name=thk $THK_FILENAME thk_DST.nc
