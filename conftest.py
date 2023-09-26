"""Autogenerating test for README"""

from typing import Callable

from biomodels.common import cache_path

path = str(cache_path.parent)


def process(line: str) -> str:
    return line.replace("<CACHE_DIR>", path)


def extract_code(infile: str, outfile: str, *, process: Callable[[str], str]):
    with open(infile) as readme, open(outfile, "w") as out:
        lines = iter(readme)
        for line in lines:
            if line.startswith("```python"):
                while not (line := next(lines)).startswith("```"):
                    line = process(line)
                    out.write(line)


extract_code("README.md", "test_readme.txt", process=process)
