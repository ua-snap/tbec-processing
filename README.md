# Data Processing codebase for Two Bears Environmental Consulting collaboration

This codebase is responsible for all data processing for the Two Bears Environmental Consulting (TBEC) collaboration. SNAP is responsible for deriving some summaries of "extremes" or "indices". To [quote NCAR](https://climatedataguide.ucar.edu/climate-data/overview-climate-indices), "A climate index is a simple diagnostic quantity that is used to characterize an aspect of a geophysical system." These are basically variables that are derived from more traditional geophysical variables (e.g. temperature, precipitation) over some timespan. 

While the term "indices" is probably more common when referring to the types of variables we are working with here, there may still be references to "extremes" throughout the codebase - just treat these as interchangeable.

## Running the pipeline

This project utilizes `conda` to manage dependencies. To run any part of the pipeline, create an environment from the `environment.yml` file via

```
conda env create -f environment.yml
```

This will create a conda environment named `tbec-processing`. Activate the environment via 

```
conda activate tbec-processing
```

and then set the environment variables listed below.

Then, run the pipeline with either `jupyter lab` or `jupyter notebook` to start a Jupyter server, and open / execute the `process_indices.ipynb` notebook to create the annual indices data that all other processing depends on. See the [Structure](#Structure) section below for more information on the functions of each of the notebooks.

#### Environment variables

The following variables need to be set prior to starting a Jupyter instance as directed above. The values used for the "production" data are provided in the `production_env_vars.sh` script for SNAP reference.

`OUTPUT_DIR`

The output directory where final products are placed.

`CORDEX_DIR`

The directory containing bias-corrected CMIP5 CORDEX data from Stantec. If you are working on Atlas and have a copy of this available on scratch space, or if you have the time to copy the data to scratch space for processing, supply that path for increased performance. 

#### Structure

This project involves a fair bit of production of visual products for summarization of the various indices, particularly at key locations. So the first step is to derive the indices from the base data at an annual time scale, and all other summarization/visualization tasks will depend on that dataset. 

The main pipeline for deriving the dataset of indices exists in the root folder of this project and is controlled with the `process_indices.ipynb` notebook - execute that first and use the `qc.ipynb` notebook to check the quality of that resulting dataset, which will be available at `$OUTPUT_DIR/annual_indices.nc`. 

The various summarization tasks are carried out using the other notebooks in the root folder:

* `extract_indices.ipynb`: Make point extractions from the annual indices dataset for some points of interest, summarizing to various decadal and 30-year time periods
* `initial_summary.ipynb`: This notebook derives some summary bar charts using the base data (not the indices dataset)
* `location_summary_plots.ipynb`: Make bar charts using the summarized annual indices extracted for the points of interest with the `extract_indices.ipynb` notebook

#### Syncing with Google Drive

Since this project has external collaborators, syncing the products created here with Google drive is one way to make sharing easier.

The `Projects/TBEC CMIP5 Processing` folder of the SNAP Team shared drive is where this stuff can go. 

If you have `rclone` configured with a mount for your personal drive, and then a shortcut to the SNAP Team drive on your root Drive direcotry, here is an example for syncing files:

```
rclone sync decadal_summary_charts google-drive:Projects/TBEC\ CMIP5\ Processing/Decadal\ summary\ charts
```
