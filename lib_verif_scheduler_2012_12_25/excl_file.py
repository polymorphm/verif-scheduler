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

from . import date_parser
from . import verif_scheduler

def load_excl_file(path):
    with open(path, 'r', encoding='utf-8', newline='\n', errors='replace') as fd:
        for line in filter(None, map(lambda s: s.strip(), fd)):
            if ':' not in line:
                yield date_parser.parse_date(line)
                continue
            
            begin_date, end_date = \
                    map(date_parser.parse_date,
                            map(lambda s: s.strip(),
                                    line.split(':', 1)))
            
            for date in verif_scheduler.make_date_iter(begin_date, end_date):
                # TODO: in Python-3.3+ we may use ``yield from``
                yield date
