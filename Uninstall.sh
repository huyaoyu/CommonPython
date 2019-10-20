#!/bin/bash

echo "Remove installed files."

cat .InstalledFiles.txt | xargs rm -rf

echo "Uninstall done."

