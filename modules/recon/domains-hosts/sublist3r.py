from recon.core.module import BaseModule
from recon.mixins.resolver import ResolverMixin
import dns.resolver
import os
from recon import sublist3r

class Module(BaseModule, ResolverMixin):

    meta = {
        'name': 'DNS enumeration using Sublist3r',
        'author': 'Xavier Stevens (@xstevens)',
        'description': 'DNS enumeration using Sublist3r. Updates the \'domains\' table with the results.',
        'comments': (
            'Github: https://github.com/aboul3la/Sublist3r',
        ),
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'options': (
            ('engines', None, False, 'comma-separated list of search engines to use'),
            ('threads', 1, False, 'number of threads to use')
        ),
    }

    def module_run(self, domains):
        num_threads = int(self.options['threads'])
        for domain in domains:
            self.heading(domain, level=0)
            subdomains = sublist3r.main(domain, num_threads, None, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=self.options['engines'])
            for subdomain in subdomains:
                self.add_hosts(subdomain)
        