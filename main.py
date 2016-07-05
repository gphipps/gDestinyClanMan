#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.api import urlfetch
import webapp2
import json
import jinja2
import os
import cgi

BungieApiKey = 'e942319af99a40c99a830df9973d3a7f'

jinja_environment = jinja2.Environment(
    autoescape=True,
    loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #name = self.request.params.get('name')
        #if name:
        #    self.response.out.write('Hello %s' % name)
        #else:
        #    self.response.out.write('Hello world!')
        
        pageCount = 1
        platformType = 1
        HEADERS = {"X-API-Key": BungieApiKey}
        url = "http://www.bungie.net/Platform/Group/119204/Members/?lc=en&fmt=true&currentPage=" + str(pageCount) + "&platformType=" + str(platformType)
        result = urlfetch.fetch(url, headers=HEADERS)
        py_result = json.loads(result.content)
        xboxMemberCount = py_result['Response']['totalResults']
        xboxclanmembers = py_result['Response']['results']
        
        pageCount += 1
        while py_result['Response']['hasMore'] is True:
            url = "http://www.bungie.net/Platform/Group/119204/Members/?lc=en&fmt=true&currentPage=" + str(pageCount) + "&platformType=" + str(platformType)
            result = urlfetch.fetch(url, headers=HEADERS)
            py_result = json.loads(result.content)
            xboxclanmembers.extend(py_result['Response']['results'])
            pageCount += 1
        
        pageCount = 1
        platformType = 2

        url = "http://www.bungie.net/Platform/Group/119204/Members/?lc=en&fmt=true&currentPage=" + str(pageCount) + "&platformType=" + str(platformType)
        result = urlfetch.fetch(url, headers=HEADERS)
        py_result = json.loads(result.content)
        psnMemberCount = py_result['Response']['totalResults']
        psnclanmembers = py_result['Response']['results']
        
        pageCount += 1

        while py_result['Response']['hasMore'] is True:
            url = "http://www.bungie.net/Platform/Group/119204/Members/?lc=en&fmt=true&currentPage=" + str(pageCount) + "&platformType=" + str(platformType)
            result = urlfetch.fetch(url, headers=HEADERS)
            py_result = json.loads(result.content)
            psnclanmembers.extend(py_result['Response']['results'])
            pageCount += 1

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(xboxclanmembers=xboxclanmembers, xboxMemberCount=xboxMemberCount, psnclanmembers=psnclanmembers, psnMemberCount=psnMemberCount))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
