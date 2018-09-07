load "$NCARG_ROOT/lib/ncarg/nclscripts/esmf/ESMF_regridding.ncl"
;
;     Multi-step regridding, steps 1-3

;     The multi-step process involves:
;     1- Creating the description NetCDF file for the source grid.
;     2- Creating the description NetCDF file for the destination grid.
;     3- Calculating and writing the weights to a NetCDF file.
;     4- Applying the weights to regrid the data from the source grid to the destination grid.
;     5- Copying attributes and coordinates to the newly regridded variable. 
;
;     source: http://www.ncl.ucar.edu/Document/Functions/ESMF/ESMF_regrid_gen_weights.shtml

begin

   srcGridName = "src_SCRIP.nc"
   dstGridName = "dst_SCRIP.nc"
   wgtFileName = "weights.nc"
  
   ; ============================ 
   ; source file
   ; ============================ 
   filein = "/glade/scratch_old/lvank/archive/smbmip/f.e20.FHIST.f09_001/QICE/QICE_f.e20.FHIST.f09_001.clm2.h2.1988-01.nc"
   ;f     = addfile(filein,"r")
   ;var = f->QICE(0,0,:,:)
   ;printVarSummary(var)

   ;Opt                = True
   ;Opt@GridMask       = where(.not.ismissing(var),1,0)
   ;Opt@ForceOverwrite = True
   ;Opt@PrintTimings   = True
   ;Opt@Title          = "CESM grid"

   ;rectilinear_to_SCRIP(srcGridName,var&latitude,var&longitude,Opt)

   ; ============================ 
   ; destination file
   ; ============================ 
   dest_grid = "/gpfs/p/work/lvank/SMBmip/MARv3.9-yearly-ERA-Interim-1980.nc"
   ;dest_grid = "/gpfs/p/work/lvank/SMBmip/grid.nc"
   f2 = addfile(dest_grid, "r")

   Opt                := True
   Opt@ForceOverwrite = True
   Opt@PrintTimings   = True
   Opt@Title          = "5x5km^2 GIMP grid provided by Xavier Fettweis"
   Opt@NetCDFType    = "netcdf4"

;   unstructured_to_ESMF(dstGridName, f2->LAT, f2->LON, Opt) ; LvK: Takes a very long time to finish!!
   curvilinear_to_SCRIP(dstGridName,f2->LAT,f2->LON,Opt) ; LvK: this is preferred, works with CDO


   ; ============================ 
   ; weights file 
   ; for use with ESMF_regrid_with_weights() function
   ; ============================ 

   Opt := True
   Opt@InterpMethod        = "bilinear"     ; bilinear, patch, conserve
   Opt@ForceOverwrite      = True
   Opt@PrintTimings        = True
   ;Opt@DstESMF = True ; set this for unstructured output
   ;ESMF_regrid_gen_weights(srcGridName, dstGridName, wgtFileName, Opt)

end
