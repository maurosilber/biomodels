import zipfile
from typing import Sequence

from pytest import raises

from .. import get_all_identifiers, get_file, get_metadata, get_omex


def test_get_all_identifiers():
    identifiers = get_all_identifiers()

    assert isinstance(identifiers, Sequence)

    id = identifiers[0]
    assert isinstance(id, str)
    assert len(id) == 15
    assert id.startswith(("BIOMD", "MODEL"))


def test_get_file_from_str():
    with raises(TypeError, match="id"):
        get_file("BIOMD0000000012_url.xml")  # type: ignore

    file = get_file("BIOMD0000000012_url.xml", model_id="BIOMD12")
    assert file.name == "BIOMD0000000012_url.xml"
    assert file.stat().st_size == 46274


def test_get_file_from_metadata():
    metadata = get_metadata("BIOMD12")
    file = get_file(metadata[0])
    assert file.name == "BIOMD0000000012_url.xml"
    assert file.stat().st_size == 46274


def test_get_metadata():
    metadata = get_metadata("BIOMD12")

    assert len(metadata) == 11

    file = metadata[0]
    assert file.name == "BIOMD0000000012_url.xml"
    assert file.description == "main"
    assert file.size == 46274


def test_get_omex():
    omex = get_omex("BIOMD12")

    # this OMEX file includes 5 more files than the metadata
    #            BIOMD0000000012 -> the OMEX file itself
    #               manifest.xml
    #               metadata.rdf
    # BIOMD0000000012_manual.png
    # BIOMD0000000012_manual.svg
    assert len(omex) == 11 + 5

    file = omex[0]
    assert isinstance(file, zipfile.Path)

    master_file = omex.master
    assert isinstance(master_file, zipfile.Path)
    assert master_file.name == "BIOMD0000000012_url.xml"
    assert len(master_file.read_bytes()) == 46274
