#!/usr/bin/env python
#
# gravatar - Copyright (c) 2009 Pablo Seminario
# This software is distributed under the terms of the GNU General
# Public License
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''A library that provides a Python interface to the Gravatar XML-RPC API'''

__author__ = 'pabluk@gmail.com'
__version__ = '0.1'

import os
import xmlrpclib
from hashlib import md5
from base64 import b64encode
from urllib import quote

API_URI = 'https://secure.gravatar.com/xmlrpc?user={0}'

class gravatar:
    '''This class encapsulates all methods from the API
    Usage:
    If you have an account at Wordpress.com you can use your API Key
        g = gravatar('user@domain', apikey='1234')
        g.test() # test the API

    Or you can use your Gravatar.com password
        g = gravatar('user@domain', password='1234')
        g.test() # test the API

    API Details: http://en.gravatar.com/site/implement/xmlrpc
    '''

    def __init__(self, email, apikey='', password=''):
        self.apikey = apikey
        self.password = password
        self.email = str.lower(str.strip(email))
        self._server = xmlrpclib.ServerProxy(API_URI.format(md5(self.email).hexdigest()))

    def test(self):
        '''Test the API.'''
        return self._call('test')

    def userimages(self):
        '''Return an array of userimages with your rating and url for this account.'''
        return self._call('userimages')

    def addresses(self):
        '''Get a list of addresses for this account'''
        return self._call('addresses')

    def exists(self, hashes):
        '''Check whether a hash has a gravatar.
        The method receives an array de hashes
            gravatar.exists(['aaaaa', 'bbbbb'])
        '''
        params = {'hashes':hashes}
        return self._call('exists', params)

    def saveData(self, file, rating=0):
        '''Save binary image data as a userimage for this account.'''
        data = ''
        if os.path.isfile(file):
            f = open(file)
            data = b64encode(f.read())

        params = {'rating':rating, 'data':data}

        return self._call('saveData', params)

    def saveUrl(self, url, rating=0):
        '''Read an image via its URL and save that as a userimage for this account.'''

        params = {'rating':rating, 'url':quote(url)}

        return self._call('saveUrl', params)

    def useUserimage(self, userimage, addresses):
        '''Use a userimage as a gravatar for one of more addresses on this account.'''

        params = {'userimage':userimage, 'addresses':addresses}

        return self._call('useUserimage', params)

    def removeImage(self, addresses):
        '''Remove the userimage associated with one or more email addresses.'''

        params = {'addresses':addresses}

        return self._call('removeImage', params)

    def deleteUserimage(self, userimage):
        '''Remove a userimage from the account and any email addresses with which it is associated.'''

        params = {'userimage':userimage}

        return self._call('deleteUserimage', params)

    def _call(self, method, params={}):
        '''Call a method from the API, gets 'grav.' prepended to it.'''

        args = params
        args['apikey'] = self.apikey
        args['password'] = self.password

        return getattr(self._server, 'grav.' + method, None)(args)

