from netCDF4 import Dataset
import xarray as xr
print("pocetak")
nc = "cartesian_tx.nc"
rootgrp = Dataset("cartesian_tx.nc", "r", format="NETCDF4")
print(rootgrp.dimensions['columns'])
