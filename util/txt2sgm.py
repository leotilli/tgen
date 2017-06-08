#!/usr/bin/env python
# -"- coding: utf-8 -"-

from __future__ import unicode_literals

import codecs
import argparse

from tgen.debug import exc_info_hook
import sys
# Start IPdb on error in interactive mode
sys.excepthook = exc_info_hook


def convert(args):
    insts = []
    max_refs = 1

    with codecs.open(args.in_file, 'rb', 'UTF-8') as fh:
        cur_no = 0
        for line in fh:
            line = line.strip()
            if args.multi_ref:
                if cur_no > max_refs:
                    max_refs = cur_no
                if not line:
                    cur_no = 0
                else:
                    if cur_no == 0:
                        insts.append([])
                    insts[-1].append(line)
                    cur_no += 1
            else:
                insts.append([line])

    with codecs.open(args.out_file, 'wb', 'UTF-8') as fh:
        settype = 'tstset' if args.type == 'test' else args.type + 'set'
        fh.write('<%s setid="%s" srclang="any" trglang="%s">\n' % (settype, args.name, args.lang))
        for inst_set_no in xrange(max_refs):
            sysid = args.sysid + ('' if max_refs == 1 else '_%d' % inst_set_no)
            fh.write('<doc docid="test" genre="news" origlang="any" sysid="%s">\n<p>\n' % sysid)
            for inst_no, refs in enumerate(insts, start=1):
                ref = refs[inst_set_no % len(refs)]  # cycle refs to have max. number
                fh.write('<seg id="%d">%s</seg>\n' % (inst_no, ref))
            fh.write('</p>\n</doc>\n')
        fh.write('</%s>' % settype)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--type', choices=['ref', 'src', 'test'], required=True,
                    help='Set type <ref|src|test>')
    ap.add_argument('-n', '--name', default='noname', help='Set name')
    ap.add_argument('-l', '--lang', default='en', help='Set language')
    ap.add_argument('-s', '--sysid', help='System ID', default='')
    ap.add_argument('-m', '--multi-ref',
                    help='Multiple reference mode: group by empty lines', action='store_true')

    ap.add_argument('in_file', help='Input TXT file')
    ap.add_argument('out_file', help='Output SGM file')

    args = ap.parse_args()
    convert(args)
