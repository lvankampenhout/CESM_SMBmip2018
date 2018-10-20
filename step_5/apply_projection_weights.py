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

varlist = []
varlist += 'RAIN SNOW QICE QRUNOFF QSNOMELT'.split()
varlist += 'QICE_MELT QSOIL'.split()
varlist += 'FSA FSR'.split()
varlist += 'FIRE FIRA'.split()
varlist += 'FSH EFLX_LH_TOT TSA'.split()

# weights file
wgtfile = '/glade/u/home/lvank/github/smbmip_processing/step_4/projection_weights.nc'

######
# END OF USER SETTINGS
######

ds_wgt = xr.open_dataset(wgtfile)
wgt = ds_wgt['weights']

for varname in varlist:

   indir_var = os.path.join(outdir, casename, 'dstGrid3d', varname)
   outdir_var = os.path.join(outdir, casename, 'dstGrid2d', varname)
   if not os.path.exists(outdir_var):
       os.makedirs(outdir_var)

   files = glob.glob(os.path.join(indir_var, '*.nc')) # all CLM vector data
   files = sorted(files)
   print(varname, len(files))

   for infile in files:

      basename = infile.split('/')[-1] # filename without path
      outfile = os.path.join(outdir_var, basename)

      if (os.path.exists(outfile)): 
         print("INFO: file exists, skipping: "+outfile)
         continue

      ds = xr.open_dataset(infile)
      ds[varname] *=  wgt

      da_var = ds[varname].sum(dim='lev', skipna=False, keep_attrs=True)
      da_var.encoding = {'dtype': 'float32', '_FillValue': 9.96921e+36}

      ds.drop(varname)
      ds[varname] = da_var

      #ds = ds.squeeze(drop=True) # drop time dimension

      #print(ds[varname])
      #ds[varname].encoding = {'dtype': 'float32', '_FillValue': 9.96921e+36}
      ds.to_netcdf(outfile,'w') #, encoding={'_FillValue': 9.96921e36})

      ds.close()
      print("INFO: written %s" % outfile)
