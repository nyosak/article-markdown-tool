#!/usr/bin/env python3

r"""
article publishing tools:
module conf:
current settings
copyright 2025, hanagai

conf/conf_current.py
version: June 1, 2025
"""

import os.path
from pathlib import Path
import re
import datetime
import random

if __name__ == '__main__':
    import conf_dirs
else:
    from conf import conf_dirs

TMP = conf_dirs.TMP
BASE = conf_dirs.BASE
DOC = os.path.join(BASE, 'docs')
QIITA = conf_dirs.QIITA
Q_DOC = os.path.join(QIITA, 'public')
ZENN = conf_dirs.ZENN
Z_DOC = os.path.join(ZENN, 'articles')

def current_setting_file_name(name):
    r"""
    get current setting file name
    """
    return os.path.join(TMP, f'current_{name}')

def get_current(name):
    r"""
    get current settings
    """
    file = current_setting_file_name(name)
    if os.path.exists(file) and os.path.isfile(file):
        with open(file, 'r') as f:
            value = f.read().strip()
            return value
    else:
        return None

def set_current(name, value):
    r"""
    set current settings
    """
    file = current_setting_file_name(name)
    with open(file, 'w') as f:
        f.write(value)

def a():
    r"""
    get current `a` path
    """
    return os.path.join(DOC, get_current('series'))

def meta():
    r"""
    get current `meta` path
    """
    return os.path.join(DOC, 'met' + get_current('series'))

def media():
    r"""
    get current `media` path
    """
    return os.path.join(DOC, 'medi' + get_current('series'))

def a_path():
    r"""
    get current `document md` path
    """
    return os.path.join(a(), get_current('key') + '.md')

def meta_path():
    r"""
    get current `meta yaml` path
    """
    return os.path.join(meta(), get_current('key') + '.yaml')

def media_path(name):
    r"""
    get current `media file` path
    """
    base_name = os.path.basename(name)
    key = f"{get_current('key')}_"
    if base_name.startswith(key):
        new_name = base_name
    else:
        new_name = f'{key}{base_name}'
    return os.path.join(media(), new_name)

def readme_path():
    r"""
    get current `readme md` path
    """
    return os.path.join(BASE, 'README.md')

def qiita_name():
    r"""
    get current name for qiita article
    """
    return get_current('key')

def zenn_name():
    r"""
    get current name for zenn article
    """
    key = get_current('key')
    found = list(Path(Z_DOC).glob(f'{key}-*.md'))
    match len(found):
        case 0: # generate new one
            digit = str(random.randint(10000, 99999))
            name = f'{key}-{digit}'
            print(f'new zenn article name generated: {name}')
        case 1: # use existing one
            name = found[0].stem.split('.')[0]
        case _: # not expected
            print(f'Warning: multiple files found for {key}.')
            print([f.stem for f in found])
            raise ValueError(f'Multiple files found for {key}. Please resolve the conflict.')
    return name

def qiita_path():
    r"""
    get current `qiita article md` path
    """
    return os.path.join(Q_DOC, qiita_name() + '.md')

def zenn_path():
    r"""
    get current `zenn article md` path
    """
    return os.path.join(Z_DOC, zenn_name() + '.md')

def date_format_reiwa(date):
    r"""
    convert date to Reiwa date string
    as YMMDD
    """
    reiwa_year = date.year - 2018
    formatted_date = str(reiwa_year).zfill(1) + date.strftime("%m%d")
    return formatted_date

def date_parse_reiwa(reiwa_date):
    r"""
    convert Reiwa date string to gregorian date time
    from YMMDD
    """
    year_length = len(reiwa_date) - 4
    year = int(reiwa_date[:year_length]) + 2018
    month_day = reiwa_date[year_length:]
    parsed = datetime.datetime.strptime(f'{year}{month_day}', '%Y%m%d')
    return parsed

def reiwa_now():
    r"""
    get reiwa now string
    as YMMDD
    """
    now = datetime.datetime.now()
    return date_format_reiwa(now)

def reiwa_day_ago(now_string):
    r"""
    get past days from specified reiwa now string
    from YMMDD
    """
    now = datetime.datetime.now()
    past = date_parse_reiwa(now_string)
    days = (now - past).days
    return days

def used_tags_str(top=0):
    r"""
    get used tags as string delimited by space
    """
    return ' '.join(used_tags(top=top))

def used_tags(top=0):
    r"""
    get used tags
    with positive top: sorted by occurrence descending
    otherwise: all tags sorted by alphabet
    """
    all_tags_nested = with_all_meta_yaml(read_yaml_tags)
    all_tags = [tag for tags in all_tags_nested for tag in tags] # flatten
    uniq_tags = sorted(set(all_tags))

    if top > 0:
        add_count = {}
        for tag in uniq_tags:
            add_count[tag] = all_tags.count(tag)
        #add_count['Ubuntu'] += 1
        #add_count['Android'] += 2
        sorted_tags = sorted(add_count.items(), key=lambda x: x[1], reverse=True)
        top_tags = [tag for tag, count in sorted_tags][:top]
        return top_tags
    else:
        return uniq_tags

def with_all_meta_yaml(func):
    r"""
    scan for all meta yaml
    """
    yamls = list(Path(DOC).glob('met*/*.yaml'))
    return [func(yaml) for yaml in yamls if yaml.is_file()]

def find_a_random_meta_yaml():
    r"""
    find a random meta yaml
    for testing
    """
    import random

    yamls = list(Path(DOC).glob('met*/*.yaml'))
    if len(yamls) > 0:
        return yamls[random.randrange(len(yamls))]
    else:
        return None

def read_yaml(yaml):
    r"""
    read yaml file
    """
    result = {}
    if os.path.exists(yaml) and os.path.isfile(yaml):
        with open(yaml, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if re.search(r'.:', line):
                key, value = line.split(':', 1)
                clean_value = value.strip()
                if key == 'tags':
                    tags = clean_value.split()
                    result[key] = tags
                else:
                    result[key] = clean_value
    return result

def read_yaml_tags(yaml):
    r"""
    read yaml file and return tags
    """
    return read_yaml(yaml).get('tags', [])



def test():
    print('test launched manually.')
    print('TMP:', TMP)
    print('BASE:', BASE)
    print('DOC:', DOC)
    print('current_setting_file_name:', current_setting_file_name('test'))
    print('get:', get_current('test'))
    #print('set:', set_current('test', 'test_value'))
    #print('get:', get_current('test'))
    #print('set:', set_current('test', 'test_value2'))
    #print('get:', get_current('test'))
    print('a:', a())
    print('meta:', meta())
    print('media:', media())
    print('a_path:', a_path())
    print('meta_path:', meta_path())
    print('media_path:', media_path('test.png'))
    print('readme_path:', readme_path())
    print('qiita_name:', qiita_name())
    print('zenn_name:', zenn_name())
    print('qiita_path:', qiita_path())
    print('zenn_path:', zenn_path())
    print('date_format_reiwa:', date_format_reiwa(datetime.datetime.now()))
    print('date_parse_reiwa:', date_parse_reiwa('60229'))
    print('date_parse_reiwa:', date_parse_reiwa('320420'))
    try:
        print('date_parse_reiwa:', date_parse_reiwa('70229'))
    except ValueError as e:
        print('date_parse_reiwa 70229 error as expected:', e)
    print('reiwa_now:', reiwa_now())
    print('reiwa_day_ago:', reiwa_day_ago('70509'))
    print('reiwa_day_ago:', reiwa_day_ago('80528'))
    print('reiwa_day_ago:', reiwa_day_ago(reiwa_now()))
    print('used_tags_str:', used_tags_str())
    print('used_tags_str:', used_tags_str(5))
    print('used_tags:', used_tags())
    print('used_tags:', used_tags(3))
    print('used_tags:', used_tags(30))
    print('used_tags:', used_tags(0))
    print('with_all_meta_yaml:', with_all_meta_yaml(read_yaml_tags))
    print('read_yaml:', read_yaml(find_a_random_meta_yaml()))
    print('read_yaml:', read_yaml('test.yaml'))
    print('read_yaml_tags:', read_yaml_tags(find_a_random_meta_yaml()))
    print('read_yaml_tags:', read_yaml_tags('test.yaml'))

if __name__ == '__main__':
    test()
