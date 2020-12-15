#
#    Copyright (c) 2019 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Installer for FilePile"""

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO

import configobj
from weecfg.extension import ExtensionInstaller

filepile_config = """
    [FilePile]
        # Where to find the incoming new data:
        filename = /var/tmp/filepile.txt
        # What unit system they will be in.
        # Choices are 'US', 'METRIC', or 'METRICWX'
        unit_system = METRICWX
        # Map from incoming names, to WeeWX names.
        [[label_map]]
            # Example: incoming observation 'filelabel1' will be mapped to 'extraTemp4'
            filelabel1 = extraTemp4
"""

filepile_dict = configobj.ConfigObj(StringIO(filepile_config))


def loader():
    return FilePileInstaller()


class FilePileInstaller(ExtensionInstaller):
    def __init__(self):
        super(FilePileInstaller, self).__init__(
            version="0.4",
            name='filepile',
            description='Augment WeeWX records with data from a file',
            author="Thomas Keffer",
            author_email="tkeffer@gmail.com",
            data_services='user.filepile.FilePile',
            config=filepile_dict,
            files=[('bin/user', ['bin/user/filepile.py'])]
            )
