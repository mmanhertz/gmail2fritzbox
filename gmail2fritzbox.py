"""
    This module converts contacts exported from gmail as .csv to an .xml that
    can be imported as phonebook on a FritzBox 6360 Cable.

    Author: Matthias Manhertz
    License: MIT
    Date: 15.03.2017
"""

from __future__ import unicode_literals

import argparse
import re
from time import time

import pandas as pd


XML_TEMPLATE = '''
<?xml version="1.0" encoding="utf-8"?>
<phonebooks>
    <phonebook>
        {contacts}
    </phonebook>
</phonebooks>
'''

CONTACT_TEMPLATE = '''
<contact>
    <category>0</category>
    <person>
        <realName>{name}</realName>
    </person>
    {telephony}
    <services />
    <setup />
    <features doorphone="0" />
    <mod_time>{mod_time}</mod_time>
    <uniqueid>{unique_id}</uniqueid>
</contact>
'''

TELEPHONY_TEMPLATE = '''
<telephony nid="{num_count}">
    {numbers}
</telephony>
'''

NUMBER_TEMPLATE = '''
<number type="{type}" prio="{prio}" id="{id}">{number}</number>
'''


def gmail2fritzbox(in_path, out_path):
    df = pd.read_csv(in_path, sep=',', header=0)

    relevant_headers = ['Name']
    relevant_headers.extend([col for col in list(df) if 'Phone' in col])

    xml_contacts = []
    for contact in df[relevant_headers].itertuples():
        xml_contacts.append(contact2xml(contact))

    xml = XML_TEMPLATE.format(contacts='\n'.join(xml_contacts))

    with open(out_path, 'w') as f:
        f.write(xml.encode('utf-8'))


def contact2xml(entry):
    numbers = []
    id, name = entry[0:2]
    if type(name) == str:
        name = name.decode('utf-8')
        name = name.replace('&', 'u.')
    for i in range(4):
        numbers.append(entry[(i + 1) * 2:(i + 2) * 2])
    return CONTACT_TEMPLATE.format(
        name=name,
        telephony=numbers2xml(numbers),
        unique_id=id + 50,
        mod_time=int(time()),
    )


def numbers2xml(numbers):
    num_count = 0
    xml_numbers = []
    numbers = clean_numbers(numbers)

    for ntype, number in numbers:
        xml_numbers.append(number2xml(number, ntype, num_count))
        num_count += 1

    return TELEPHONY_TEMPLATE.format(
        num_count=num_count,
        numbers='\n'.join(xml_numbers)
    )


def number2xml(number, ntype, id):
    return NUMBER_TEMPLATE.format(
        type=ntype.lower(),
        number=number,
        id=id,
        prio=1 if id == 0 else 0,
    )


def clean_numbers(numbers):
    cleaned_numbers = []
    for ntype, number in numbers:
        if type(ntype) == str:
            # there can be additional chars and text, remove that stuff
            number = re.sub('[^0123456789()+:]', '', number)

            # For some reason gmail sometimes exports two numbers separated by
            # three colons. Separate them and treat them as different numbers.
            split_numbers = number.split(' ::: ')
            for n in split_numbers:
                # remove the country prefix if any
                n = rm_prefix('+49', n)
                cleaned_numbers.append((ntype, n))
    return cleaned_numbers


def rm_prefix(prefix, txt):
    if txt.startswith(prefix):
        return txt[len(prefix):]
    return txt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('inpath', help='Filepath to the input .csv file.')
    parser.add_argument('outpath', help='Filepath to the output .xml file.')

    args = parser.parse_args()

    gmail2fritzbox(args.inpath, args.outpath)


