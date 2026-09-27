"""Utility for palindrome checking.

The :func:`is_palindrome` function determines whether a given string reads the same
forward and backward when ignoring spaces, punctuation, and character case.
"""

from __future__ import annotations


def _normalize(text: str) -> str:
    """
    Return a case‑folded string containing only alphanumeric characters from *text*.

    This helper strips out spaces, punctuation and any other non‑alphanumeric symbols,
    then applies :meth:`str.casefold` for locale‑independent case‑insensitive comparison.
    """
    return "".join(ch.casefold() for ch in text if ch.isalnum())


def _is_palindrome_two_pointer(normalized: str) -> bool:
    """
    Check palindrome using a two‑pointer technique on the already normalized string.

    Parameters
    ----------
    normalized : str
        The string that has been stripped of non‑alphanumerics and case‑folded.

    Returns
    -------
    bool
        ``True`` if *normalized* reads the same forward and backward, ``False`` otherwise.
    """
    left, right = 0, len(normalized) - 1
    while left < right:
        if normalized[left] != normalized[right]:
            return False
        left += 1
        right -= 1
    return True


def is_palindrome(s: str) -> bool:
    """
    Check whether *s* is a palindrome, ignoring spaces, punctuation, and case.

    Parameters
    ----------
    s : str
        The string to test.

    Returns
    -------
    bool
        ``True`` if *s* is a palindrome under the described rules, ``False`` otherwise.

    Raises
    ------
    TypeError
        If *s* is not an instance of :class:`str`.

    Examples
    --------
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("Hello, World!")
    False
    >>> is_palindrome("")
    True
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected a string (str), got {type(s).__name__}")

    cleaned = _normalize(s)
    return _is_palindrome_two_pointer(cleaned)


__all__ = ("is_palindrome",)