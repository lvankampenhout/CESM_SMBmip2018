

# Extract TOPO_COL from any h0 history file
ncks -v TOPO_COL /gpfs/fs1/scratch/lvank/archive/f.e20.FHIST.f09_001/lnd/hist/f.e20.FHIST.f09_001.clm2.h0.2001-11.nc LatLon_TOPO_COL.nc

cdo -f nc4 -z zip9 remapbil,/gpfs/u/home/lvank/github/smbmip_processing/step_2/dst_SCRIP.nc LatLon_TOPO_COL.nc Dst_TOPO_COL.nc
