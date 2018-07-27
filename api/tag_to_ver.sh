#!/bin/bash

tag=$(git describe --abbrev=0 --tags)

cat > namex/VERSION.py << EOF
__version__='$tag'
EOF
