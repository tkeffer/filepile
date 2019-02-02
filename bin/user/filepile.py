#
#    Copyright (c) 2009-2015 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""
A WeeWX that parses a file, adding its contents to a WeeWX record.

To use:

1. Include a stanza in your weewx.conf configuration file:

[FilePile]
    filename = /var/tmp/filepile.txt
    unit_system = METRIC  # Or, 'US' or 'METRICWX'


2. Add the FilePile service to the list of data_services:

[Engine]
  [[Services]]
    ...
    data_services = user.filepile.FilePile

3. Have your external data source write values to the file
('/var/tmp/filepile.txt' in the example above) in the following
format:

    key = value

where key is an observation name, and value is its value.
The value can be 'None'.
"""

import syslog
import weewx
import weewx.units
from weewx.wxengine import StdService
from weeutil.weeutil import to_float


class FilePile(StdService):

    def __init__(self, engine, config_dict):
        # Initialize my superclass:
        super(FilePile, self).__init__(engine, config_dict)

        # Extract our stanza from the configuration dicdtionary
        filepile_dict = config_dict.get('FilePile', {})
        # Get the location of the file ...
        self.filename = filepile_dict.get('filename', '/var/tmp/filepile.txt')
        # ... and the unit system it will use
        unit_system_name = filepile_dict.get('unit_system', 'METRICWX').strip().upper()
        # Make sure we know about the unit system. If not, raise an exception.
        if unit_system_name not in weewx.units.unit_constants:
            raise ValueError("FilePile: Unknown unit system: %s" % unit_system_name)
        # Use the numeric code for the unit system
        self.unit_system = weewx.units.unit_constants[unit_system_name]

        syslog.syslog(syslog.LOG_INFO, "filepile: using %s with the '%s' unit system"
                      % (self.filename, unit_system_name))

        # Bind to the NEW_ARCHIVE_RECORD event
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)

    def new_archive_record(self, event):
        new_record_data = {'usUnits' : self.unit_system}
        try:
            with open(self.filename, 'rb') as fd:
                for line in fd:
                    eq_index = line.find('=')
                    # Ignore all lines that do not have an equal sign
                    if eq_index == -1:
                        continue
                    name = line[:eq_index].strip()
                    value = line[eq_index + 1:].strip()
                    new_record_data[name] = to_float(value)
                # Convert the new values to the same unit system as the record
                target_data = weewx.units.to_std_system(new_record_data, event.record['usUnits'])
                # Add the new values to the record:
                self.event.record.update(target_data)
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, "filepile: cannot open file. Reason: %s" % e)
