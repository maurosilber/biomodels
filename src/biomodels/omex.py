import zipfile

from pydantic_xml import BaseXmlModel, attr, element

from .common import as_table, base_url, cache_path, fix_id, pooch


class Content(BaseXmlModel, tag="content"):
    location: str = attr()
    format: str = attr()
    master: bool = attr()


class Manifest(
    BaseXmlModel,
    tag="omexManifest",
    nsmap={"": "http://identifiers.org/combine.specifications/omex-manifest"},
):
    contents: list[Content] = element()
    _model_id: str
    _zipfile: zipfile.Path

    def __getitem__(self, item: int | str) -> zipfile.Path:
        if isinstance(item, int):
            c = self.contents[item]
            return self._zipfile / c.location
        elif isinstance(item, str):
            raise NotImplementedError
        else:
            raise TypeError("must be int or str")

    @property
    def master(self):
        for c in self.contents:
            if c.master:
                return self._zipfile / c.location
        raise ValueError("No naster file in this manifest")

    def __repr__(self):
        return as_table(
            self.contents,
            attributes=Content.model_fields.keys(),
        )

    def _repr_html_(self):
        return as_table(
            self.contents,
            attributes=Content.model_fields.keys(),
            tablefmt="html",
        )


def get_omex(model_id: str, *, known_hash: str | None = None) -> Manifest:
    """Get OMEX file from BioModels.

    The file is cached in the user's cache directory.

    >>> get_omex("BIOMD0000000001")

    No need to fill leading zeros:
    >>> get_omex("BIOMD1") == get_omex("BIOMD0000000001")
    True
    """
    model_id = fix_id(model_id)

    url = f"{base_url}/model/download/{model_id}"
    path = pooch.retrieve(
        url,
        known_hash=known_hash,
        fname=model_id,
        path=cache_path / "omex",
        progressbar=True,
    )
    file = zipfile.Path(path)
    xml = (file / "manifest.xml").read_bytes()
    manifest = Manifest.from_xml(xml)
    manifest._model_id = model_id
    manifest._zipfile = file
    return manifest
