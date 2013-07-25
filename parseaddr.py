# Author: Alexey Bogdanenko
# Contact: alexey@bogdanenko.com
# works with python 3.2 and older

import re

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

    # extract local and domain parts
    local_part, sep, domain_part = text.partition('@')
    if not local_part or not domain_part:
        # either local part or domain part is missing
        return 1   

    # parse domain part
    if not 3 <= len(domain_part) <= 256:
        # domain part is too short or too long
        return 2
    subdomain_regex = re.compile('[a-z0-9_-]+\Z')
    for subdomain in domain_part.split('.'):
        if not subdomain_regex.match(subdomain):
            # illegal character in domain part
            return 2
        if subdomain.startswith('-') or subdomain.endswith('-'):
            # subdomain must not start with dash or end with dash
            return 3

    # parse local part
    if '..' in local_part:
        # consecutive dots in local part are not allowed
        return 5

    """
    Check if Rules 4, 6, 7 are satisfied
    Algorithm:
        Split (without overlaps) local_part so that resulting list looks like
        this: 

            [N, Q, N, ..., Q, N],

        where Q represents string two or more characters long that starts and
        ends with double quotes (i.e. matches quoted_regex) and N contains less
        than two quotation marks.

        Then split the list into two lists with even and odd elements:

            [N, N, ..., N]
            [Q, ..., Q]

        and check for illegal characters inside strings of each list.
    """
    if len(local_part) > 128:
        # local part is too long
        return 4

    quoted_regex = re.compile('(".*?")')  # non-greedy match
    inside_quotes_regex = re.compile('[!,:a-z0-9._-]*\Z')
    outside_quotes_regex = re.compile('[a-z0-9._-]*\Z') 
    local_part_tokens = quoted_regex.split(local_part)    

    for x in local_part_tokens[::2]:  # even elems
        if '"' in x:
            # missing closing quote in local part
            return 6
        if not inside_quotes_regex.match(x):
            # illegal character in local part
            return 4
        if not outside_quotes_regex.match(x):
            # punctuation characters "!,:" must be inside quotes
            return 7

    for x in local_part_tokens[1::2]:  # odd elems
        x = x[1:-1]  # strip quotes
        if not inside_quotes_regex.match(x):
            # illegal character in local part
            return 4

    # success, text represents a valid email address
    return 0
