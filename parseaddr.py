# Author: Alexey Bogdanenko
# Contact: alexey@bogdanenko.com
# works with python 3.2 and older

"""Email address parser"""

def parse_email_addr(text):
    """Check if text represents a valid email address.
    text is considered a valid email address if and only if it complies with
    The Rules given in the problem description (ommitted here for brevity).
    
    Args:
        text: a string.

    Returns:
        If text represents a valid email address, returns 0, otherwise, returns
        number of the first rule text doesn't comply with. For example:
        >>> parse_email_addr('jsmith@example.com')
        0
        >>> parse_email_addr('double..dots@example.com')
        5

    Raises:
        TypeError: if text is some random object and not a string (inherited
            from a string)
    """
    
    if not isinstance(text, str):
        raise TypeError('expecting a string')
    pass
