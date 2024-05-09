# Python analysis project #

This is a project template powered by [Cookiecutter][] for use with
[datakit-project][] and similar workflows.

[Cookiecutter]: https://www.cookiecutter.io/
[datakit-project]: https://github.com/associatedpress/datakit-project

## Structure ##

```
.
├── README.md
├── analysis
│   └── archive
├── data
│   ├── handmade
│   ├── processed
│   └── source
├── etl
├── publish
└── scratch
```

*   `README.md`

    *   Project-specific introductory documentation.

*   `analysis`

    *   All Jupyter notebooks and other executable files that contain analysis
        for the project.

        *   Notebooks in this folder can ingest data from either `data/source`
            (if that data comes from the source in a workable format) or
            `data/processed` (if the data required some prep).

        *   Dataframes from analysis notebooks should be written out to
            `data/processed`.

    *   Note that only `.qmd` linked to `.ipynb` via [Jupytext][] are commited.
        Original `.ipynb` files are in the `.gitignore` because `.ipynb`
        metadata frequently disrupts version control whenever a notebook is
        opened or interacted with; `.qmd` files only keep track of code.

    *   `analysis/archive`

        *   Notebooks that leave the scope of the project but should also
            remain easily accessible.

*   `data`

    *   `data/handmade`

        *   Data that has been manually altered (e.g., Excel workbooks with
            inconsistent string errors requiring eyes on every row) or manually
            created (e.g., crosswalks and other types of lookup tables).

    *   `data/processed`

        *   Data that has either been transformed from an `etl` script or
            output from an `analysis` notebook.

    *   `data/source`

        *   Raw, untouched data directly from its source.

*   `etl`

    *   Scripts or notebooks involved with collecting data and prepping it for
        analysis.

*   `publish`

    *   Documents in the project that will be visible to the public.

*   `scratch`

    *   Files that will not be used in the project in its final form, such as
        filtered tables or quick visualizations for reporters.

    *   This directory is not tracked in Git.

[Jupytext]: https://jupytext.readthedocs.io/

## Usage ##

*   Create a project:

    *   Assuming you're working with [Cookiecutter][] directly:

        ```sh
        cookiecutter 'gh:myersjustinc/cookiecutter-python-project'
        ```

    *   Or if you're using [AP DataKit][] and have [datakit-project][]
        installed:

        ```sh
        datakit project create --template 'gh:myersjustinc/cookiecutter-python-project'
        ```

*   `cd` into your new project.

*   Set up paths that are specific to your machine, and go ahead and set up
    Jupyter and other dependencies:

    ```sh
    pipenv run ./run_me_first.py
    ```

*   To open up a [JupyterLab][] environment and get to work, run:

    ```sh
    pipenv run jupyter lab
    ```

[AP DataKit]: https://datakit.ap.org/
[JupyterLab]: https://jupyterlab.readthedocs.io/

## Prerequisites ##

*   [Python][], of course
*   [pipenv][], for project-level package management
*   [Quarto][], for notebook rendering

[Pipenv]: https://pipenv.pypa.io/
[Python]: https://www.python.org/
[Quarto]: https://quarto.org/
