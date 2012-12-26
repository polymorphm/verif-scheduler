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

import calendar
import itertools
from . import shuf

class VerifSchedulerError(Exception):
    pass

class GetDaysError(VerifSchedulerError):
    pass

def make_date_iter(begin_date, end_date):
    cal = calendar.Calendar()
    cal_year = begin_date.year
    cal_month = begin_date.month
    
    while True:
        for date in cal.itermonthdates(cal_year, cal_month):
            if date >= end_date:
                return
            
            if date < begin_date or date.year != cal_year or date.month != cal_month:
                continue
            
            yield date
        
        cal_month += 1
        
        if cal_month == 13:
            cal_year += 1
            cal_month = 1

def get_dates(begin_date, end_date, week_days, excl_list=None):
    if excl_list is None:
        excl_list = ()
    
    if not isinstance(week_days, tuple):
        week_days = tuple(week_days)
    if not isinstance(excl_list, tuple):
        excl_list = tuple(excl_list)
    
    for date in make_date_iter(begin_date, end_date):
        if date.weekday() not in week_days:
            continue
        
        if date in excl_list:
            continue
        
        yield date

def verif_schedule(dates, verif_count, make_shuf_indexes_func=None):
    if make_shuf_indexes_func is None:
        make_shuf_indexes_func = shuf.make_shuf_indexes
    
    sch_dates = tuple([date, 0] for date in dates)
    
    shuf_iter = itertools.cycle(make_shuf_indexes_func(len(sch_dates)))
    for verif_i in range(verif_count):
        shuf_i = next(shuf_iter)
        sch_dates[shuf_i][1] += 1
    
    for sch_dates in sch_dates:
        for sch_dates_i in range(sch_dates[1]):
            # TODO: for Python-3.3+ we may use ``yield from`` and ``itertools.repeat``
            yield sch_dates[0]
