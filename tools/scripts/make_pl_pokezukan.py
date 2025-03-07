#!/usr/bin/env python3
import argparse
import json
import pathlib
import subprocess

from consts.species import PokemonSpecies


argparser = argparse.ArgumentParser(
    prog='make_pl_pokezukan_py',
    description='Packs the archive containing NatDex->SinnohDex number mapping'
)
argparser.add_argument('-n', '--narc',
                       required=True,
                       help='Path to narc executable')
argparser.add_argument('-s', '--source-dir',
                       required=True,
                       help='Path to the source directory (res/pokemon)')
argparser.add_argument('-p', '--private-dir',
                       required=True,
                       help='Path to the private directory (where binaries will be made)')
argparser.add_argument('-o', '--output-dir',
                       required=True,
                       help='Path to the output directory (where the NARC will be made)')
argparser.add_argument('pokedex',
                       help='List of pokemon in the Sinnoh Pokedex')
args = argparser.parse_args()

source_dir = pathlib.Path(args.source_dir)
private_dir = pathlib.Path(args.private_dir)
output_dir = pathlib.Path(args.output_dir)

private_dir.mkdir(parents=True, exist_ok=True)

NUM_POKEMON = 494

pokedex = [0 for i in range(NUM_POKEMON)]

with open(args.pokedex) as data_file:
    dex_data = json.load(data_file)
    for i, mon in enumerate(dex_data):
        pokedex[PokemonSpecies[mon].value] = i

target_fname = private_dir / 'pl_pokezukan_0.bin'
with open(target_fname, 'wb+') as target_file:
    pl_pokezukan = [0 for i in range(NUM_POKEMON * 2)]
    for i in range(NUM_POKEMON):
        pl_pokezukan[i*2] = pokedex[i] & 0xff
        pl_pokezukan[i*2 + 1] = (pokedex[i] >> 8) & 0xff
    target_file.write(bytes(pl_pokezukan))

subprocess.run([args.narc, 'create', '--output', output_dir / 'pl_pokezukan.narc', private_dir])
