import re

def remove_group_channels(lines) -> list:
    """
    Removes grouping channels similar to ----- DE DEUTSCHLAND -----.
    """
    pattern = "----- \w*\s*\w* -----"
    remove_line = False
    for line_id, line in enumerate(lines.copy()):
        if remove_line:
            lines.remove(line)
            remove_line = False
        if line_id % 2 != 0:
            if re.search(pattern,line):
                lines.remove(line)
                remove_line = True
    return lines

def create_channel_groups_pattern() -> str:
    """
    Creates the pattern of the channel groups which are to be kept.
    The result is later used in remove_groups() to remove channel groups not contained in this pattern.
    """
    groups = ['DE DEUTSCHLAND','DE DOKU','DE SPORT','AT AUSTRIA','CH SUISSE - SWITZERLAND','CH SUISSE - SWITZERLAND SPORT','EXYU SPORT','EXYU MUZICKI','BH BOSNIA AND HERZEGOVINA']
    pattern = ''
    for id, group in enumerate(groups):
        if id+1 == len(groups):
            pattern = pattern + '"' + group
        else:
            pattern = pattern + '"' + group + '|'
    return pattern

def remove_groups(lines) -> list:
    """
    Removes channel groups which are not needed/wanted.
    """
    pattern = create_channel_groups_pattern()
    remove_line = False
    for line_id, line in enumerate(lines.copy()):
        if remove_line:
            lines.remove(line)
            remove_line = False
        if line_id % 2 != 0:
            if not re.search(pattern,line):
                lines.remove(line)
                remove_line = True
    return lines

def add_chno(lines) -> list:
    """
    Adds a channel number for each channel in order to sort them later on in Jellyfin.
    """
    channel_list = []
    chno = 1
    for line_id, line in enumerate(lines):
        if line_id % 2 != 0:
            index = line.find('tvg-logo=')
            line = line[:index] + f'tvg-chno="{chno}" ' + line[index:]
            chno += 1
        channel_list.append(line)
    return channel_list

def remove_tvgid(channel_list) -> str:
    """
    Removes the tvg_id attribute from each line as this is not needed.
    """
    pattern = 'tvg-id="\S*" '
    channel_list = ''.join([str(item) for item in channel_list])
    channel_list = re.sub(pattern,'',channel_list)
    return channel_list

def create_m3u(channel_list, output_file):
    m3u_file = open(output_file, "w")
    m3u_file.write(channel_list)
    m3u_file.close()