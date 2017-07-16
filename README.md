# ** NOTE **
This is NOT original [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng) repository. This is my fork with modifications.

That said you're welcome to use it. Enjoy!

# Recon-ng

Recon-ng is a full-featured Web Reconnaissance framework written in Python. Complete with independent modules, database interaction, built in convenience functions, interactive help, and command completion, Recon-ng provides a powerful environment in which open source web-based reconnaissance can be conducted quickly and thoroughly.

Recon-ng has a look and feel similar to the Metasploit Framework, reducing the learning curve for leveraging the framework. However, it is quite different. Recon-ng is not intended to compete with existing frameworks, as it is designed exclusively for web-based open source reconnaissance. If you want to exploit, use the Metasploit Framework. If you want to social engineer, use the Social-Engineer Toolkit. If you want to conduct reconnaissance, use Recon-ng! See the [Usage Guide](https://bitbucket.org/LaNMaSteR53/recon-ng/wiki/Usage%20Guide) for more information.

Recon-ng is a completely modular framework and makes it easy for even the newest of Python developers to contribute. Each module is a subclass of the "module" class. The "module" class is a customized "cmd" interpreter equipped with built-in functionality that provides simple interfaces to common tasks such as standardizing output, interacting with the database, making web requests, and managing API keys. Therefore, all the hard work has been done. Building modules is simple and takes little more than a few minutes. See the [Development Guide](https://bitbucket.org/LaNMaSteR53/recon-ng/wiki/Development%20Guide) for more information.

## Install
It's best to setup a python virtual environment. recon-ng requires python 2.x at this time so do something similar to the following:

```
virtualenv -p python2 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Sponsors

[![Black Hills Information Security](https://static.wixstatic.com/media/75fce7_d7704144d33847a197598d7731d48770.png)](http://www.blackhillsinfosec.com)

Consulting | Research | Development | Training

## Donations

Recon-ng is free software. However, large amounts of time and effort go into its continued development. If you are interested in financialy supporting the development of Recon-ng, please send your donation to tjt1980[at]gmail.com via PayPal. Thank you.
