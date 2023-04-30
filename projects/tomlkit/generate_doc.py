from random import randint, uniform, getrandbits, seed
from typing import Tuple, Callable
import sys
from string import ascii_uppercase, ascii_lowercase, digits
import datetime
import atheris
import sys

import dictgen
import tomlkit

def func_name(f):
    def f2(*args,**kw):
        print('Called by: ',f.__name__)
        return f(*args,**kw)
    return f2


def generate(
    val_generators=None,
    nested_generators=None,
    max_height: int = 3,
    max_depth: int = 3,
    rand_seed: int = None,
    result=None,
):
    """
    Generate a random dictionary.

    :param max_height: Maximum number of keys at a level in the dictionary
    :param max_depth: Maximum depth of generated dictionary
    """

    # Validation Logic
    if max_height < 1 or max_depth < 1:
        raise AttributeError("max_height and max_depth must be greater than 0")

    if rand_seed:
        seed(rand_seed)

    # Create a random list of generators
    if max_depth > 1:
        all_generators = val_generators + nested_generators
    else:
        all_generators = val_generators
    generator_tuples = []
    for i in range(randint(0, max_height)):
        generator_tuples.append((all_generators[randint(0, len(all_generators) - 1)],))

    for (val_gen,) in generator_tuples:
        if max_depth > 1:
            try:
                result.add(*val_gen(
                    max_height=max_height,
                    max_depth=max_depth,
                    val_generators=val_generators,
                    nested_generators=nested_generators,
                ))
            except tomlkit.exceptions.KeyAlreadyPresent: # Deal with duplicate keys
                pass
        else:
            result.add(*val_gen())

    return result


def random_comment(**kwargs):
    return (tomlkit.comment(dictgen.random_string()),)


def random_nl(**kwargs):
    return (tomlkit.nl(),)


def random_title(**kwargs):
    return dictgen.random_string(), dictgen.random_string()


def random_datetime(**kwargs):
    return dictgen.random_string(), tomlkit.datetime(dictgen.random_datetime())


def random_int(**kwargs):
    return dictgen.random_string(), tomlkit.integer(dictgen.random_int())


def random_table(
    val_generators,
    nested_generators,
    max_height,
    max_depth,
    **kwargs
):
    all_generators = val_generators + nested_generators
    # Create a random list of generators
    generators = []
    for i in range(randint(0, max_height)):
        # If we are at a top level depth don't allow any nested generators
        if max_depth > 2:
            generators.append(all_generators[randint(0, len(all_generators) - 1)])
        else:
            generators.append(val_generators[randint(0, len(val_generators) - 1)])
    
    result = tomlkit.table()

    for generator in generators:
        new_val = generator(
            max_height=max_height,
            max_depth=max_depth - 1,
            val_generators=val_generators,
            nested_generators=nested_generators,
        )
        result.add(*new_val)

    return dictgen.random_string(), result

def test_one_input(input_bytes: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(input_bytes)
    random_doc = generate(
        max_height=10,
        max_depth=4,
        val_generators=(random_comment, random_nl, random_title, random_datetime, random_int),
        nested_generators=(random_table,),
        result=tomlkit.document(),
        rand_seed=fdp.ConsumeInt(32)
    )

def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()