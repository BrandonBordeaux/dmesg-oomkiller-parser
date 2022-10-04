# Dmesg oom-killer Parser

Parses dmesg logs for oom-killer events. Prints a report of:
- Process that invoked oom-killer
- Top rss comsumers more than 1 GB
- Process that was killed as a result

```commandline
usage: parse.py [-h] directory file_part

Parse dmesg logs for oom-killer events and report on the top consumers

positional arguments:
  directory   Directory with dmesg logs
  file_part   Filename part to match

optional arguments:
  -h, --help  show this help message and exit
```