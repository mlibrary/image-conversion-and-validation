#!/usr/bin/env bash
PROG="$0"
USAGE="[-hv] [-b BASE] [-1 | -2]"
VERBOSE=false
BASE="$(dirname "$(dirname "$0")")"
RUN_TWICE=false

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
  local once="run all tests once"
  local twice="run only fast tests first"
  $RUN_TWICE && local twice="$twice (default)" \
             || local once="$once (default)"

  cat <<EOF
usage: ${PROG} $USAGE

Run tests for this project.

optional arguments:
 -h           show this help message and exit
 -v           verbose logging
 -b BASE      base dir to run tests (default $BASE)
 -1           $once
 -2           $twice
EOF
}

# Parse any arguments.
while getopts ":hvb:12" opt; do
  case "$opt" in
    h)
      # Just print the help message and exit happily.
      printhelp
      exit 0
      ;;

    v)
      VERBOSE=true
      ;;

    b)
      BASE="$OPTARG"
      ;;

    1)
      RUN_TWICE=false
      ;;

    2)
      RUN_TWICE=true
      ;;

    ?)
      # Don't tolerate unrecognized options.
      errorout "unrecognized option: \`-$OPTARG'"
      ;;
  esac
done

# Shift so that the first "real" argument is $1.
shift $((OPTIND - 1))

if $VERBOSE; then
  V_FLAG="-v"

else
  V_FLAG=""
fi

run_tests() {
  python3 -m unittest $V_FLAG
}

echo_green() {
  echo -n "[1;37;42m                 [1;37;44mRefactor[1;37;42m"
  echo " or begin writing a new test.                  [0m"
}

echo_red_normal() {
  echo -n "[1;37;41m                             Fix your code!"
  echo "                             [0m"
}

echo_red_slow() {
  echo -n "[1;37;41m                        Fix your "
  echo -n "[1;36;41mslow-test[1;37;41m code!"
  echo "                        [0m"
}

run_slow_tests() {
  if SLOW_TESTS=1 run_tests; then
    echo_green

  else
    echo_red_slow
  fi
}

run_fast_tests_first() {
  echogood "Running tests (skipping any marked as slow) ..."
  if run_tests; then
    echogood "Running again, including slow tests ..."
    run_slow_tests

  else
    echo_red_normal
  fi
}

run_from_cwd() {
  if $RUN_TWICE; then
    run_fast_tests_first

  else
    echogood "Running all tests ..."
    run_slow_tests
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