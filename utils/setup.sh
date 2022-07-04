#!/bin/sh

cd "$(dirname $0)"
PATH_TO_SCRIPTS=$(pwd)

python3 "$PATH_TO_SCRIPTS/create_sprites.py" ducks
python3 "$PATH_TO_SCRIPTS/create_sprites.py" miniducks
