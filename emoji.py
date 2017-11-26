#!/usr/bin/env python3

import json
import os
import subprocess


def svg2png(src, dst, size):
    if not os.path.isfile(src):
        raise Exception("File not found")

    if os.path.isfile(dst):
        dstat = os.stat(dst)
        sstat = os.stat(src)
        if dstat.st_mtime > sstat.st_mtime:
            return
        return

    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    print(os.path.basename(dst))
    subprocess.call(['rsvg-convert', '-f', 'png', src, '-o', dst, '-w', str(size), '-h', str(size)])
    subprocess.call(['pngcrush', '-ow', dst])


def main():
    emoji = json.load(open(os.path.join('emojione', 'emoji.json')))
    result = []

    for name in emoji:
        data = emoji[name]
        category = data['category']
        code = emoji[name]['unicode']
        filename = os.path.join('emojione', 'assets', 'svg', code + '.svg')

        if category in ('modifier', 'regional'):
            continue

        svg2png(filename, os.path.join('png-64', category, name + '.png'), 64)
        svg2png(filename, os.path.join('png-256', category, name + '.png'), 256)
        svg2png(filename, os.path.join('png-512', category, name + '.png'), 512)

        if '-' in name:
            continue

        result.append({
            'category': category,
            'name': name})

    catmap = {'activity': 2, 'flags': 9, 'food': 3, 'nature': 4, 'objects': 5, 'people': 1, 'travel': 6, 'modifier': 7, 'symbols': 8, 'regional': 10}

    result.sort(key=lambda x: emoji[x['name']]['emoji_order'])
    result.sort(key=lambda x: catmap[x['category']])

    json.dump(result, open('emoji.json', 'w'), indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
