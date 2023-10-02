# BioModels

`biomodels` is a Python library to download models from [BioModels](https://www.ebi.ac.uk/biomodels/).
Models are cached locally in the OS user cache directory,
so they will not be redownloaded every time.

## Usage

### Get model metadata

The first time we download a file,
it will let us know that it is being downloaded
and cached locally.

```python
>>> import biomodels
>>> metadata = biomodels.get_metadata("BIOMD0000000012")  # doctest: +SKIP
Downloading data from 'https://www.ebi.ac.uk/biomodels/model/files/BIOMD0000000012?format=json' to file '.../Caches/biomodels/model/files/BIOMD0000000012'.
SHA256 hash of downloaded file: ...
Use this value as the 'known_hash' argument of 'pooch.retrieve' to ensure that the file hasn't changed if it is downloaded again in the future.
```

Later, this file will get fetched from the local cache,
instead of being redownloaded.

```python
>>> metadata = biomodels.get_metadata("BIOMD12")  # no need to input the leading zeros
>>> metadata
    name                         description                            size
--  ---------------------------  -----------------------------------  ------
 0  BIOMD0000000012_url.xml      main                                  46274
 1  BIOMD0000000012-biopax2.owl  Auto-generated BioPAX (Level 2)       16748
 2  BIOMD0000000012-biopax3.owl  Auto-generated BioPAX (Level 3)       23577
 3  BIOMD0000000012.m            Auto-generated Octave file             4994
 4  BIOMD0000000012.pdf          Auto-generated PDF file              205156
 5  BIOMD0000000012.png          Auto-generated Reaction graph (PNG)   39018
 6  BIOMD0000000012.sci          Auto-generated Scilab file              154
 7  BIOMD0000000012.svg          Auto-generated Reaction graph (SVG)   35750
 8  BIOMD0000000012.vcml         Auto-generated VCML file              60183
 9  BIOMD0000000012.xpp          Auto-generated XPP file                4114
10  BIOMD0000000012_urn.xml      Auto-generated SBML file with URNs    47097
```

### Get a particular file

To get a particular file,
you can either pass the filename and model_id:

```python
>>> biomodels.get_file("BIOMD0000000012_url.xml", model_id="BIOMD12")
PosixPath('<CACHE_DIR>/biomodels/model/download/BIOMD0000000012/BIOMD0000000012_url.xml')
```

or choose one from the metadata:

```python
>>> path = biomodels.get_file(metadata[0])
>>> path
PosixPath('<CACHE_DIR>/biomodels/model/download/BIOMD0000000012/BIOMD0000000012_url.xml')
```

Then, you can use that `Path` object to load the file:

```python
>>> print(path.read_text())
<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level2/version3" metaid="_153818" level="2" version="3">
...
```

### Get COMBINE archive

If you are interested in all the model files,
it might be better to download the COMBINE archive,
which is a compressed file (260KB vs 500KB for this small model):

```python
>>> omex = biomodels.get_omex("BIOMD12")
>>> omex
    location                     format                                                                 master
--  ---------------------------  ---------------------------------------------------------------------  --------
 0  .                            https://identifiers.org/combine.specifications/omex                    False
 1  ./manifest.xml               https://identifiers.org/combine.specifications/omex-manifest           False
 2  ./metadata.rdf               https://identifiers.org/combine.specifications/omex-metadata           False
 3  BIOMD0000000012-biopax2.owl  https://identifiers.org/combine.specifications/biopax.level-2          False
 4  BIOMD0000000012-biopax3.owl  https://identifiers.org/combine.specifications/biopax.level-3          False
 5  BIOMD0000000012.m            https://purl.org/NET/mediatypes/application/x.unknown                  False
 6  BIOMD0000000012.pdf          https://purl.org/NET/mediatypes/application/pdf                        False
 7  BIOMD0000000012.png          https://purl.org/NET/mediatypes/image/png                              False
 8  BIOMD0000000012.sci          https://purl.org/NET/mediatypes/application/x.unknown                  False
 9  BIOMD0000000012.svg          https://purl.org/NET/mediatypes/application/xml                        False
10  BIOMD0000000012.vcml         https://purl.org/NET/mediatypes/application/xml                        False
11  BIOMD0000000012.xpp          https://purl.org/NET/mediatypes/application/x.unknown                  False
12  BIOMD0000000012_manual.png   https://purl.org/NET/mediatypes/image/png                              False
13  BIOMD0000000012_manual.svg   https://purl.org/NET/mediatypes/application/xml                        False
14  BIOMD0000000012_url.xml      https://identifiers.org/combine.specifications/sbml.level-2.version-3  True
15  BIOMD0000000012_urn.xml      https://identifiers.org/combine.specifications/sbml.level-2.version-3  False
```

We can select a particular file by indexing:

```python
>>> content = omex[14]
>>> content
Content(location='BIOMD0000000012_url.xml', format='https://identifiers.org/combine.specifications/sbml.level-2.version-3', master=True)
```

Then,
you can get a `zipfile.Path` object with the `Content.path` attribute,
and read the contents from the OMEX file:

```python
>>> print(content.path.read_text())
<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level2/version3" metaid="_153818" level="2" version="3">
...
```

## Installation

```
pip install biomodels
```

## Development

We are using pytest for testing,
and pre-commit hooks to format and lint the codebase.

To easily set-up a development environment,
run the following commands:

```
git clone https://github.com/maurosilber/biomodels
cd biomodels
conda env create --file environment-dev.yml
pre-commit install
```

which assume you have git and conda preinstalled.
