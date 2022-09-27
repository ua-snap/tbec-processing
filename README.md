# Data Processing codebase for Two Bears Environmental Consulting collaboration

This codebase is responsible for all data processing for the Two Bears Environmental Consulting (TBEC) collaboration. SNAP is responsible for deriving some summaries of "extremes" or "indices". To [quote NCAR](https://climatedataguide.ucar.edu/climate-data/overview-climate-indices), "A climate index is a simple diagnostic quantity that is used to characterize an aspect of a geophysical system." These are basically variables that are derived from more traditional geophysical variables (e.g. temperature, precipitation) over some timespan. 

While the term "indices" is probably more common when referring to the types of variables we are working with here, there may still be references to "extremes" throughout the codebase - just treat these as interchangeable.

## Running the pipelines in this codebase

This codebase is set up to work with [Anaconda Project](https://anaconda-project.readthedocs.io/en/latest/), the conda-based dependency management system.

To run any of the pipelines here, which are set up as Jupyter notebooks, simply install Anaconda or Miniconda, and install Anaconda Project via `conda install anaconda-project` if you do not have it (it comes with Anaconda v4.3.1 and later by default).

Once you have Anaconda Project installed, running any of the notebooks with all required dependencies is as simple as:

```sh
anaconda-project run <command>
```

where `<command>` should be replaced by any of the available commands below. Running this command will ensure that all dependencies are installed. 

#### Environment variables

Running the any of the above commands will ensure that the required environment variables are defined, which are:

`BASE_DIR`

The base directory for storing project data that should be backed up.
* default value: `/workspace/Shared/Tech_Projects/TBEC_CMIP5_Processing/project_data`

`OUTPUT_DIR`

The output directory where final products are placed.
* default value: `/workspace/Shared/Tech_Projects/TBEC_CMIP5_Processing/final_products`

`SCRATCH_DIR`

The scratch directory for storing project data which does not need to be backed up. This one does not have a default and can be set to a directory in your personal scratch space in `/atlas_scratch` if working on Atlas.

`CORDEX_DIR`

The directory containing bias-corrected CMIP5 CORDEX data from Stantec. If you have a copy of this available on scratch space, or if you have the time to copy the data to scratch space for processing, supply that path for increased performance. 

* default value: `/atlas_scratch/kmredilla/AK_CORDEX`

#### Structure

This project involves a fair bit of production of visual products for summarization of the various indices, particularly at key locations. So the first step is to derive the indices from the base data an an annual time scale, and all other summarization/visualization tasks will depend on that dataset. 

The main pipeline for deriving the dataset of indices exists in the root folder of this project and is controlled with the `process_indices.ipynb` notebook. 

The various sumarization tasks are carried out using the other notebooks in the root folder:

* `extract_indices.ipynb`: Make point extractions from the annual indices dataset for some points of interest
* `initial_summary.ipynb`: This notebook derives some summary bar charts using the base data, not the indices dataset
* `location_summary_plots.ipynb`: Make bar charts using the indices extracted for the points of interest for decadal and 30-year periods 

#### Commands

There is currently one "command" available for this project:

```
anaconda-project run process_indices
```

This opens the notebook that can be used to derive the indices from the base climate data.

Opening the remaining notebooks can be done using the same Jupyter instance started from that command, or by simply running:

```
anaconda-project run jupyter lab
```

To open a Jupyter Lab instance on port 8888.

Note - if the above commands are run on a remote machine such as Atlas, port-forwarding can be used to access the Jupyter notebook or Lab servers. 
