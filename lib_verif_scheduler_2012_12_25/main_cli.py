# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2012 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import sys
import argparse
from . import date_parser
from . import excl_file
from . import verif_scheduler

class UserError(Exception):
    pass

def main():
    try:
        parser = argparse.ArgumentParser(
                description='utility for scheduling device verification process')
        parser.add_argument('--begin-date', metavar='BEGIN-DATE',
                help='date of period begin')
        parser.add_argument('--end-date', metavar='END-DATE',
                help='date of period end (not including end day)')
        parser.add_argument('--verif-count', metavar='VERIF-COUNT', type=int,
                help='count of device verifications')
        parser.add_argument('--week-days', metavar='WEEK-DAYS-LIST',
                help='list of week days. example: "0,2,4" means is "mo, we, fr"')
        parser.add_argument('--excl', metavar='EXCLUSION-FILE-PATH',
                help='path to exclusion file')
        parser.add_argument('--use-rus-fmt', action='store_true',
                help='use russian regional format for result output file')
        parser.add_argument('--out', metavar='OUT-FILE-PATH',
                help='path to result output file')
        
        args = parser.parse_args()
        
        if args.begin_date is None:
            raise UserError('args.begin_date is None')
        if args.end_date is None:
            raise UserError('args.end_date is None')
        if args.verif_count is None or args.verif_count <= 0:
            raise UserError('args.verif_count is None or args.verif_count <= 0')
        if args.week_days is None:
            raise UserError('args.week_days is None')
        if args.out is None:
            raise UserError('args.out is None')
        
        begin_date = date_parser.parse_date(args.begin_date)
        end_date = date_parser.parse_date(args.end_date)
        week_days = date_parser.parse_week_days(args.week_days)
        if args.excl is not None:
            excl_list = tuple(excl_file.load_excl_file(args.excl))
        else:
            excl_list = None
        
        sch_dates = verif_scheduler.verif_schedule(
                verif_scheduler.get_dates(
                        begin_date,
                        end_date,
                        week_days,
                        excl_list=excl_list,
                        ),
                args.verif_count,
                )
        
        with open(args.out, 'w', encoding='utf-8', newline='\n', errors='replace') as fd:
            for sch_date in sch_dates:
                if args.use_rus_fmt:
                    fd.write('{}\n'.format(sch_date.strftime('%d.%m.%Y')))
                    continue
                fd.write('{}\n'.format(sch_date))
    except UserError as e:
        print('user error: {}'.format(e), file=sys.stderr)
