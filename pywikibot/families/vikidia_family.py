# -*- coding: utf-8  -*-
"""Family module for Vikidia."""
__version__ = '$Id$'

from pywikibot import family


class Family(family.Family):

    """Family class for Vikidia."""

    def __init__(self):
        """Constructor."""
        family.Family.__init__(self)
        self.name = 'vikidia'

        self.langs = {
            'en': 'en.vikidia.org',
            'es': 'es.vikidia.org',
            'fr': 'fr.vikidia.org',
            'it': 'it.vikidia.org',
            'ru': 'ru.vikidia.org',
        }

        # Wikimedia wikis all use "bodyContent" as the id of the <div>
        # element that contains the actual page content; change this for
        # wikis that use something else (e.g., mozilla family)
        self.content_id = "bodyContent"

    def scriptpath(self, code):
        """The prefix used to locate scripts on this wiki.

        This is the value displayed when you enter {{SCRIPTPATH}} on a
        wiki page (often displayed at [[Help:Variables]] if the wiki has
        copied the master help page correctly).

        The default value is the one used on Wikimedia Foundation wikis,
        but needs to be overridden in the family file for any wiki that
        uses a different value.

        """
        return '/w'

    # Which version of MediaWiki is used? REQUIRED
    def version(self, code):
        """Return the version for this family."""
        return '1.23.1'

    def code2encoding(self, code):
        """Return the encoding for a specific language wiki."""
        # Most wikis nowadays use UTF-8, but change this if yours uses
        # a different encoding
        return 'utf-8'

    def protocol(self, code):
        """Return https as the protocol for this family."""
        return "https"

    def ignore_certificate_error(self, code):
        """Ignore certificate errors."""
        return True  # has self-signed certificate for a different domain.
