# -*- coding: utf-8  -*-
"""Family module for test.wikipedia.org."""
__version__ = '$Id$'

from pywikibot import family


# The test wikipedia family
class Family(family.WikimediaFamily):

    """Family class for test.wikipedia.org."""

    def __init__(self):
        super(Family, self).__init__()
        self.name = 'test'
        self.langs = {
            'test': 'test.wikipedia.org',
        }

    def from_url(self, url):
        return None  # Don't accept this, but 'test' of 'wikipedia'
