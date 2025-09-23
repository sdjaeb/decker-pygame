# Source this file in your interactive shell to get a `preflight` function.
# Example: source scripts/preflight.zsh

preflight() {
  # Prefer the shell script for execution but provide convenience here.
  local script_path
  script_path="${PWD}/scripts/preflight.sh"
  if [ -x "${script_path}" ]; then
    "${script_path}"
  else
    bash "${script_path}"
  fi
}

export -f preflight
# Source this file from your ~/.zshrc to get a `preflight` function in your shell
# Example: source scripts/preflight.zsh

preflight() {
  # Call the repo-local preflight script so behavior is consistent across the team
  "$(cd "$(dirname "${(%):-%x}")/.." && pwd)/scripts/preflight.sh" "$@"
}
