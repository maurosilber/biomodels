from __future__ import annotations

from typing import Iterable, Mapping

import pooch
from tabulate import TableFormat, tabulate

base_url = "https://www.ebi.ac.uk/biomodels"
cache_path = pooch.os_cache("biomodels")


def fix_id(model_id: str) -> str:
    """Adds leading zeros to BioModels ID"""
    if len(model_id) == 15:
        return model_id

    model_type, model_number = model_id[:5], model_id[5:]
    return f"{model_type}{model_number:>010}"


def as_table(
    iterable,
    *,
    attributes: Iterable[str] | Mapping[str, str],
    tablefmt: TableFormat | str = "simple",
    index: Iterable[str] | bool = True,
):
    if isinstance(attributes, Mapping):
        headers = attributes.values()
    else:
        headers = attributes = list(attributes)

    return tabulate(
        [[getattr(c, k) for k in attributes] for c in iterable],
        headers=list(headers),
        tablefmt=tablefmt,
        showindex=index,
    )
