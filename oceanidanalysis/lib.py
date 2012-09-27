"""
oceanidanalysis.lib
===================

Generally useful methods that span across submodules.

"""

def injectlocals(l, skip=['self','args','kwargs'], **kwargs):
    """Update a dictionary with another, skipping specified keys."""
    if l.has_key('kwargs') : kwargs.update(l['kwargs'])
    kwargs.update(dict((k, v) for k, v in l.items() if k not in skip))
    return kwargs

