Scripts supporting the CESM contribution to the SMB Model Intercomparison Project, August - October 2018.
Link to the SMBMIP project [here](http://climato.be/cms/index.php?climato=SMBMIP).


# Data details
The CESM data used in this submission stems from a atmosphere-only simulation (AMIP style) performed by Leo van Kampenhout on the Cheyenne supercomputer in August 2018. In particular, the compset used was `HIST_CAM60_CLM50%SP_CICE%PRES_DOCN%DOM_SROF_CISM2%NOEVOLVE_SWAV` with the sandbox `/gpfs/fs1/work/juliob/cesm_tags/cesm2.0.0`. 

The simulation was started in 1979 with initial files for the land component (CLM) and atmosphere component (CAM) taken from a recent coupled simulation (`b.e20.BHIST.f09_g17.20thC.299_01`) in the same year. SST and SIC are prescribed by the [Hurrell et al. 2008](https://doi.org/10.1175/2008JCLI2292.1) dataset.

All relevant variables for the intercomparison project were output in a separate CLM output stream separated by elevation class. This data presents a 3D view, if you will, of the mass and energy fluxes that are taking place over the Greenland ice sheet. This 3D view is mapped to the target resolution and topography by the scripts in this repository.


# Postprocessing details 

Step 1
------
   convert unstructured monthly data into levelled (3d) files. 
   
   The levels are in principle customizable but are chosen to reflect the levels that CLM internally uses (the virtual elevation class midpoints), augmented with sea level height:

```python
      levs = [0, 100.0, 300.0, 550.0, 850.0, 1150.0, 1450.0, 1800.0, 2250.0, 2750.0, 3500.0]
```

   tools: Python, the custom [libvector](https://github.com/lvankampenhout/libvector) library

Step 2
------
   create SCRIP grid description of target grid (regional ice sheet domain)

   tools: NCL, ESMF library

Step 3
------
   spatial regridding of levelled (3d) files to destination grid

   tools: Python, CDO

Step 4
------
   calculation of linear interpolation weights that project the 3D data onto the target elevation, yielding a 2D dataset. 
   
   The result of this step is a 3D weights matrix (nlev, nlat, nlon) of which each vertical column sum (i.e. wgt[:,i,j].sum()) equals 1. This matrix can be multiplied with the levelled files produced in the previous step and then summed in the vertical direction to obtain a "linear interpolation" to the target elevation.

   tools: Python

Step 5
------
   apply weights to monthly data. The result is a 2D projection on the target elevation.

   tools: Python

Step 6
------
   Various postprocessing: merge variables, aggregate into yearly files, rename variables, convert units, update attributes, 

   tools: Python / Jupyter notebook

Step 7
------
   Prepare file with some metadata

   tools: Python / Jupyter notebook
   
# Contact
Leo van Kampenhout (L.vankampenhout -at- uu.nl)
