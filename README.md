# FilePile
WeeWX service for additional types from a file to a WeeWX data stream

## Installation instructions

1. Arrange to have your new data saved to a file, say `/var/tmp/pond.txt`. It should be in the following
format:

    ```
    extraTemp1 = 45.5
    extraHumid1 = None
    myVoltage = 12.2
    ```
    
    The value `None` is a valid value and signifies a bad data point.
    
2. Install the extension

    ```shell
    wee_extension --install=path-to-filepile
    ```

3. Edit the new stanza `[FilePile]` to reflect your situation. Here's an example:

   ```ini
   [FilePile]
       filename = /var/tmp/pond.txt
       unit_system = US
       [[label_map]]
           myVoltage = supplyVoltage
   ```
   In this example, the incoming data will be found in the file `/var/tmp/pond.txt` and it
will be in the [US Customary](http://weewx.com/docs/customizing.htm#units) unit system.

   The incoming observation type `myVoltage` will get mapped to the WeeWX type `supplyVoltage`. The
other two types in the file (`extraTemp1` and `extraHumid1` in the example above), do not appear in the mapping, so
they will appear under their own names `extraTemp1` and `extraHumid1`.

4. Restart WeeWX. For example:

   ```shell
   sudo systemctl stop weewx
   sudo systemctl start weewx
   ```

5. On every archive interval, your temporary file will be read, parsed,
and its contents added to the WeeWX record. 


## Manual installation instructions

1. Arrange to have your new data saved to a file, say `/var/tmp/pond.txt`. It should be in the following
format:

    ```
    extraTemp1 = 45.5
    extraHumid1 = None
    myVoltage = 12.2
    ```
    
    The value `None` is a valid value and signifies a bad data point.
    
2. Include a stanza in your `weewx.conf` configuration file that looks like this. Adjust
the options as necessary:

    ```ini
    [FilePile]
        filename = /var/tmp/pond.txt
        unit_system = US  # Or, 'METRIC' or 'METRICWX'
        # Map from incoming names, to WeeWX names.
        [[label_map]]
            myVoltage = supplyVoltage   # Incoming name 'myVoltage' will get mapped to 'supplyVoltage'
    ``` 

3. Add the FilePile service to the list of `data_services`:

    ```ini
    [Engine]
        [[Services]]
          ...
          data_services = user.filepile.FilePile
          ...
    
4. Put the file `filepile.py` in your WeeWX `user` subdirectory.
For example, if you installed using `setup.py`:

    ```shell
    cp filepile.py /home/weewx/bin/user
    ```

5. Restart WeeWX. For example:

   ```shell
   sudo systemctl stop weewx
   sudo systemctl start weewx
   ```

6. On every archive interval, your temporary file will be read, parsed,
and its contents added to the WeeWX record. 


