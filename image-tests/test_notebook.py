#!/usr/bin/env python3
import nbformat
import os
from nbclient import NotebookClient
from pathlib import Path


def run_notebook(notebook_path: str) -> bool:
    """
    Executes all cells in a Jupyter notebook and saves the output back to the same file.

    Args:
        notebook_path (str): The path to the notebook file to execute.

    Returns:
        bool: True if the notebook executed successfully, False otherwise.
    """
    try:
        notebook = nbformat.read(notebook_path, as_version=4)
    except FileNotFoundError:
        return False

    client = NotebookClient(
        notebook,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(Path(notebook_path).parent)}},
    )

    try:
        notebook = client.execute()
    except Exception:
        return False

    return True


def test_all_notebooks_execute():
    notebook_dir = Path("image-tests/notebooks")
    notebook_files = sorted(notebook_dir.glob("*.ipynb"))

    # If no notebooks exist, the test passes.
    if not notebook_files:
        return

    for nb_path in notebook_files:
        assert run_notebook(str(nb_path)), f"Notebook failed: {nb_path.name}"


if __name__ == "__main__":
    test_all_notebooks_execute()

