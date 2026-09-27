"""Utility for palindrome checking.

The :func:`is_palindrome` function determines whether a given string reads the same
forward and backward when spaces, punctuation, and case differences are ignored.
"""

__all__ = ["is_palindrome"]


def _normalize(text: str) -> str:
    """
    Return a lowercase string containing only alphanumeric characters from *text*.

    This helper removes spaces, punctuation and any other non‑alphanumeric symbols,
    then lower‑cases the remaining characters so that the palindrome check is
    case‑insensitive.

    Parameters
    ----------
    text: str
        The original string to be normalized.

    Returns
    -------
    str
        Normalized representation of *text*.
    """
    return "".join(ch.lower() for ch in text if ch.isalnum())


def is_palindrome(s: str) -> bool:
    """
    Check whether *s* is a palindrome, ignoring spaces, punctuation and case.

    The function accepts only string inputs; any other type raises a :class:`TypeError`.
    An empty string (or a string that becomes empty after normalization) is considered
    a palindrome.

    Parameters
    ----------
    s: str
        The value to be tested.

    Returns
    -------
    bool
        ``True`` if *s* is a palindrome under the described rules, ``False`` otherwise.

    Raises
    ------
    TypeError
        If *s* is not an instance of :class:`str`.
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected a string, got {type(s).__name__!r}")

    left, right = 0, len(s) - 1
    while left < right:
        # Move left pointer to the next alphanumeric character
        while left < right and not s[left].isalnum():
            left += 1
        # Move right pointer to the previous alphanumeric character
        while left < right and not s[right].isalnum():
            right -= 1
        if left < right:
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
    return True


if __name__ == "__main__":
    examples = [
        "A man, a plan, a canal: Panama",
        "No lemon, no melon",
        "Hello, World!",
        "",
        "!!!",
        "Was it a car or a cat I saw?",
    ]

    for txt in examples:
        result = is_palindrome(txt)
        print(f"{txt!r:40} -> {result}")