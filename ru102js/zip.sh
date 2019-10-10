#!/bin/bash

rm -f ru102js-project.zip
zip -r ru102js-project.zip redisolar -x "redisolar/.vscode/*" -x "redisolar/node_modules/*" -x redisolar/.gitignore -x "redisolar/**/.DS_Store"
