import functools
from numbers import Number
import inflect


@functools.lru_cache(maxsize=20)
def number_to_name(
    number: Number,
    spaces: str = " ",
    want_list: bool = False,
    comma: str = ",",
    *args,
    **kwargs
) -> str | list[str]:
    """
    Converts a number to its corresponding word representation.

    Args:
        number (Number): The number to be converted.
        spaces (str, optional): The character used to replace spaces in the word representation. Defaults to " ".
        want_list (bool, optional): If True, returns a list of words instead of a single string. Defaults to False.
        *args: Extra arguments for number_to_words.
        **kwargs: Keyword arguments for number_to_words.

    Returns:
        str | list[str]: The word representation of the number. If want_list is True, returns a list of words.

    """
    p = inflect.engine()
    word = p.number_to_words(number, *args, comma=comma, wantlist=want_list, **kwargs)
    if isinstance(word, str):
        word = word.replace("-", spaces).replace(" ", spaces).replace(",", comma)

    return word
