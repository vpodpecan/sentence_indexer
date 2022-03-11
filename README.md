### Sentence indexer and sampler

This small project implements an indexer on a given corpus of sentences. It uses the most basic schema (the only field is the sentence itself), but also offers lemmatization when indexing and searching.

### Requirements
-  python 3.6+
-  whoosh==2.7.*
-  lemmagen3==3.3.2


### How to use

The following snippet illustrates how to use indexer. We will  use NLTK's sentence tokenizer to split the text of the whole novel [Deseti brat](https://sl.wikisource.org/wiki/Deseti_brat_(Josip_Jur%C4%8Di%C4%8D)) into sentences and store them into an index. Then, we will perform an ordinary query which returns the first _k_ results, and a sample query which samples the whole results set.

Notice that the results contain sentences which contain different forms of the query word. This is the result of using the `indexer.lemmatization_schema`. If you do not want such behaviour you can use the `indexer.simple_schema` which only performs tokenization and lowercase transformation.


```python
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
```
