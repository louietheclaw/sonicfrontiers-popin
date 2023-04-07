# Copyright (c) Adubbz
# Modified by louietheclaw

# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.

# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
 
import argparse
import struct
import subprocess
import shutil
import sys
from distutils.dir_util import copy_tree
from glob import glob
from pathlib import Path

GEDIT_BLACKLIST = [
    'w1r03_disable_slotstar01.gedit',
    'w1r03_disable_slotstar02.gedit',
    'w1r04_disable_slotstar01.gedit',
    'w1r05_disable_slotstar01.gedit',
    'w2r01_disable_slotstar01.gedit',
    'w3r01_disable_slotstar01.gedit',
    'w3r01_disable_drawbridge.gedit'
]

def read(offset, size):
    return data[offset:offset+size]

def write(offset, new_data):
    global data
    data[offset:offset+len(new_data)] = new_data

def read_string(offset):
    str = ''
    c = chr(data[offset])
    while c != '\0':
        str += chr(data[offset])
        offset += 1
        c = chr(data[offset])
    return str

def unpack(format, offset):
    return struct.unpack_from(format, data, offset)

def cleanup():
    for path in glob(f'{args.gedit_folder}/*/'):
        shutil.rmtree(path, ignore_errors=True)

def backup():
    backup_dir = Path(Path(args.gedit_folder).parent, 'gedit_bak')
    shutil.rmtree(backup_dir, ignore_errors=True)
    copy_tree(str(args.gedit_folder), str(backup_dir.absolute()))

def load_multipliers(filepath):
    multipliers = {}
    with open(filepath) as multiplier_file:
        for line in multiplier_file:
            key, value = line.partition("=")[::2]
            multipliers[key.strip()] = float(value)
    return multipliers

parser = argparse.ArgumentParser(prog='Bubbler', description='Increases the range for object pop-in in Sonic Frontiers')
parser.add_argument('hedge_arc_pack', help='Full Path to HedgeLib HedgeArcPack.exe including the executable filename')
parser.add_argument('gedit_folder', help='Path to gedit folder. Copy this out of game files before working on it!')
parser.add_argument('multiplier_file', help='Path to ini you will use for multipliers')
args = parser.parse_args()

# Cleanup any existing folders
cleanup()

# Backup the gedit folder
backup()

# Load multiplier values from file
multipliers = load_multipliers(args.multiplier_file)

# Start by unpacking all the pac files in the gedit folder
for path in Path(args.gedit_folder).glob('*.pac'):
    if not 'r' in path.name:
        continue

    subprocess.run([args.hedge_arc_pack, path])

for path in Path(args.gedit_folder).rglob('*.gedit'):
    # Skip blacklisted files
    if path.name in GEDIT_BLACKLIST:
        print(f'Skipping {path.name} (blacklisted)')
        continue

    # Read the gedit file
    with open(path, 'rb') as f:
        print(f'Reading {path}')
        data = bytearray(f.read())

    magic, version, endianness, file_size, block_count = unpack('<4s3scIH', 0)

    if magic != b'BINA':
        sys.exit('Invalid file magic')

    print(f'Found {block_count} block(s)')

    block_start = 0x10

    for i in range(block_count):
        block_signature, block_size = unpack('<4sI', block_start)

        if block_signature == b'DATA':
            str_table_offset, str_table_size, off_table_size, relative_data_offset = unpack('<IIIH', block_start+0x8)
            
            block_data_start = block_start + 0x18 + relative_data_offset
            object_offset_table_offset, object_count = unpack('<QQ', block_data_start+0x10)
            
            object_offsets = map(lambda off: block_data_start + off, unpack(f'<{object_count}Q', block_data_start+object_offset_table_offset))
            
            # Iterate over all objects
            for object_offset in object_offsets:
                object_type_offset, object_name_offset = unpack('<QQ', object_offset+0x8)
                tags_offset_table_offset, tag_count = unpack('<QQ', object_offset+0x70)

                object_type = read_string(block_data_start+object_type_offset)
                object_name = read_string(block_data_start+object_name_offset)
                print(f'{object_name}\n Type: {object_type}\n Tags ({tag_count}):')

                tag_offsets = map(lambda off: block_data_start + off, unpack(f'<{tag_count}Q', block_data_start+tags_offset_table_offset))

                # Iterate over all tags
                for tag_offset in tag_offsets:
                    type_offset, tag_data_length, tag_data_offset = unpack('<QQQ', tag_offset+0x8)

                    tag_type = read_string(block_data_start+type_offset)
                    tag_data = read(block_data_start+tag_data_offset, tag_data_length)

                    print(f'  {tag_type}:')

                    if tag_type == 'RangeSpawning':
                        if object_type not in multipliers:
                            print(f'WARN: Object type {object_type} not assigned a multiplier. Skipping...')
                            continue
                        multiplier = multipliers[object_type]
                        range_in, range_out = struct.unpack('<ff', tag_data)
                        print(f'Multiplier {multiplier}\n   Range In {range_in} -> {range_in * multiplier}\n   Range Out {range_out} -> {range_out * multiplier}')

                    # Replace the range data
                    write(block_data_start+tag_data_offset, struct.pack('<ff', range_in * multiplier, range_out * multiplier))

                    # Write the data back to the file
                    with open(path, 'wb') as f:
                        f.write(data)

        block_start += block_size

# Re-pack the files
for path in glob(f'{args.gedit_folder}/*/'):
    print('Packing ' + path)
    subprocess.run([args.hedge_arc_pack, '-P', '-E=little', '-S=0', '-T=frontiers', path])

# Clean up the old folders
cleanup()