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

import datetime

class DateParserError(Exception):
    pass

class ParseDateError(DateParserError):
    pass

class ParseWeekDaysError(DateParserError):
    pass

DEFAULT_PARSE_DATE_ERROR_STR = 'unknown or invalid date format'
DEFAULT_PARSE_WEEK_DAYS_ERROR_STR = 'unknown or invalid week days format'

def parse_date(s):
    if not isinstance(s, str):
        s = str(s)
    
    if '-' in s:
        ss = s.split('-')
        if len(ss) != 3:
            raise ParseDateError('{}: {!r}'.format(DEFAULT_PARSE_DATE_ERROR_STR, s))
        try:
            year, month, day = map(int, ss)
        except ValueError:
            raise ParseDateError('{}: {!r}'.format(DEFAULT_PARSE_DATE_ERROR_STR, s))
        
        return datetime.date(year, month, day)
    
    if '.' in s:
        ss = s.split('.')
        if len(ss) != 3:
            raise ParseDateError('{}: {!r}'.format(DEFAULT_PARSE_DATE_ERROR_STR, s))
        try:
            day, month, year = map(int, ss)
        except ValueError:
            raise ParseDateError('{}: {!r}'.format(DEFAULT_PARSE_DATE_ERROR_STR, s))
        
        return datetime.date(year, month, day)
    
    raise ParseDateError('{}: {!r}'.format(DEFAULT_PARSE_DATE_ERROR_STR, s))

def parse_week_days(s):
    if not isinstance(s, str):
        s = str(s)
    
    ss = s.split(',')
    
    week_days = []
    
    for raw_day in filter(None, map(lambda s: s.strip(), ss)):
        if raw_day.lower() == 'mo':
            day = 0
        elif raw_day.lower() == 'tu':
            day = 1
        elif raw_day.lower() == 'we':
            day = 2
        elif raw_day.lower() == 'th':
            day = 3
        elif raw_day.lower() == 'fr':
            day = 4
        elif raw_day.lower() == 'sa':
            day = 5
        elif raw_day.lower() == 'su':
            day = 6
        else:
            try:
                day = int(raw_day)
            except ValueError:
                raise ParseWeekDaysError('{}: {!r}'.format(DEFAULT_PARSE_WEEK_DAYS_ERROR_STR, s))
            if day not in range(7):
                raise ParseWeekDaysError('{}: {!r}'.format(DEFAULT_PARSE_WEEK_DAYS_ERROR_STR, s))
        
        week_days.append(day)
    return tuple(week_days)
