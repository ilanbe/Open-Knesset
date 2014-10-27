# encoding: utf-8

from okscraper.base import ParsingFromFileTestCase
from lobbyists.scrapers.lobbyist import LobbyistScraper
from lobbyists.scrapers.lobbyist_represent import LobbyistRepresentScraper
from lobbyists.scrapers.lobbyists_index import LobbyistsIndexScraper
from lobbyists.scrapers.lobbyist import LobbyistScraperDictStorage
from lobbyists.models import Lobbyist, LobbyistData, LobbyistRepresent
from django.core.exceptions import ObjectDoesNotExist

class LobbyistScraperDictStorage_withoutRepresents(LobbyistScraperDictStorage):

    def __init__(self, *args, **kwargs):
        self._represents_data = kwargs.pop('represents_data')
        super(LobbyistScraperDictStorage_withoutRepresents, self).__init__(*args, **kwargs)

    def _get_represents_data(self, source_id):
        return self._represents_data

class testLobbyistScraper(ParsingFromFileTestCase):

    def _getScraperClass(self):
        return LobbyistScraper

    def _getFilename(self):
        return 'View_lobbyist_<<id>>.xml'

    def _get_latest_data(self, lobbyist):
        return lobbyist.latest_data

    def testParsing(self):
        self.assertScrape(
            args=(220,),
            expectedData={
                'corporation_id': u'',
                'corporation_name': u'',
                'faction_member': u'לא',
                'faction_name': u'',
                'family_name': u'אביזוהר',
                'first_name': u'יותם',
                'id': u'220',
                'permit_type': u'קבוע',
                'profession': u''
            }
        )

    def testStorage(self):
        scraper = LobbyistScraper()
        scraper.source = self._getSource()
        scraper.storage = LobbyistScraperDictStorage_withoutRepresents(represents_data=[])
        lobbyist = scraper.scrape(220)
        self.assertEqual(lobbyist.source_id, u'220')
        self.assertEqual(lobbyist.person.name, u'יותם אביזוהר')
        self.assertEqual(self._get_latest_data(lobbyist).first_name, u'יותם')
        self.assertEqual(self._get_latest_data(lobbyist).family_name, u'אביזוהר')
        self.assertEqual(self._get_latest_data(lobbyist).profession, u'')
        self.assertEqual(self._get_latest_data(lobbyist).corporation_name, u'')
        self.assertEqual(self._get_latest_data(lobbyist).corporation_id, u'')
        self.assertEqual(self._get_latest_data(lobbyist).faction_member, u'לא')
        self.assertEqual(self._get_latest_data(lobbyist).faction_name, u'')
        self.assertEqual(self._get_latest_data(lobbyist).permit_type, u'קבוע')
        # now, if we scrape this lobbyist again, it will use the same object
        scraper = LobbyistScraper()
        scraper.source = self._getSource()
        scraper.storage = LobbyistScraperDictStorage_withoutRepresents(represents_data=[])
        lobbyist2 = scraper.scrape(220)
        lobbyist2_data = self._get_latest_data(lobbyist2)
        self.assertEqual(lobbyist, lobbyist2)
        self.assertEqual(self._get_latest_data(lobbyist), self._get_latest_data(lobbyist2))
        # now, same lobbyist but different represents
        scraper = LobbyistScraper()
        scraper.source = self._getSource()
        lobbyist_represent_1 = LobbyistRepresent.objects.create(source_id=u'1')
        lobbyist_represent_2 = LobbyistRepresent.objects.create(source_id=u'2')
        scraper.storage = LobbyistScraperDictStorage_withoutRepresents(represents_data=[
            lobbyist_represent_1, lobbyist_represent_2
        ])
        lobbyist3 = scraper.scrape(220)
        self.assertNotEqual(lobbyist2_data, self._get_latest_data(lobbyist3))


class testLobbyistRepresentScraper(ParsingFromFileTestCase):

    maxDiff = None

    def _getScraperClass(self):
        return LobbyistRepresentScraper

    def _getFilename(self):
        return 'lobbist_type_<<id>>.xml'

    def testParsing(self):
        self.assertScrape(
            args=(220,),
            expectedData=[
                {
                    'domain': u'איכות הסביבה, בריאות הציבור, בטיחות בדרכים',
                    'id': u'6954817',
                    'lobbyist_id': u'220',
                    'name': u'ישראל בשביל אופניים',
                    'type': u'קבוע',
                },{
                    'id': u'6954818',
                    'lobbyist_id': u'220',
                    'name': u'אופנים בשביל ירושלים',
                    'type': u'קבוע',
                    'domain': u'תחבורה, התחדשות עירונית, בטיחות בדרכים',
                }
            ]
        )


class testLobbyistsIndexScraper(ParsingFromFileTestCase):

    maxDiff = None

    def _getScraperClass(self):
        return LobbyistsIndexScraper

    def testParsingSingle(self):
        self.assertScrape(
            filename='lobbyists_index_only220.html',
            expectedData=[u'220',]
        )

    def testParsing(self):
        self.assertScrape(
            filename='lobbyists_index.html',
            expectedData=[
                u'220',
                u'561',
                u'405',
                u'544',
                u'221',
                u'426',
                u'450',
                u'564',
                u'309',
                u'266',
                u'547',
                u'282',
                u'299',
                u'225',
                u'269',
                u'393',
                u'548',
                u'205',
                u'429',
                u'302',
                u'572',
                u'293',
                u'228',
                u'472',
                u'395',
                u'573',
                u'515',
                u'289',
                u'231',
                u'457',
                u'232',
                u'569',
                u'347',
                u'213',
                u'214',
                u'576',
                u'234',
                u'513',
                u'430',
                u'206',
                u'545',
                u'303',
                u'451',
                u'348',
                u'324',
                u'425',
                u'489',
                u'578',
                u'456',
                u'236',
                u'452',
                u'270',
                u'238',
                u'571',
                u'376',
                u'239',
                u'312',
                u'567',
                u'240',
                u'378',
                u'300',
                u'241',
                u'399',
                u'516',
                u'242',
                u'243',
                u'424',
                u'541',
                u'245',
                u'323',
                u'246',
                u'247',
                u'446',
                u'420',
                u'325',
                u'291',
                u'568',
                u'458',
                u'540',
                u'250',
                u'557',
                u'283',
                u'209',
                u'556',
                u'570',
                u'252',
                u'539',
                u'428',
                u'286',
                u'401',
                u'566',
                u'349',
                u'253',
                u'384',
                u'379',
                u'254',
                u'579',
                u'552',
                u'437',
                u'255',
                u'388',
                u'256',
                u'377',
                u'162',
                u'558',
                u'202',
                u'352',
                u'257',
                u'543',
                u'397',
                u'292',
                u'259',
                u'298',
                u'553',
                u'400',
                u'350',
                u'261',
                u'262',
                u'306',
                u'263',
                u'212',
                u'264',
                u'432',
                u'265',
                u'326',
                u'272',
                u'460',
                u'449',
                u'332',
                u'560',
                u'546',
                u'559',
                u'555',
                u'565',
                u'520',
                u'577',
                u'549',
                u'554',
                u'551',
                u'575',
                u'563',
                u'310'
            ]
        )
