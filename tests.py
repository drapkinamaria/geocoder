import unittest
from calculations import *


texts = [
    '''<node id="2736761063" version="1" timestamp="2014-03-23T14:48:14Z" ''' +
    '''lat="45.4074454" lon="35.8552273"/>\n<node id="2736761065" version=''' +
    '''"1" timestamp="2014-03-23T14:48:14Z" lat="45.4074638" lon="35.85490''' +
    '''56"/>\n<node id="2736761066" version="1" timestamp="2014-03-23T14:4''' +
    '''8:14Z" lat="45.4075846" lon="35.8545614"/>\n<node id="2736761068" v''' +
    '''ersion="1" timestamp="2014-03-23T14:48:14Z" lat="45.4075978" lon="3''' +
    '''5.8554443"/>\n<node id="2736761070" version="1" timestamp="2014-03-''' +
    '''23T14:48:14Z" lat="45.4077343" lon="35.8543145"/>''',
    '''
    <way id="4424726" version="9" timestamp="2021-05-08T08:07:46Z">
    <nd ref="27137906"/>
    <nd ref="27137907"/>
    <tag k="highway" v="secondary"/>
    <tag k="old_ref" v="Т-01-02"/>
    <tag k="surface" v="asphalt"/>
    </way>
    ''',
    ""
]

bad_words = build_bad_words(read_file("bad_words.txt").split())


class TestCalculations(unittest.TestCase):

    def test_getting_nodes(self):
        self.assertEqual(
            {
                '2736761063': {'lat': '45.4074454', 'lon': '35.8552273'},
                '2736761065': {'lat': '45.4074638', 'lon': '35.8549056'},
                '2736761066': {'lat': '45.4075846', 'lon': '35.8545614'},
                '2736761068': {'lat': '45.4075978', 'lon': '35.8554443'},
                '2736761070': {'lat': '45.4077343', 'lon': '35.8543145'}
            },
            get_nodes(texts[0]))
        self.assertEqual({}, get_nodes(texts[2]))

    def test_getting_ways(self):
        self.assertEqual(
            {
                '4424726':
                    {
                        'nodes': ['27137906', '27137907'],
                        'tags': ['secondary', 'т-01-02', 'asphalt']
                    }
            },
            get_ways(texts[1], bad_words))
        self.assertEqual({}, get_ways(texts[2], bad_words))

    def test_geopy(self):
        self.assertEqual({'1': {'lat': 56.6811951, 'lon': 48.07362542533522}},
                         find_with_api("Москва Кузнецово 3а"))
        self.assertEqual({'1': {'lat': 56.840488, 'lon': 60.61649048816038}},
                         find_with_api("Ленина 51 Екатеринбург"))
        self.assertEqual({'1': {'lat': 56.7728553, 'lon': 60.5455228}},
                         find_with_api(" Екатеринбург Лесная"))
