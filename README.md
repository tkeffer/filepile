# FilePile
WeeWX service for additional types from a file to a WeeWX data stream

## Installation instructions

1) Install the extension

    ```shell
    wee_extension --install=path-to-filepile
    ```

2) Restart WeeWX. For example:

   ```shell
   sudo systemctl stop weewx
   sudo systemctl start weewx
   ```



## Manual installation instructions

1. Include a stanza in your `weewx.conf` configuration file that looks like this:

    ```ini
    [FilePile]
        filename = /var/tmp/filepile.txt
        unit_system = METRIC  # Or, 'US' or 'METRICWX'
        # Map from incoming names, to WeeWX names.
        [[label_map]]
            temp1 = extraTemp1     # Incoming name 'temp1' will get mapped to 'extraTemp1'
            humid1 = extraHumid1   # Incoming name 'humid1' will get mapped to 'extraHumid1'
    ``` 
    
    The default values are:

    |option | default| meaning |
    | ----------- | ----------- | ----- |
    |`filename`| `/var/tmp/filepile.txt`| Location of data file |
    |`unit_system`| `METRICWX`| The unit system it will be in |
    | `[[label_map]]` |  *no mapping*         | Map an incoming name to a WeeWX name|

2. Add the FilePile service to the list of `data_services`:

    ```ini
    [Engine]
        [[Services]]
          ...
          data_services = user.filepile.FilePile
          ...
    
3. Put this file (`filepile.py`) in your WeeWX `user` subdirectory.
For example, if you installed using `setup.py`:

    ```shell
    cp filepile.py /home/weewx/bin/user
    ```

4. Have your external data source write values to the file
(`/var/tmp/filepile.txt` in the example above) in the following
format:    

    ```
    key = value
    ```
    where `key` is an observation name, and `value` is its value.

    If `key` appears in the `label_map`, then it will be mapped to a corresponding
name. If not, then `key` will be used.

    The value `None` can be used to signify a bad data value.
