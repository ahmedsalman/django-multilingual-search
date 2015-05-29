# django-multilingual-search
A multilingual Haystack plugin for Django and Elasticsearch.
The module is a drop-in replacement for the Haystack `ElasticsearchSearchEngine`.

Instead of a single index it creates an index for each language specified in `settings.LANGUAGES`.

A query is routed to the index of the currently active language.


## Installation

Install with pip:

    pip install django-multilingual-search
    
The major and minor versions of this project correspond to the Haystack version the package was
tested against.
    
    
## Configuration

The app provides a drop-in replacement for the ElasticsearchEngine of Haystack.
To use it, specify this engine in `settings.py`:

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'multilingual.elasticsearch.ElasticsearchMultilingualSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'myproject',
        },
    }

## Contributing

Please read the [Contributing](./CONTRIBUTING.md) guide.


## Release History

- 2.3.0: First release