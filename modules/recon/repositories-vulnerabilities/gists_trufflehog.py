import math
import os
from recon.core.module import BaseModule

class Module(BaseModule):
    """
    This merges the important bits of the truffleHog code into gist searching within recon-ng.

    TODO: In future refactor truffle hog entropy code into a re-usable component.
    """
    meta = {
        'name': 'Github Gist Truffle Hog',
        'author': '@dxa4481 and Xavier Stevens (@xstevens)',
        'description': 'Uses the Github API to download and search Gists for high entropy strings. Updates the \'vulnerabilities\' table with the results.',
        'query': "SELECT DISTINCT url FROM repositories WHERE url IS NOT NULL AND resource LIKE 'Github' AND category LIKE 'gist'",
        'options': (
            ('b64entropy', 4.5, False, 'the Base64 entropy threshold'),
            ('hexentropy', 3, False, 'the Base64 entropy threshold'),
        ),
    }

    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    HEX_CHARS = "1234567890abcdefABCDEF"

    def shannon_entropy(self, data, iterator):
        """
        Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
        """
        if not data:
            return 0
        entropy = 0
        for x in iterator:
            p_x = float(data.count(x))/len(data)
            if p_x > 0:
                entropy += - p_x*math.log(p_x, 2)
        return entropy

    def get_strings_of_set(self, word, char_set, threshold=20):
        count = 0
        letters = ""
        strings = []
        for char in word:
            if char in char_set:
                letters += char
                count += 1
            else:
                if count > threshold:
                    strings.append(letters)
                letters = ""
                count = 0
        if count > threshold:
            strings.append(letters)
        return strings

    def module_run(self, gists):
        b64_entropy_threshold = float(self.options['b64entropy'])
        hex_entropy_threshold = float(self.options['hexentropy'])
        for gist in gists:
            filename = gist.split(os.sep)[-1]
            resp = self.request(gist)
            lines = resp.raw.splitlines()
            examples = []
            for lineno, line in enumerate(lines):
                for word in line.split():
                    base64_strings = self.get_strings_of_set(word, self.BASE64_CHARS)
                    hex_strings = self.get_strings_of_set(word, self.HEX_CHARS)
                    for string in base64_strings:
                        b64_entropy = self.shannon_entropy(string, self.BASE64_CHARS)
                        if b64_entropy > b64_entropy_threshold:
                            examples.append('line %d: %s' % (lineno, line.strip()))

                    for string in hex_strings:
                        hex_entropy = self.shannon_entropy(string, self.HEX_CHARS)
                        if hex_entropy > hex_entropy_threshold:
                            examples.append('line %d: %s' % (lineno, line.strip()))

            if len(examples) > 0:
                self.heading(filename, level=0)
                data = {
                    'reference': gist,
                    'example': '\n'.join(examples),
                    'category': 'Information Disclosure',
                }
                self.add_vulnerabilities(**data)
