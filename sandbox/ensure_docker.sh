#!/usr/bin/env bash
# Exit 0 once the Docker daemon answers; on macOS start Docker Desktop if needed (waits up to 90 s).
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
docker info >/dev/null 2>&1 && exit 0
[ "$(uname)" = Darwin ] && open -ga Docker
for _ in $(seq 45); do sleep 2; docker info >/dev/null 2>&1 && exit 0; done
echo "Docker daemon not available. Start Docker, or set MINER_SANDBOX=host / PUBLISH_SANDBOX=host (UNSAFE: runs model code on this machine)." >&2
exit 1
