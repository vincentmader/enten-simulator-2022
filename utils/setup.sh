#!/bin/sh

cd "$(dirname $0)"
PATH_TO_SCRIPTS=$(pwd)

pip3 install -r ../requirements.txt

python3 "$PATH_TO_SCRIPTS/create_sprites.py" ducks
python3 "$PATH_TO_SCRIPTS/create_sprites.py" miniducks
python3 "$PATH_TO_SCRIPTS/create_sprites.py" monkeys
python3 "$PATH_TO_SCRIPTS/create_sprites.py" ostriches
python3 "$PATH_TO_SCRIPTS/create_sprites.py" penguins
python3 "$PATH_TO_SCRIPTS/create_sprites.py" bears
