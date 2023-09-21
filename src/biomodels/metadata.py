import json
from pathlib import Path
from typing import overload

from pydantic import BaseModel, ConfigDict, Field

from .common import as_table, base_url, cache_path, fix_id, pooch


class File(BaseModel):
    name: str
    description: str = "main"
    size: int = Field(alias="fileSize")
    _model_id: str


class Metadata(BaseModel):
    model_id: str
    files: list[File]

    model_config = ConfigDict(protected_namespaces=())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for file in self.files:
            file._model_id = self.model_id

    def __repr__(self):
        return as_table(
            self.files,
            attributes=File.model_fields.keys(),
        )

    def _repr_html_(self):
        return as_table(
            self.files,
            attributes=File.model_fields.keys(),
            tablefmt="html",
        )

    def __getitem__(self, item):
        return self.files[item]

    def __iter__(self):
        return self.files.__iter__()


def get_metadata(model_id: str, *, known_hash: str | None = None) -> Metadata:
    model_id = fix_id(model_id)
    path = pooch.retrieve(
        f"{base_url}/model/files/{model_id}?format=json",
        known_hash=known_hash,
        fname=model_id,
        path=Path(cache_path, "model", "files"),
    )
    with open(path) as f:
        data = json.load(f)

    return Metadata(model_id=model_id, files=[*data["main"], *data["additional"]])


@overload
def get_file(
    file: str,
    *,
    model_id: str,
    known_hash: str | None = None,
) -> Path:
    ...


@overload
def get_file(
    file: File,
    *,
    model_id: None = None,
    known_hash: str | None = None,
) -> Path:
    ...


def get_file(
    file,
    *,
    model_id=None,
    known_hash=None,
) -> Path:
    if isinstance(file, File):
        model_id = file._model_id
        file = file.name
    elif model_id is None:
        raise TypeError("must provide model_id if file is a `str`")

    path = pooch.retrieve(
        f"{base_url}/model/download/{model_id}?filename={file}",
        known_hash=known_hash,
        fname=file,
        path=Path(cache_path, "model", "download", model_id),
    )
    return Path(path)
