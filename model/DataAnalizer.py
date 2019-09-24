from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
class DataAnalizer():

    def __init__(self, rootgrp):

        self.rootgrp = rootgrp
        self.printing()

    def printing(self):

        print("Beginning analysis")
        # nc = "cartesian_tx.nc"
        dataset = Dataset(self.rootgrp, "r", format="NETCDF4")

        data = np.array(dataset.variables['OTCI'])

        plt.imshow(data,cmap='viridis', interpolation='nearest')
        plt.colorbar()

        plt.show()
