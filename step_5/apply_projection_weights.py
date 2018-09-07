#!/gpfs/u/home/lvank/miniconda3/bin/python3
###!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
projection of 3D gridded data to 2D using vertical interpolation weights
"""

import sys
import glob
import os, os.path
#import subprocess 
import xarray as xr
import numpy as np

casename    = 'f.e20.FHIST.f09_001'
#stream_tag  = 'h2' # stream identifier for vector data (h0, h1, or h2)
outdir      = '/glade/u/home/lvank/scratch/archive/smbmip/' # post-fix /$CASENAME/dstGrid3d/varname will be added
#scrip_dst   = '/gpfs/u/home/lvank/github/libvector/smbmip/step_2/dst_SCRIP.nc' # SCRIP file of destination grid (from step 2)
#remap_wgt    = 'remap_weights.nc' # temporary file

varlist = 'RAIN SNOW QICE QRUNOFF QSNOMELT'.split()

# weights file
outfile = '../step_4/projection_weights.nc'

######
# END OF USER SETTINGS
######

ds_wgt = xr.open_dataset(outfile)
wgt = ds_wgt['weights']

for varname in varlist:

   indir_var = os.path.join(outdir, casename, 'dstGrid3d', varname)
   outdir_var = os.path.join(outdir, casename, 'dstGrid2d', varname)
   if not os.path.exists(outdir_var):
       os.makedirs(outdir_var)

   files = glob.glob(os.path.join(indir_var, '*.nc')) # all CLM vector data
   files = sorted(files)
   print(varname, len(files))

   #infile =  os.path.join(indir_var, varname+'_all.nc')
   #outfile = os.path.join(outdir_var, varname+'_all.nc')

   for infile in files:

      basename = infile.split('/')[-1] # filename without path
      outfile = os.path.join(outdir_var, basename)

      ds = xr.open_dataset(infile)
      #print(ds[varname])
      ds[varname] *=  wgt
      #print(ds[varname])

      da_var = ds[varname].sum(dim='lev', skipna=False)
      da_var.encoding = {'dtype': 'float32', '_FillValue': 9.96921e+36}
      #print(da_var)

      ds.drop(varname)
      ds[varname] = da_var
      #ds.drop('lev')
      ds = ds.squeeze(drop=True)

      #print(ds[varname])
      #ds[varname].encoding = {'dtype': 'float32', '_FillValue': 9.96921e+36}
      ds.to_netcdf(outfile,'w') #, encoding={'_FillValue': 9.96921e36})

      ds.close()
      print("INFO: written %s" % outfile)
      #assert(False)

