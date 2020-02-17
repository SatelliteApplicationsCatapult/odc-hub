# iJupyter Notebooks being adapted to work with Dask

This is a two-stage process:
- first adapt the code to run in conjunction with the local scheduler by chunking `dc.load()`, replacing cloud masking, and delaying raster operations until the very last one, executed with `compute()`
- secondly bring all dependencies across Dask workers and run the code across the distributed Dask cluster by creating a client for it

Once the last stage is completed and tested successfully, the resulting Notebook should be moved to the *completeforhandover* folder.
