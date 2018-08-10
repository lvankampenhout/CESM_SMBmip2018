#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
interpolation of 3D gridded data to destination grid 
"""

import sys
import glob
import os, os.path
import subprocess 

casename    = 'f.e20.FHIST.f09_001'
#stream_tag  = 'h2' # stream identifier for vector data (h0, h1, or h2)
outdir      = '/glade/u/home/lvank/scratch/archive/smbmip/' # post-fix /$CASENAME/dstGrid3d/varname will be added
scrip_dst   = '/gpfs/u/home/lvank/github/libvector/smbmip/step_2/dst_SCRIP.nc' # SCRIP file of destination grid (from step 2)
remap_wgt    = 'remap_weights.nc' # temporary file

varlist = 'RAIN SNOW QICE QRUNOFF QSNOMELT'.split()

for varname in varlist:

   indir_var = os.path.join(outdir, casename, 'vector2gridded3d', varname)
   outdir_var = os.path.join(outdir, casename, 'dstGrid3d', varname)
   if not os.path.exists(outdir_var):
       os.makedirs(outdir_var)

   files = glob.glob(os.path.join(indir_var, '*.nc')) # all CLM vector data
   files = sorted(files)
   print(varname, len(files))

   #infile =  os.path.join(indir_var, varname+'_all.nc')
   #outfile = os.path.join(outdir_var, varname+'_all.nc')

   for infile in files:

      if (not os.path.exists(remap_wgt)):
         # only needed once per destination grid
         args = ['cdo']
         args += ['genbil,%s' % scrip_dst, infile, remap_wgt]
         subprocess.check_call(args, stderr=subprocess.STDOUT)

      basename = infile.split('/')[-1] # filename without path
      outfile = os.path.join(outdir_var, basename)

      args = ['cdo']
      args += ['--format', 'nc4', '-b', 'F32']
      #args += ['-z', 'zip1']
      args += ['remap,%s,%s' % (scrip_dst, remap_wgt), infile, outfile]
      print(infile)
      subprocess.check_call(args, stderr=subprocess.STDOUT)
