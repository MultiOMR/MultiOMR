#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
xmllint --schema ${DIR}/musicxml.xsd $1

