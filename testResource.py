from flask_restful import reqparse

import urllib2
from SharedModels import api
from base_resource import BaseResource


class testResource(BaseResource):
    parser = api.parser()
    parser.add_argument('myURL', type=str, location='headers', required=True)
    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('myURL', type=str, location='headers', required=True)
        args = parser.parse_args()

        req = urllib2.Request(args['myURL'])
        print args['myURL']
        response = urllib2.urlopen(req)
        the_page = response.read()

        the_page = the_page.decode('string_escape').decode('string_escape')
        the_page = the_page.replace('""', '')

        return the_page