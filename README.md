# FilePile
Add additional types to a WeeWX data stream via a file

To use:

1. Include a stanza in your `weewx.conf` configuration file that looks like this:

    ```ini
    [FilePile]
        filename = /var/tmp/filepile.txt
        unit_system = METRICWX      # Or, 'US' or 'METRIC'
    ``` 
    
    The default values are:

    |option | default| meaning |
    | ----------- | ----------- | ----- |
    |`filename`| `/var/tmp/filepile.txt`| Location of data file |
    |`unit_system`| `METRICWX`| The unit system it will be in |

2. Add the FilePile service to the list of `data_services`:

    ```ini
    [Engine]
        [[Services]]
          ...
          data_services = user.filepile.FilePile
          ...
    
3. Have your external data source write values to the file
(`/var/tmp/filepile.txt` in the example above) in the following
format:    

    ```
    key = value
    ```
where `key` is an observation name, and `value` is its value.
The value can be `None` to signify a bad data value.
