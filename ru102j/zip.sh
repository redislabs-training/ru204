#!/bin/bash

rm ru102j-project.zip
zip -r ru102j-project.zip project -x "project/.idea/*" -x "project/*.iml" -x "project/target/*" -x project/.gitignore -x "project/**/.DS_Store"
