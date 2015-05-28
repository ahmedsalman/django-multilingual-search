# coding: utf-8
from __future__ import absolute_import, unicode_literals
from django.test import SimpleTestCase
from django.utils import translation

from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend
from haystack.query import SearchQuerySet
from multilingual.elasticsearch_backend import ElasticsearchMultilingualSearchQuery, \
    ElasticsearchMultilingualSearchBackend
from .mocks import Data, mock_backend

try:
    from unittest import mock  # python >= 3.3
except ImportError:
    import mock  # python 2


@mock.patch('elasticsearch.Elasticsearch')
class BackendTest(SimpleTestCase):
    maxDiff = None

    def test_query(self, mock_es):
        sqs = SearchQuerySet()
        self.assertFalse(sqs.query.has_run())
        self.assertIsInstance(sqs.query, ElasticsearchMultilingualSearchQuery)
        all_results = sqs.all()
        all_results.query.backend = mock_backend()
        list(all_results)
        self.assertTrue(all_results.query.backend.search.called)
        self.assertEqual('*:*', all_results.query.backend.search.call_args[0][0])

    def test_haystack_search(self, mock_es):
        es = ElasticsearchSearchBackend('default', **Data.connection_options)
        self.assertFalse(es.setup_complete)
        es.setup()
        es.search('*:*', end_offset=1)
        es.conn.search.assert_called_with(**Data.search_kwargs)

    def test_multilingual_search(self, mock_es):
        es = ElasticsearchMultilingualSearchBackend('default', **Data.connection_options)
        es.setup()
        kwargs = Data.search_kwargs.copy()
        for language in ['de', 'en', 'ru']:
            with translation.override(language):
                es.search('*:*', end_offset=1)
                kwargs['index'] = es.index_name_for_language(language)
                es.conn.search.assert_called_with(**kwargs)

    def test_haystack_process_results(self, mock_es):
        es = ElasticsearchSearchBackend('default', **Data.connection_options)
        es.setup()
        results = es._process_results(Data.raw_results)
        expected = {'hits': 0, 'spelling_suggestion': None, 'results': [], 'facets': {}}
        self.assertEqual(expected, results)

    def test_multiligual_process_results(self, mock_es):
        es = ElasticsearchMultilingualSearchBackend('default', **Data.connection_options)
        es.setup()
        results = es._process_results(Data.raw_results)
        expected = {'hits': 0, 'spelling_suggestion': None, 'results': [], 'facets': {}}
        self.assertEqual(expected, results)