# Data Processing codebase for Two Bears Environmental Consulting collaboration

This codebase contains all of the data pipelines for the Two Bears Environmental Consulting (TBEC) collaboration, with which SNAP is responsible for various "processing" tasks (quotes because it's sort of TBD), such as computing summaries of extreme weather events from various datasets.

## Running the pipelines in this codebase

This codebase is set up to work with [Anaconda Project](https://anaconda-project.readthedocs.io/en/latest/), the conda-based dependency management system.

To run any of the pipelines here, which are set up as Jupyter notebooks, simply install Anaconda or Miniconda, and install Anaconda Project via `conda install anaconda-project` if you do not have it (it comes with Anaconda v4.3.1 and later by default).

Once you have Anaconda Project installed, running any of the notebooks with all required dependencies is as simple as:

```sh
anaconda-project run <command>
```

where `<command>` should be replaced by any of the available commands below. Running this command will ensure that all dependencies are installed. 

### Environment variables

The environment variables required for this project have the following default values:

```sh
BASE_DIR=/workspace/Shared/Tech_Projects/TBEC_CMIP5_Processing/project_data
OUTPUT_DIR=/workspace/Shared/Tech_Projects/TBEC_CMIP5_Processing/final_products
```

### Commands

Here are the available commands for this project:

- `initial_summary`: notebook that derives a summary figure for the June 2022 progress report, demonstrating SNAP's retrieval and use of the bias-corrected CORDEX data from Stantec.
- `remote_lab`: This command can be used to start a Jupyter Lab instance with the root directory of the project as the working directory.

Note - if the above commands are run on a remote machine such as Atlas, port-forwarding can be used to access the Jupyter notebook or Lab servers. 

