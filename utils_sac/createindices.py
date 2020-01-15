
def NDVI(dataset):
    return (dataset.nir - dataset.red)/(dataset.nir + dataset.red)

def NDWI(dataset):
    return (dataset.green - dataset.nir)/(dataset.green + dataset.nir)

def NDBI(dataset):
    return (dataset.swir2 - dataset.nir)/(dataset.swir2 + dataset.nir)

#from within DCAL_Land_Change Script
def EVI(dataset):
    return 2.5*(dataset.nir - dataset.red)/(dataset.nir + 6.0*dataset.red - 7.5*dataset.blue + 1.0)