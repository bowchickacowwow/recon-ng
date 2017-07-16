import json
import time
from recon.core.module import BaseModule


class Module(BaseModule):

    meta = {
        'name': 'ipinfo.io GeoIP',
        'author': 'Xavier Stevens (@xstevens)',
        'description': 'Leverages the ipinfo.io API to geolocate a host by IP address. Updates the \'hosts\' table with the results.',
        'required_keys': ['ipinfoio_api'],
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
    }
   
    def module_run(self, hosts):
        api_key = self.keys.get('ipinfoio_api')
        for host in hosts:
            url = 'https://ipinfo.io/%s/json?token=%s' % (host, api_key)
            resp = self.request(url)
            if resp.json:
                jsonobj = resp.json
            else:
                self.error('Invalid JSON response for \'%s\'.\n%s' % (host, resp.text))
                continue
            if resp.status_code == 429:
                self.error("Exceeded request allowance. ipinfo.io is telling you to back off.")
                break
            time.sleep(.7)
            region = ', '.join([str(jsonobj[x]).title() for x in ['city', 'region'] if jsonobj[x]]) or None
            country = jsonobj['country']
            loc = jsonobj['loc']
            latitude, longitude = loc.split(',')
            org = jsonobj['org']
            asn, org_name = org.split(" ", 1)
            self.output('%s - %s %s - %s,%s - %s' % (host, asn, org_name, latitude, longitude, ', '.join([x for x in [region, country] if x])))
            self.query('UPDATE hosts SET asn=?, org=?, region=?, country=?, latitude=?, longitude=? WHERE ip_address=?', (asn, org_name, region, country, latitude, longitude, host))
