# Overview

<code>coveapi</code> is the Python client for the PBS COVE API service.


# Getting Started

* Read the [COVE API documentation](http://projects.pbs.org/confluence/x/1IlGAQ).
* [Request an API Key](http://open.pbs.org/pbs-api-key-request/) from PBS
* Install Python dependencies: <code>pip install -r REQUIREMENTS.txt</code>


# Installation

Install <code>coveapi</code> to your Python path (hopefully in a virtual environment!).

    python setup.py install
    
    
# Usage

To do anything, you will first need a connection to the COVE API service:

    import coveapi
    cove = coveapi.connect('PHONY-COVEAPI_APP_ID', 'PHONY-COVEAPI_APP_SECRET')

To retrieve a single resource, pass the resource ID, or resource URI to *.get():

    cove.videos.get(123)
    cove.videos.get('/cove/v1/videos/123/')
    cove.videos.get('http://api.pbs.org/cove/v1/videos/123/')
    

To retrieve a list resources, pass the filters to *.filter():

    cove.programs.filter(filter_nola_root='NOVA')
    cove.programs.filter(filter_title='American Experience')


See COVE API documentation for the complete list of filters and return data.