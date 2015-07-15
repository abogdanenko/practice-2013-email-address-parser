# Email address parser
Module *parseaddr* contains function *parse_email_addr* that checks if text
represents a valid email address.

Text is considered a valid email address if and only if it complies with The
Rules given in the problem description (ommitted here for brevity).

Function *parse_email_addr* returns 0 if text represents a valid email address,
otherwise, it returns number of the first rule text doesn't comply with.

For example:
```
>>> parse_email_addr('jsmith@example.com')
    0
>>> parse_email_addr('double..dots@example.com')
    5
```

To run unit tests, execute program *parsetest.py*.
