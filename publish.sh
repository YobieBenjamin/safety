#!/usr/bin/env bash
# One-command publish to github.com/YobieBenjamin/safety.
# Only unavoidable human step: be authenticated once (`gh auth login`) or export GITHUB_TOKEN.
set -euo pipefail
OWNER="${GH_OWNER:-YobieBenjamin}"; REPO="${GH_REPO:-safety}"
cd "$(dirname "$0")"
[ -f .venv/bin/activate ] && . .venv/bin/activate          # project-local Python deps
if [ "${PUBLISH_SANDBOX:-docker}" = docker ]; then          # default: verify untrusted code in the sandbox
  sandbox/ensure_docker.sh            # aborts publish (set -e) if Docker is unavailable
  scripts/changed_algorithms.sh > .verify_changed   # same selection as CI (Phase D)
  echo "verify: experiments for: $(tr '\n' ' ' < .verify_changed)"
  SANDBOX_MEM="${SANDBOX_MEM:-6g}" SANDBOX_TIMEOUT="${SANDBOX_TIMEOUT:-10800}" sandbox/run.sh . verify --ro   # aborts publish on failure
  rm -f .verify_changed
else                                                         # explicit opt-out: run on this machine
  if [ "$(uname)" = Darwin ] && [ -z "${SDKROOT:-}" ]; then   # macOS: pick an SDK the linker can read
    printf 'double f(double x){return x;}' > /tmp/_sdk_probe.c
    if ! gcc -shared -fPIC -o /tmp/_sdk_probe.so /tmp/_sdk_probe.c -lm 2>/dev/null; then
      for s in /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk \
               /Library/Developer/CommandLineTools/SDKs/MacOSX*.sdk; do
        SDKROOT="$s" gcc -shared -fPIC -o /tmp/_sdk_probe.so /tmp/_sdk_probe.c -lm 2>/dev/null && { export SDKROOT="$s"; break; }
      done
    fi
  fi
  scripts/changed_algorithms.sh > .verify_changed; make verify; rm -f .verify_changed
fi                                   # never publish unverified code
[ -d .git ] || { git init -q -b main; }
git add -A
git -c user.name="${GIT_NAME:-Yobie Benjamin}" -c user.email="${GIT_EMAIL:-YobieBenjamin@users.noreply.github.com}" \
    commit -qm "${1:-Mining run $(date -u +%F)}" || echo "nothing new to commit"
sync() {  # merge whatever is already on GitHub (e.g. LICENSE, browser uploads) before pushing
  git fetch -q "$1" main 2>/dev/null && git -c user.name=x -c user.email=x@x merge -q --no-edit \
      --allow-unrelated-histories -X ours FETCH_HEAD || true
}
if command -v gh >/dev/null; then
  gh repo view "$OWNER/$REPO" >/dev/null 2>&1 || gh repo create "$OWNER/$REPO" --private --source=. --remote=origin
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
  sync origin; git push -u origin main
elif [ -n "${GITHUB_TOKEN:-}" ]; then
  curl -sf -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user/repos \
       -d "{\"name\":\"$REPO\",\"private\":true}" >/dev/null || true
  sync "https://$GITHUB_TOKEN@github.com/$OWNER/$REPO.git"; git push "https://$GITHUB_TOKEN@github.com/$OWNER/$REPO.git" main
else
  echo "Authenticate first: 'gh auth login' or export GITHUB_TOKEN"; exit 1
fi
echo "Published: https://github.com/$OWNER/$REPO"
