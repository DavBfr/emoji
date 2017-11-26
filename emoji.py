#!/usr/bin/env python3

import glob
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
        
        if '_tone' in name:
            continue

        result.append({
            'category': category,
            'name': name})

    category = 'emojis'
    for filename in glob.glob(os.path.join(category, '*.svg')):
        name = os.path.splitext(os.path.basename(filename))[0]

        svg2png(filename, os.path.join('png-64', category, name + '.png'), 64)
        svg2png(filename, os.path.join('png-256', category, name + '.png'), 256)
        svg2png(filename, os.path.join('png-512', category, name + '.png'), 512)

        result.append({
            'category': category,
            'name': name})

        if name not in emoji:
            emoji[name] = {'emoji_order': name}

    catmap = {'emojis': 1, 'activity': 3, 'flags': 10, 'food': 4, 'nature': 5, 'objects': 6, 'people': 2, 'travel': 7, 'modifier': 8, 'symbols': 9, 'regional': 11}

    result.sort(key=lambda x: emoji[x['name']]['emoji_order'])
    result.sort(key=lambda x: catmap[x['category']])

    json.dump(result, open('emoji.json', 'w'), indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
