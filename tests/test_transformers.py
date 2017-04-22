from typing import Type, TypeVar

import pytest
from datapipelines import DataTransformer, PipelineContext

T = TypeVar("T")
F = TypeVar("F")


class SimpleDataTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    @transform.register(float, int)
    def float_to_int(self, value, context: PipelineContext = None):
        return int(value)

    @transform.register(int, float)
    def int_to_float(self, value, context: PipelineContext = None):
        return float(value)

    @transform.register(str, int)
    def str_to_int(self, value, context: PipelineContext = None):
        return int(value)

    @transform.register(str, float)
    def str_to_float(self, value, context: PipelineContext = None):
        return float(value)


########################
# Unsupported Function #
########################

def test_unsupported():
    from datapipelines import UnsupportedError

    unsupported = DataTransformer.unsupported(int, 0.0)
    assert type(unsupported) is UnsupportedError

    unsupported = DataTransformer.unsupported(float, 0)
    assert type(unsupported) is UnsupportedError

    unsupported = DataTransformer.unsupported(str, None)
    assert type(unsupported) is UnsupportedError


#######################
# Transforms Function #
#######################

def test_transforms():
    transformer = SimpleDataTransformer()

    assert transformer.transforms == {
        int: {float},
        float: {int},
        str: {int, float}
    }


######################
# Transform Function #
######################

def test_transform():
    transformer = SimpleDataTransformer()

    value = 0
    assert type(transformer.transform(float, value)) is float

    value = 0.0
    assert type(transformer.transform(int, value)) is int

    value = "0"
    assert type(transformer.transform(int, value)) is int
    assert type(transformer.transform(float, value)) is float


def test_transform_unsupported():
    from datapipelines import UnsupportedError
    transformer = SimpleDataTransformer()

    value = 0
    with pytest.raises(UnsupportedError):
        transformer.transform(str, value)