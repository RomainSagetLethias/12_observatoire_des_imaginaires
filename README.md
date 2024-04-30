# Observatoire des imaginaires

## Installing with poetry

### Prerequisites:

1. Python (≥ `3.10`) installed on your system.
2. Ensure you have `poetry` installed. If not, you can install them using `pip`.

```bash
pip install poetry
```

### Steps:

1. **Clone the GitHub Repository:**

   Clone the GitHub repository you want to install locally using the `git clone` command.

   ```bash
   git clone https://github.com/dataforgoodfr/12_observatoire_des_imaginaires.git
   ```

2. **Navigate to the Repository Directory:**

   Use the `cd` command to navigate into the repository directory.

   ```bash
   cd 12_observatoire_des_imaginaires/
   ```

3. **Configure `poetry` to create a Virtual Environment inside the project:**

   Ensure that poetry will create a `.venv` directory into the project with the command:

   ```bash
   poetry config virtualenvs.in-project true
   ```

4. **Install Project Dependencies using `poetry`:**

   Use `poetry` to install the project dependencies.

   ```bash
   poetry install
   ```

   This will read the `pyproject.toml` file in the repository and install all the dependencies specified.

5. **Activate the Virtual Environment:**

   Activate the virtual environment to work within its isolated environment.

   On Unix or MacOS:

   ```bash
   poetry shell
   ```

6. **Run & edit notebooks**:

   ```bash
   jupyter notebook
   ```

## Environment Variables

This code base uses a `.env` file at the root directory of the code base.

| Variable         | Description                                                         | Default Value |
| ---------------- | ------------------------------------------------------------------- | ------------- |
| HF_TOKEN         | Hugging Face API Token. You must have write access to the datasets. | N/A           |
| TMDB_API_KEY     | TMDB API Token.                                                     | N/A           |
| TMDB_BATCH_SIZE  | Number of TMDB entries to download before updating a HF dataset.    | 10000         |
| TMDB_MAX_RETRIES | Maximum number of times to retry a failed TMDB API call.            | 500           |

## Website to select a specific movie or TV show

The [observable](https://github.com/dataforgoodfr/12_observatoire_des_imaginaires/tree/main/site-observable) directory contains
an observable framework site that collect film and movie data from the above datasets on kaggle and filters the datasets according
to the following rules in order to reduced the size of the data present on the generated web site. This site provides a search UI
allow a user to select a specific movie or TV show. The user can then click on the link for their selection to kick off the
questionnaire on tally andis destined to be embedded in an iframe in the main Observatoire des Imaginaires web site.

Movies:

- filter out adult movies
- filter out movies released more that two years ago

TV Shows:

- filter out adult shows

The web site is currently hosted on the [Observable hosting platform](https://observablehq.com/) and is available at the following URL:

https://observatoire-des-imaginaires.observablehq.cloud/questionnaire

## Run precommit-hook locally

[Install precommits](https://pre-commit.com/)

    pre-commit run --all-files

## Use Tox to test your code

    tox -vv

## Tasks

This repo includes invoke for pythonic task execution. To see the
is of available tasks you can run:

```bash
invoke -l
```

###

To run the observable site in development mode you can run:

```bash
invoke dev
```

### Updating the Movie Dataset

The [French regional TMDB Movies Dataset](https://huggingface.co/datasets/DataForGood/observatoire_des_imaginaires_movies)
on Hugging Face can be updated using the following command:

```bash
invoke update-movies-dataset
```

### Updating the Series Dataset

The [French regional TMDB Series Dataset](https://huggingface.co/datasets/DataForGood/observatoire_des_imaginaires_series)
on Hugging Face can be updated using the following command:

```bash
invoke update-series-dataset
```
