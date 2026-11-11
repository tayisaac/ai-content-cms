#!/usr/bin/env bash
# Seeds an eval workspace with the fictional ClearView project and one run folder.
# Usage (from a case's scaffold script): seed.sh <run fixture: bad|clean|outline> <run folder name>
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$here/ClearView" ./ClearView
mkdir -p "ClearView/runs/$2"
cp "$here/runs/$1/blueprint.json" "ClearView/runs/$2/blueprint.json"
