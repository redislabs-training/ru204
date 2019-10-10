#!/bin/bash

rm -f ru102js-project.zip
zip -r ru102js-project.zip project -x "project/.vscode/*" -x "project/node_modules/*" -x project/.gitignore -x "project/**/.DS_Store"
