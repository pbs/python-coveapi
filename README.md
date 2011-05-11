# Overview

Python-coveapi is the Python client for the PBS COVE API service.


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
    cove = coveapi.connect('PHONY-COVEAPI-APP-ID', 'PHONY-COVEAPI-APP-SECRET')

To retrieve a single resource, pass the resource ID, or resource URI to <code>*.get()</code>

    cove.videos.get(3143)
    cove.videos.get('/cove/v1/videos/3143/')
    cove.videos.get('http://api.pbs.org/cove/v1/videos/3143/')
    

To retrieve a list resources, pass the filters to <code>*.filter()</code>

    cove.programs.filter(filter_nola_root='NOVA')
    cove.programs.filter(filter_title='American Experience')

You may query with <code>*.get()</code> or <code>*.filter()</code> for:

    * Groups: <code>cove.groups.get(<resource>)</code>
    * Categories: <code>cove.categories.get(<resource>)</code>
    * Programs: <code>cove.programs.get(<resource>)</code>
    * Videos: <code>cove.videos.get(<resource>)</code>
    

See COVE API documentation for the complete list of filters and return data.