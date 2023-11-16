from functions import remove_group_channels, remove_groups, add_chno, remove_tvgid, create_m3u
import re


INPUT_FILE = "files/tv_channels_mrVWSURFKf_plus.m3u"
OUTPUT_FILE = "files/ammar_iptv.m3u"

with open(INPUT_FILE) as f:
    lines = f.readlines()
print(len(lines))

lines = remove_group_channels(lines)
print(len(lines))

lines = remove_groups(lines)
print(len(lines))

channel_list = add_chno(lines)
print(len(channel_list))

channel_list = remove_tvgid(channel_list)

create_m3u(channel_list, OUTPUT_FILE)