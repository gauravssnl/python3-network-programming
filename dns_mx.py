#!/usr/bin/env python3
# Looking up a mail domain - the part of an email address after the `@`

import dns.resolver


def resolve_hostname(hostname, indent=''):
    """ print an A or AAAA record for hostname; follow CNAME if necessary """
    indent = indent + '	'
    answer = dns.resolver.query(hostname, 'A')
    if answer.rrset is not None:
        for record in answer:
            print(indent, hostname, 'has A address', record.address)
            return
    answer = dns.resolver.query(hostname, 'AAAA')
    if answer.rrset is not None:
        for record in answer:
            print(indent, hostname, 'has AAAA address', record.address)
            return
    answer = dns.resolver.query(hostname, 'CNAME')
    if answer.rrset is not None:
        record = answer[0]
        cname = record.address
        print(indent, hostname, 'is an alias for', cname)
        resolve_hostname(cname, indent)
        return
    print(indent, 'ERROR: no A, AAAA, or CNAME records for', hostname)


def resolve_email_domain(domain):
    """ For an email address `name@domain` , find its mail server IP address """
    try:
        answer = dns.resolver.query(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        print('Error: No such domain', domain)
        return
    if answer.rrset is not None:
        records = sorted(answer, key=lambda record: record.preference)
        for record in records:
            name = record.exchange.to_text(omit_final_dot=True)
            print('Priority', record.preference)
            resolve_hostname(name)
    else:
        print(domain, 'has no explicit MX records')
        print('Attempting to resolve domain as an a A, AAAA, or CNAME')
        resolve_hostname(domain)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Find mailserver IP address')
    parser.add_argument('domain', help='domain that you want to send mail to')
    resolve_email_domain(parser.parse_args().domain)
