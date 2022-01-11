import unittest
from calculations import *

strings = [
    ("Вертолет", "Вертолет"),
    ("Машина", "Я"),
    ("Левенштейна", '')
]
texts = [
    '''
    <node id="2736761063" version="1" timestamp="2014-03-23T14:48:14Z" lat="45.4074454" lon="35.8552273"/>
    <node id="2736761065" version="1" timestamp="2014-03-23T14:48:14Z" lat="45.4074638" lon="35.8549056"/>
    <node id="2736761066" version="1" timestamp="2014-03-23T14:48:14Z" lat="45.4075846" lon="35.8545614"/>
    <node id="2736761068" version="1" timestamp="2014-03-23T14:48:14Z" lat="45.4075978" lon="35.8554443"/>
    <node id="2736761070" version="1" timestamp="2014-03-23T14:48:14Z" lat="45.4077343" lon="35.8543145"/>
    ''',
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

    def test_distance(self):
        self.assertEqual(0, distance(strings[0][0], strings[0][1]))
        self.assertEqual(6, distance(strings[1][0], strings[1][1]))
        self.assertEqual(11, distance(strings[2][0], strings[2][1]))

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
