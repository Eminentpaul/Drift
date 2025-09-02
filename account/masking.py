def mask(acctno):
    prefix = acctno[:2]
    suffix = acctno[-2:]

    return f'{prefix}{'*' * 6}{suffix}'