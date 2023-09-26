from pytest import mark

from ..common import fix_id


@mark.parametrize(
    "model_id",
    [
        "BIOMD12",
        "BIOMD012",
        "BIOMD0000000012",
    ],
)
def test_fix_id(model_id):
    fixed_id = fix_id(model_id)

    assert len(fixed_id) == 15
    assert fixed_id == "BIOMD0000000012"
