# -*- coding: utf-8 -*-
"""Tile implementation."""
from pkan.dcatapde.constants import MANDATORY_FOLDERS
from pkan.tiles import _
from plone import api
from plone import tiles
from plone.app.standardtiles import _PMF
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.supermodel.model import Schema
from zope import schema
from zope.component import queryUtility


class IPKANFolderTile(Schema):
    """A tile that shows Gists from GitHub."""

    tile_title = schema.TextLine(
        description=_PMF(
            u'The title will also be used to create identifying class on '
            u'that tile',
        ),
        required=True,
        title=_PMF(u'Title'),
    )

    show_title = schema.Bool(
        default=True,
        title=_PMF(u'Show tile title'),
    )

    title_level = schema.Choice(
        default=u'h2',
        required=False,
        title=_(u'Headline level'),
        values=(u'h1', u'h2', u'h3', u'h4', u'h5', u'h6'),
    )


class PKANFolderTile(tiles.Tile):
    """A tile that shows PKAN Folders."""

    @property
    def tile_id(self):
        return queryUtility(IIDNormalizer).normalize(
            self.data.get('tile_title'),
        )

    @property
    def tile_title(self):
        return self.data.get('tile_title')

    @property
    def show_title(self):
        return self.data.get('show_title')

    @property
    def title_level(self):
        return self.data.get('title_level') or u'h2'

    def folder(self):
        for folder_name, folder_type in MANDATORY_FOLDERS.items():
            results = api.content.find(**{'portal_type': folder_type,
                                          'title': folder_name})
            yield {
                'label': folder_name,
                'url': results[0].getObject().absolute_url(),
            }
