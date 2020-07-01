# -*- coding: utf-8 -*-

from imio.urban.core.contents.parcel.interfaces import IParcel

from plone import api
from plone.dexterity.content import Item

from Products.urban import services

from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(IParcel)
class Parcel(Item):
    """
    Parcel dexterity class.
    """

    def Title(self):
        """
        """
        division = self.getDivisionName() or ''
        division = division.encode('utf-8')
        section = self.getSection()
        radical = self.getRadical()
        bis = self.getBis()
        exposant = self.getExposant()
        puissance = self.getPuissance()
        generatedTitle = str(division) + ' ' + str(section) + ' ' + str(radical) + ' ' + str(bis) + ' ' + str(exposant) + ' ' + str(puissance)
        generatedTitle = generatedTitle.strip().replace(' 0', '').replace(' _ ', ' ')
        if self.partie:
            generatedTitle = generatedTitle + ' (partie)'
        return generatedTitle

    def reference_as_dict(self, with_empty_values=False):
        """
        Return this parcel reference defined values as a dict.
        By default only return parts of the reference with defined values.
        If with_empty_values is set to True, also return empty values.
        """
        references = {
            'division': self.divisionCode,
            'section': self.section,
            'radical': self.radical,
            'bis': self.bis,
            'exposant': self.exposant,
            'puissance': self.puissance,
        }
        if not with_empty_values:
            references = dict([(k, v) for k, v in references.iteritems() if v])

        return references

    @property
    def divisionCode(self):
        """
        divisionCode should return the division number
        """
        return self.getDivisionCode()

    def getDivisionCode(self):
        """
        DivisionCode should return the division number
        """
        return self.getDivision()

    def getDivision(self):
        return self.division or '00000'

    def getDivisionName(self):
        division_names = getUtility(
            IVocabularyFactory,
            name='urban.vocabularies.division_names'
        )(self)
        if self.division in division_names.by_value:
            voc_term = division_names.getTerm(self.division)
            return voc_term.title
        else:
            return self.division

    def getDivisionAlternativeName(self):
        division_names = getUtility(
            IVocabularyFactory,
            name='urban.vocabularies.division_alternative_names'
        )(self)
        if self.division in division_names.by_value:
            voc_term = division_names.getTerm(self.division)
            return voc_term.title
        else:
            return self.division

    def getSection(self):
        return self.section or '_'

    def getRadical(self):
        return self.radical or '0'

    def getBis(self):
        return self.bis or '0'

    def getExposant(self):
        return self.exposant or '_'

    def getPuissance(self):
        return self.puissance or '0'

    def getPartie(self):
        return self.partie or False

    def getIsOfficialParcel(self):
        return self.isOfficialParcel

    def getOutdated(self):
        return self.outdated

    def getRelatedLicences(self, licence_type=''):
        catalog = api.portal.get_tool('portal_catalog')
        licence = self.aq_parent
        capakey = self.get_capakey()
        brains = []
        if licence_type:
            brains = catalog(portal_type=licence_type, parcelInfosIndex=capakey)
        else:
            brains = catalog(parcelInfosIndex=capakey)
        return [brain for brain in brains if brain.id != licence.id]

    def getCSSClass(self):
        if self.getOutdated():
            return 'outdated_parcel'
        elif not self.getIsOfficialParcel():
            return 'manual_parcel'
        return ''

    def get_capakey(self):
        capakey = "%s%s%04d/%02d%s%03d" % (
            self.getDivisionCode(),
            self.getSection(),
            int(self.getRadical()),
            int(self.getBis()),
            self.getExposant(),
            int(self.getPuissance())
        )
        return capakey

    @property
    def capakey(self):
        return self.get_capakey()

    def get_historic(self):
        """
        Return the "parcel historic" object of this parcel
        """
        session = services.cadastre.new_session()
        historic = session.query_parcel_historic(self.capakey)
        session.close()
        return historic
