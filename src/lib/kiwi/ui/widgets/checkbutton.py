#
# Kiwi: a Framework and Enhanced Widgets for Python
#
# Copyright (C) 2003-2005 Async Open Source
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
# USA
#
# Author(s): Christian Reis <kiko@async.com.br>
#            Gustavo Rahal <gustavo@async.com.br>
#            Johan Dahlin <jdahlin@async.com.br>
#            Lorenzo Gil Sanchez <lgs@sicem.biz>
#

"""GtkCheckButton support for the Kiwi Framework"""

import gtk

from kiwi import ValueUnset
from kiwi.python import deprecationwarn
from kiwi.ui.proxywidget import ProxyWidgetMixin
from kiwi.utils import PropertyObject, gsignal, type_register

class ProxyCheckButton(PropertyObject, gtk.CheckButton, ProxyWidgetMixin):
    __gtype_name__ = 'ProxyCheckButton'

    # changed allowed data types because checkbuttons can only
    # accept bool values
    allowed_data_types = bool,

    def __init__(self, label=None, use_underline=True):
        ProxyWidgetMixin.__init__(self)
        PropertyObject.__init__(self, data_type=bool)
        gtk.CheckButton.__init__(self, label=label,
                                 use_underline=use_underline)

    gsignal('toggled', 'override')
    def do_toggled(self):
        self.emit('content-changed')
        self.chain()

    def read(self):
        return self.get_active()

    def update(self, data):
        if data is None or data is ValueUnset:
            self.set_active(False);
            return

        # No conversion to string needed, we only accept bool
        self.set_active(data)

class CheckButton(ProxyCheckButton):
    def __init__(self):
        deprecationwarn(
            'CheckButton is deprecated, use ProxyCheckButton instead',
            stacklevel=3)
        ProxyCheckButton.__init__(self)
type_register(CheckButton)
