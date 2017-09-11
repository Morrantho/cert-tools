#!/usr/bin/env python
'''
Generates the issuer file (.json) that represents the issues which is needed for issuing and validating certificates.

Currently, just not check for inputs' validity (e.g. valid address, URLs, etc.)
'''
import os
import sys
import json
import datetime

import configargparse

from cert_tools import helpers

def generate_issuer_file(config):
    output_handle = open(config.output_file, 'w') if config.output_file else sys.stdout
    introductionURL = config.issuer_url + "intro/" if config.issuer_url.endswith('/') else "/intro/"
    currentDate = str(datetime.date.today())

    issuer_json = {
       'id': config.issuer_id,
       'url': config.issuer_url,
       'introductionURL': introductionURL,
       'name': config.issuer_name,
       'email': config.issuer_email,
       'image': helpers.encode_image(config.issuer_logo_file),
       'issuerKeys': [
           {
               'date': currentDate,
               'key': config.issuer_address
           }
       ],
       'revocationKeys': [
           {
               'date': currentDate,
               'key': config.revocation_address
           }
       ]
     }

    output_handle.write(json.dumps(issuer_json, indent=2))

    if output_handle is not sys.stdout:
        output_handle.close()


def get_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(base_dir, 'conf.ini')]) 
    p.add('-c', '--my-config', required=True, is_config_file=True, help='config file path')
    p.add_argument('-k', '--issuer_address', type=str, required=True, help='the issuer\'s Bitcoin address that will be used to issue the certificates')
    p.add_argument('-r', '--revocation_address', type=str, required=True, help='the issuer\'s Bitcoin revocation address that can be used to revocate the certificates')
    p.add_argument('-d', '--issuer_id', type=str, required=True, help='the issuer\'s publicly accessible identification file; i.e. URL of the file generated by this tool')

    p.add_argument('-u', '--issuer_url', type=str, help='the issuers main URL address')
    p.add_argument('-l', '--issuer_certs_url', type=str, help='the issuer\'s URL address of the certificates')
    p.add_argument('-n', '--issuer_name', type=str, help='the issuer\'s name')
    p.add_argument('-e', '--issuer_email', type=str, help='the issuer\'s email')
    p.add_argument('-m', '--issuer_logo_file', type=str, help='the issuer\' logo image')
    p.add_argument('-o', '--output_file', type=str, help='the output file to save the issuer\'s identification file')
    args, _ = p.parse_known_args()

    return args


def main():
    conf = get_config()
    generate_issuer_file(conf)


if __name__ == "__main__":
    main()

