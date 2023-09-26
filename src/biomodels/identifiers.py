from __future__ import annotations

import json
import urllib.request
from typing import Literal, Sequence

from .common import base_url


def _get_all_identifiers(*, format: Literal["json", "xml"]):
    url = f"{base_url}/model/identifiers?format={format}"
    return urllib.request.urlopen(url)


def get_all_identifiers() -> Sequence[str]:
    data = _get_all_identifiers(format="json")
    return json.load(data)["models"]
