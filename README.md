### Python Challenge

```
usage: xfipchk.py [-h] {cli,web} ...

Use the X-Force API to check IP address reputation.

positional arguments:
  {cli,web}   Mutually exclusive sub-commands
    cli       Command-line Interface; run 'xfipchk cli -h' to see options
    web       Web interface; run 'xfipchk web -h' to see options


cli:
    xfipchk.py cli [-h] [-o [output_file]]
                          [-i ip_address | -I file_of_ip_addresses]
                          authN

    positional arguments:
      authN                 Path to a file containing your X-Force credentials,
                            key and password on first and second lines,
                            respectively.

    optional arguments:
      -h, --help            show this help message and exit
      -o [output_file], --out [output_file]
                            Write result of X-Force call to file; if this option
                            is elected but no filename is provided, a file will be
                            created for the user.
      -i ip_address, --ip ip_address
                            An IP address to be checked via X-Force. If the
                            IPaddress is omitted or invalid, the user will be
                            prompted for one.
      -I file_of_ip_addresses, --Ips file_of_ip_addresses
                            A file containing IP addresses, one per line.

web:
    usage: xfipchk.py web [-h] [-p PORT] [-a ADDRESS]

    Web Interface:
      You may specify the address and port to bind to; defaults are 127.0.0.1
      and 8000

      -p PORT, --port PORT
      -a ADDRESS, --address ADDRESS


```