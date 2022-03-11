import indexer
from nltk.tokenize import sent_tokenize

# split text into sentences
text = open('sample_data/Deseti_brat.txt').read().replace('\n', ' ')
sentences = sent_tokenize(text, language='slovene')

# create index using simple schema with lemmatization and add sentences to index
lem_idx = indexer.create_index('index_folder', 'deseti_brat_idx', schema=indexer.lemmatization_schema)
indexer.add_sentences_to_index(sentences, lem_idx)

# an ordinary query with first 10 results
indexer.query('puška', lem_idx, limit=10)

# a query which returns a random sample of the whole result set
indexer.query_sample('puška', lem_idx, sample_size=10)
