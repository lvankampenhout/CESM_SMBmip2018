SMBmip, August 2018

STEP 1
------
   process monthly data, convert into gridded 3D files with custom levels

   tools: Python, "libvector" library

STEP 2
------
   create SCRIP grid description of target grid (regional ice sheet)
   by using 2-dimensional LAT and LON fields

   tools: NCL, ESMF library

STEP 3
------
   regridding of levelled (3d) filed to destination grid

   tools: Python, CDO

STEP 4
------
   calculate linear interpolation weights that project the 3D data onto the target elevation (2D)
   the result of this step is a 3D weights matrix (nlev, nlat, nlon) of which each vertical column 
   sum (i.e. wgt[:,i,j].sum()) equals 1.
   
   This matrix can be multiplied with the levelled files produced in step 3 and then summed in the 
   vertical direction to obtain a "linear interpolation" to the target elevation.

   tools: Python

STEP 5
------
   apply weights to monthly data, resulting in 2D maps on the target grid

STEP 6
------
   rename variables, correct units

   tools: NCO
