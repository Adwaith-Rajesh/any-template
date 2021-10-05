# How to contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

First, read these guidelines.

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Before you begin making changes, state your intent to do so in an Issue.
Then, fork the project and create a new branch. Make changes in your copy of the repository.
Then open a pull request once your changes are ready.

## Code style

The project follows a convention of:

- Maximum line length: 120 characters
- Use reorder-python-imports
- Use autopep8, flake8
- Strict PEP8 conventions.
- Completely type hinted and verified using mypy
- No type comments
- Three double quotes around docstrings.

All theses can be done using pre-commit. To use pre-commit on this project run the following commands after forking the repo.

```commandline
pip install -r requirements-dev.txt
```

```commandline
pre-commit install
```

This will enforce all the code styling before you commit.

## Template Schema

When creating a new schema please follow these guidelines.

```json
{
	"folders": [], // list of the folders that needs to be created,
	"files": [], // list of the all the files that needs to created,
	"files_with_contents": {
		"filename": "url"
	} // and object where the name of the file maps to the url where the
	// can be found
}

// all these fields are necessary even if they are empty
```
