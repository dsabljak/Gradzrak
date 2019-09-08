from netCDF4 import Dataset

class DataAnalizer():

    def __init__(self, rootgrp):

        self.rootgrp = rootgrp
        self.printing()

    def printing(self):

        print("Beginning analysis")
        # nc = "cartesian_tx.nc"
        # rootgrp = Dataset("cartesian_tx.nc", "r", format="NETCDF4")
        # print(rootgrp.dimensions['columns'])
        print(self.rootgrp.variables)
        for attr in self.rootgrp.ncattrs():
            print(attr, "=", getattr(self.rootgrp, attr))

