#!/bin/sh

rm -rf build
mkdir -p build/megascans build/python
cp src/*.json build/
cp -r src/menu build/megascans/
python -m pip install . --target build/python
cd build
zip -r megascans-$NEW_VERSION.zip .
