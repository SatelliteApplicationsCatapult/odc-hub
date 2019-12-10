
def NDVI(dataset):
    return (dataset.nir - dataset.red)/(dataset.nir + dataset.red)

def NDWI(dataset):
    return (dataset.green - dataset.nir)/(dataset.green + dataset.nir)

def NDBI(dataset):
        return (dataset.swir2 - dataset.nir)/(dataset.swir2 + dataset.nir)
