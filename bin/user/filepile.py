#
#    Copyright (c) 2019 Tom Keffer <tkeffer@gmail.com>
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
    ignore_value_error = False
    # Map from incoming names, to WeeWX names.
    [[label_map]]
        temp1 = extraTemp1
        humid1 = extraHumid1


2. Add the FilePile service to the list of data_services to be run:

[Engine]
  [[Services]]
    ...
    data_services = user.filepile.FilePile

3. Put this file (filepile.py) in your WeeWX user subdirectory.
For example, if you installed using setup.py,

    cp filepile.py /home/weewx/bin/user

4. Have your external data source write values to the file
('/var/tmp/filepile.txt' in the example above) using the following
format:

    key = value

where 'key' is an observation name, and 'value' is its value.
The value can be 'None'.
"""

import weewx
import weewx.units
from weewx.wxengine import StdService
from weeutil.weeutil import to_float, to_bool

VERSION = "0.4"

try:
    # Test for new-style weewx logging by trying to import weeutil.logger
    import weeutil.logger
    import logging
    log = logging.getLogger(__name__)

    def logdbg(msg):
        log.debug(msg)

    def loginf(msg):
        log.info(msg)

    def logerr(msg):
        log.error(msg)

except ImportError:
    # Old-style weewx logging
    import syslog

    def logmsg(level, msg):
        syslog.syslog(level, 'filepile: %s:' % msg)

    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)

    def loginf(msg):
        logmsg(syslog.LOG_INFO, msg)

    def logerr(msg):
        logmsg(syslog.LOG_ERR, msg)


class FilePile(StdService):
    """WeeWX service for augmenting a record with data parsed from a file."""

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
        self.ignore_value_error = to_bool(filepile_dict.get('ignore_value_error', False))

        # Mapping from variable names to weewx names
        self.label_map = filepile_dict.get('label_map', {})

        loginf("Using %s with the '%s' unit system" % (self.filename, unit_system_name))
        loginf("Label map is %s" % self.label_map)

        # Bind to the NEW_ARCHIVE_RECORD event
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)

    def new_archive_record(self, event):
        new_record_data = {}
        try:
            with open(self.filename, 'r') as fd:
                for line in fd:
                    eq_index = line.find('=')
                    # Ignore all lines that do not have an equal sign
                    if eq_index == -1:
                        continue
                    name = line[:eq_index].strip()
                    value = line[eq_index + 1:].strip()
                    # Values which are empty strings are interpreted as None
                    if value == '':
                        value_f = None
                    else:
                        try:
                            value_f = to_float(value)
                        except ValueError as e:
                            if self.ignore_value_error:
                                continue
                            logerr("Could not convert to float: %s" % value)
                            raise
                    new_record_data[self.label_map.get(name, name)] = value_f
                # Supply a unit system if one wasn't included in the file
                if 'usUnits' not in new_record_data:
                    new_record_data['usUnits'] = self.unit_system
                # Convert the new values to the same unit system as the record
                target_data = weewx.units.to_std_system(new_record_data, event.record['usUnits'])
                # Add the converted values to the record:
                event.record.update(target_data)
        except IOError as e:
            logerr("Cannot open file. Reason: %s" % e)
