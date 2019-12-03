# -*- coding: utf-8 -*-
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.analysis import StandardAnalyzer

from musicpod.model.artist import Artist
from musicpod.model.release import Release


class Search(object):

    DEFAULT_LIMIT = 100

    no_stop = StandardAnalyzer(stoplist=None)
    schema = Schema(dtype=NUMERIC(stored=True),
                    id=NUMERIC(stored=True),
                    name=TEXT(stored=True, analyzer=no_stop), 
                    artist=TEXT(stored=True, analyzer=no_stop), 
                    release=TEXT(stored=True, analyzer=no_stop), 
                    sortname=TEXT(stored=True),
                    artistid=ID(stored=True),
                    releaseid=ID(stored=True),
                    year=NUMERIC
                   )
    try:
        ix = open_dir("data/search")
    except EmptyIndexError:
        try:
            ix = create_in("data/search", schema)
        except ValueError:
            ix = None

    def search(self, field, query, limit = DEFAULT_LIMIT):
        def compare(a, b):
            if a['dtype'] == b['dtype']:
                return int(b['score'] - a['score'])
            else:
                return a['dtype'] - b['dtype']; 

        searcher = self.ix.searcher()
        query = QueryParser(field, schema=self.schema).parse(query)
        result = searcher.search(query, limit=limit)
        json = []
        for i in xrange(result.scored_length()):
            d = {}
            for f in result.fields(i):
                d[f] = result[i][f]
            d['score'] = int(result.score(i) * 20)
            json.append(d)
        json = sorted(json, cmp=compare)

        return json

    def index_data(self):
        writer = self.ix.writer()
        artists = Artist.query.order_by(Artist.sortname).all()
        for a in artists:
            writer.add_document(dtype=0,
                                name=a.name,
                                artist=a.name,
                                sortname=a.sortname,
                                artistid=a.mbid,
                                id=a.id)
        writer.commit()

        writer = self.ix.writer()
        releases = Release.query.order_by(Release.name).all()
        for r in releases:
            writer.add_document(dtype=1,
                                name=r.name,
                                artist=r.name,
                                year=r.year,
                                releaseid=r.mbid,
                                id=r.id)
        writer.commit(optimize=True)

search_inst = Search()
