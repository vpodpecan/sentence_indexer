import os
from whoosh import index
from whoosh.fields import Schema, TEXT
from whoosh.analysis import Filter, SimpleAnalyzer
from whoosh.qparser import QueryParser
from random import sample

from lemmagen3 import Lemmatizer

lem_sl = Lemmatizer('sl')


class LemmatizationFilter(Filter):
    is_morph = True

    def __init__(self, lang):
        self.lang = lang

    def __call__(self, tokens):
        for t in tokens:
            t.text = lem_sl.lemmatize(t.text)
            yield t


simple_schema = Schema(content=TEXT(stored=True, analyzer=SimpleAnalyzer()))
lemmatization_schema = Schema(content=TEXT(stored=True, analyzer=SimpleAnalyzer() | LemmatizationFilter(lang='sl')))


def read_or_create_index(idirname, iname, schema):
    if not os.path.exists(idirname):
        os.mkdir(idirname)
        ix = index.create_in(idirname, schema=schema, indexname=iname)
    try:
        ix = index.open_dir(idirname, indexname=iname)
    except:
        ix = index.create_in(idirname, schema=schema, indexname=iname)
    return ix


def create_index(idirname, iname, schema=lemmatization_schema):
    if not os.path.exists(idirname):
        os.mkdir(idirname)
    ix = index.create_in(idirname, schema=schema, indexname=iname)
    return ix


def add_sentences_to_index(sentences, index):
    with index.writer() as writer:
        for sentence in sentences:
            writer.add_document(content=sentence)


def query(query, index, limit=10):
    qp = QueryParser('content', schema=index.schema)
    q = qp.parse(query)
    with index.searcher() as s:
        results = s.search(q, limit=limit)
        sentences = [x['content'] for x in results]
    return sentences


def query_sample(query, index, sample_size=10):
    qp = QueryParser('content', schema=index.schema)
    q = qp.parse(query)
    with index.searcher() as s:
        results = s.search(q, limit=None)
        sentences = [x['content'] for x in results]
    if sample_size <= len(sentences):
        return sample(sentences, sample_size)
    else:
        return sentences
