#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   SMB mip 
"""
import sys
import glob
import os, os.path

# import libvector package from local directory tree
sys.path.insert(0, "../..")

from libvector import VectorMecVariable, vector2gridded3d 


datadir     = '/glade/u/home/lvank/scratch/archive' # post-fix /$CASENAME/lnd/hist/ is implicit
casename    = 'f.e20.FHIST.f09_001'
stream_tag  = 'h2' # stream identifier for vector data (h0, h1, or h2)
outdir      = '/glade/u/home/lvank/scratch/archive/smbmip/' # post-fix /$CASENAME/vector2gridded3d/varname will be added

files = glob.glob(os.path.join(datadir,casename, 'lnd', 'hist', '*'+stream_tag+'*.nc')) # all CLM vector data
files = sorted(files)
print(len(files))

varlist = 'RAIN SNOW QICE QRUNOFF QSNOMELT'.split()


for fname_vector in files:
   basename = fname_vector.split('/')[-1] # filename without path

   for varname in varlist:
      print("processing var = %s" % varname)

      outdir_var = os.path.join(outdir, casename, 'vector2gridded3d', varname)
      if not os.path.exists(outdir_var):
          os.makedirs(outdir_var)

      outfile = os.path.join(outdir_var, varname + '_' + basename)

      vmv = VectorMecVariable(varname, fname_vector)

      # set topography, required for custom levels
      fname_cpl_restart = "/glade2/scratch2/lvank/archive/f.e20.FHIST.f09_001/rest/1994-01-01-00000/f.e20.FHIST.f09_001.cpl.r.1994-01-01-00000.nc"
      vmv.setGlcTopoCouplerFile(fname_cpl_restart)

      # convert to 3D output (no corrections for elevation) and export to file
      levs = [0, 100.0, 300.0, 550.0, 850.0, 1150.0, 1450.0, 1800.0, 2250.0, 2750.0, 3500.0] 
      vector2gridded3d(vmv, outfile, levs)
      print('wrote %s' % outfile)
