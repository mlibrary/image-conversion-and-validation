#!/usr/bin/env bash
PROG="$0"
USAGE="[-h]"
BASE="$(dirname "$0")"

# Colorful logging.
echogood() { echo "[1;32m *[0m $@"; }
echowarn() { echo "[1;33m *[0m $@"; }
echobad()  { echo "[1;31m *[0m $@"; }

# Echo an optional error message, then show expected usage and
# exit an error status code.
errorout() {
  echo "usage: ${PROG} $USAGE" >&2
  [ -n "$1" ] && echo "${PROG}: error: $@" >&2
  exit 1
}

# Echo the expected usage along with a detailed help message.
printhelp() {
  cat <<EOF
usage: ${PROG} $USAGE

Run tests for this project.

optional arguments:
 -h           show this help message and exit
 -b BASE      base dir to run tests (default $BASE)
EOF
}

# Parse any arguments.
while getopts ":h" opt; do
  case "$opt" in
    h)
      # Just print the help message and exit happily.
      printhelp
      exit 0
      ;;

    b)
      BASE="$OPTARG"
      ;;

    ?)
      # Don't tolerate unrecognized options.
      errorout "unrecognized option: \`-$OPTARG'"
      ;;
  esac
done

# Shift so that the first "real" argument is $1.
shift $((OPTIND - 1))

run_tests() {
  python3 -m unittest
}

run_from_cwd() {
  echogood "Running tests (skipping any marked as slow) ..."
  if run_tests; then
    echogood "Running again, including slow tests ..."
    if SLOW_TESTS=1 run_tests; then
      echogood "Refactor or begin writing a new test."

    else
      echobad "Fix your slow test code!"
    fi

  else
    echobad "Fix your code!"
  fi
}

run_from_pushd() {
  if ! pushd "$1" > /dev/null; then
    errorout "couldn't cd into dir: \`$1'"
  fi

  run_from_cwd

  popd > /dev/null
}

if [ "$BASE" = . ]; then
  run_from_cwd

else
  run_from_pushd "$BASE"
fi