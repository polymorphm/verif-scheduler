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

def make_shuf_indexes(stop):
    indexes = []
    level = 0
    step = 1
    
    while step <= stop:
        level_indexes = []
        
        for i in range(0, stop, step):
            if step > 1:
                indexes.remove(i)
            level_indexes.append(i)
        
        level_indexes.extend(indexes)
        indexes = level_indexes
        
        level += 1
        step = step * 2
    
    return indexes
