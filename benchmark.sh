#!/usr/bin/env bash
set -euo pipefail

TAG="${1:-naive}"
DOCKERFILE="${2:-Dockerfile.train.${TAG}}"
IMAGE="iris-train:${TAG}"

[[ -f "$DOCKERFILE" ]] || { echo "Dockerfile introuvable : $DOCKERFILE" >&2; exit 1; }
[[ -f train.py ]] || { echo "train.py introuvable" >&2; exit 1; }

cp train.py train.py.bak
trap 'mv -f train.py.bak train.py' EXIT

echo "Build à froid..."
START=$(date +%s)
docker build --no-cache -f "$DOCKERFILE" -t "$IMAGE" . > build_froid.log 2>&1
FROID=$(( $(date +%s) - START ))

echo "Rebuild après modification..."
echo "# modification benchmark" >> train.py
START=$(date +%s)
docker build -f "$DOCKERFILE" -t "$IMAGE" . > build_chaud.log 2>&1
CHAUD=$(( $(date +%s) - START ))

TAILLE=$(docker image inspect "$IMAGE" --format '{{.Size}}')
TAILLE_MO=$(( TAILLE / 1000000 ))

echo
echo "Image : $IMAGE"
echo "Taille : ${TAILLE_MO} Mo"
echo "Build à froid : ${FROID} s"
echo "Rebuild à chaud : ${CHAUD} s"
