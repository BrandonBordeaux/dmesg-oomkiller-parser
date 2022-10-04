#!/usr/bin/env python3

import argparse
import os
import sys

directory = ''
file_str = ''
about = 'Parse dmesg logs for oom-killer events and report on the top consumers'

# if no arguments
if not len(sys.argv) > 1:
    sys.exit(2)

# init parser
parser = argparse.ArgumentParser(description=about)
parser.add_argument("directory", nargs=1, help="Directory with dmesg logs")
parser.add_argument("file_part", nargs=1, help="Filename part to match")
args = parser.parse_args()

if args.directory:
    directory = args.directory[0]
    print(directory)
if args.file_part:
    file_str = args.file_part[0]
    print(file_str)

start = '[ pid ]   uid  tgid total_vm      rss nr_ptes swapents oom_score_adj name'
end = 'Out of memory: Kill process'
oom_cause = 'invoked oom-killer'
oom_killed = 'Killed process'

final_files = []
files = os.listdir(directory)

for f in files:
    if f.find(file_str) != -1:
        file_path = os.path.join(directory, f)
        final_files.append(file_path)

gb = float(1024)
reading = False

for f in final_files:
    consumers = []
    cause = ''
    killed = ''
    print('\n++++++++++++ {} ++++++++++++'.format(f))
    with open(f) as dmesg:
        for line in dmesg:
            if line.find(oom_cause) != -1:
                start_idx = line.find(']') + 1
                cause = line[start_idx:]
                print('\nCaused by: {}'.format(cause))
                continue

            if line.find(oom_killed) != -1:
                start_idx = line.find(']') + 1
                killed = line[start_idx:]
                print('\nProcess killed: {}'.format(killed))
                continue

            if line.find(start) != -1:
                reading = True
                continue
            elif line.find(end) != -1:
                reading = False

                sorted_consumers = sorted(consumers, key=lambda x: x[1], reverse=True)

                print('{0:<11} {1:<}'.format('rss (MB)', 'process'))
                print('======================')
                for i in sorted_consumers:
                    # Print size greater than 1 GB
                    if i[1] >= gb:
                        print('{0:<11.2f} {1:<}'.format(i[1], i[0]))

                continue
            elif reading:
                # Don't process empty lines
                if len(line) < 50:
                    continue

                line_list = line.split()

                pid = line_list[-9].replace('[', '').replace(']', '')
                name = line_list[-1]
                rss = float(line_list[-5]) * (4 * 1024) / 1024 / 1024
                process = '{} ({})'.format(pid, name)
                consumers.append((process, rss))
