#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
interpolation of 3D gridded data to destination grid 
"""

import sys
import time
import os, os.path
import numpy as np
import netCDF4
from netCDF4 import Dataset, default_fillvals
from scipy.interpolate import InterpolatedUnivariateSpline

t1 = time.time()

# Output file
outfile = 'projection_weights.nc'

# Target elevation 
if (False):
   elev_file   = '/gpfs/p/work/lvank/SMBmip/MARv3.9-yearly-ERA-Interim-1980.nc' # contains target elevation
   elev_varname = 'SRF_GIMP'
   elev_lat = 'LAT'
   elev_lon = 'LON'

if (True): # ISMIP6-1km 
   elev_file = '/gpfs/fs1/work/lvank/SMBmip/1km-ISMIP6.nc'
   elev_varname = 'SRF'
   elev_lat = 'lat'
   elev_lon = 'lon'

with Dataset(elev_file,'r') as fid:
   target_srf = fid.variables[elev_varname][:].squeeze() # Two dimensional

   lat2d = fid.variables[elev_lat][:]
   lon2d = fid.variables[elev_lon][:]
   

# construct mask with invalid values, which will be used during output phase
topo_dst_masked = np.ma.masked_greater(target_srf, 4000.)  # removes all values of 9999
topo_dst_masked = np.ma.masked_less(topo_dst_masked, 0.) # removes negative values

# standard numpy array for calculating weights; invalid values are treated as if they 
# were at sea level (z=0) and will be masked later.
topo_dst = topo_dst_masked.filled(fill_value = 0)

#print(topo_dst.min())
#print(topo_dst.max())
#print(topo_dst.shape)
nlat, nlon = topo_dst.shape
print(topo_dst.shape)


# Source elevation
if (True):
   # custom levels as defined in step 1
   levs = np.array( [0, 100.0, 300.0, 550.0, 850.0, 1150.0, 1450.0, 1800.0, 2250.0, 2750.0, 3500.0] )
   nlev = len(levs)

else:
   # MEC column topography
   # read TOPO_COL on target grid

   msg = '''
   Script only custom levels at this point'''
   raise NotImplementedError(msg)


if (topo_dst.max() >= levs[-1]):
   msg = '''
      Largest elevation on destination grid exceeds highest MEC level! 
      This possibility has not accounted for in the script.'''
   raise NotImplementedError(msg)



# -------------------
# compute weights
# -------------------

# numpy.digitize() : Return the indices of the bins to which each value in input array belongs.
bin_idx = np.digitize(topo_dst, bins=levs)

# setting lower bin bound of 1 is needed to prevent errors for points that have elevation 0.0 in the 
# GIMP dataset. They would return upper bound index 0, and 0-1 = -1, which is an invalid 
# choice index. Adding '1' in this case is a workaround, that should not change
# answer because the weight of lev_A is 1.0 and lev_B 0.0
bin_idx = np.where(bin_idx < 1, 1, bin_idx)

# the elevation on the destination grid can always be bound by two levels, lets say A and B
# in other words, for any grid point on the destination grid, some levels A and B satisfy A <= z < B
# the bounding levels are determined for each grid cell simultaneously
lev_A = np.take(levs, bin_idx - 1)
lev_B = np.take(levs, bin_idx)

# compute weights for each level (linear interpolation)
wgt_A = (lev_B - topo_dst) / (lev_B - lev_A)
wgt_B = (topo_dst - lev_A) / (lev_B - lev_A)

assert(wgt_A.max() <= 1.0)
assert(wgt_A.min() >= 0.0)
assert(wgt_B.max() <= 1.0)
assert(wgt_B.min() >= 0.0)

# store weights in 3d levelled array
wgt = np.ma.zeros((nlat,nlon,nlev), dtype=np.float64)
#print(wgt.shape)
#print(bin_idx.shape)

t2 = time.time()
print('INFO: elapsed time: %s [s]' % str(t2-t1))

# insert weights into weights array
# there should be a better way to do this than two nested for-loops
# see my question posed here: https://stackoverflow.com/questions/51739574/fill-3d-levelled-array-with-2d-weights-and-level-indices
for ii in range(nlat):
   for jj in range(nlon):
      wgt[ii,jj,bin_idx[ii,jj]-1] = wgt_A[ii,jj]
      wgt[ii,jj,bin_idx[ii,jj]]   = wgt_B[ii,jj]

assert(np.allclose(np.sum(wgt,axis=2), 1.0, rtol=1e-05, atol=1e-08))

# Set mask to account for invalid values
wgt.mask = topo_dst_masked.mask 

t2 = time.time()
print('INFO: elapsed time: %s [s]' % str(t2-t1))

# reorder dimensions to (nlev, nlat, nlon)
wgt2 = wgt.transpose((2,0,1)) 


if (True): # write output file
   print("INFO: writing %s" % outfile)
   ncfile = Dataset(outfile, 'w', format='NETCDF4')
   ncfile.title = 'Linear interpolation weights for projecting levelled CLM output onto target elevation '
   ncfile.elev_file = elev_file

   ncfile.institute = "NCAR / Utrecht University"
   ncfile.contact = "L.vankampenhout@uu.nl"

   ncfile.netcdf = netCDF4.__netcdf4libversion__

   # Create dimensions
   ncfile.createDimension('y', nlat)
   ncfile.createDimension('x', nlon)
   ncfile.createDimension('lev',nlev)

   # Define the coordinate var
   lons   = ncfile.createVariable('lon', 'f8', ('y','x'))
   lats   = ncfile.createVariable('lat', 'f8', ('y','x'))
   levs   = ncfile.createVariable('lev', 'i4', ('lev',))

   # Assign units attributes to coordinate var data
   lons.standard_name = "longitude" ;
   lons.long_name = "longitude" ;
   lons.units   = "degrees_east"
   lons.axis = "Y"

   lats.standard_name = "latitude" ;
   lats.long_name = "latitude" ;
   lats.units   = "degrees_north"
   lats.axis = "X"
   
   levs.units   = "MEC level number"
   
   # Write data to coordinate var
   lons[:]    = lon2d[:]
   lats[:]    = lat2d[:]
   levs[:]    = range(0,nlev)

   var            = ncfile.createVariable('weights','f4',('lev','y','x',), fill_value=default_fillvals['f4'])
   var.units      = "-"
   var.long_name  = "interpolation weights"
   var[:] = wgt2
   ncfile.close()
   print("INFO: done")


t2 = time.time()
print('INFO: elapsed time: %s [s]' % str(t2-t1))
