#!/bin/bash
# run_all.sh - Test all function implementations in render/
# Usage: ./run_all.sh [subject_name]
#   Without argument: tests all subjects
#   With argument: tests only the specified subject (e.g. ft_strlen)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RENDER_DIR="$(cd "$SCRIPT_DIR/../../render" && pwd)"
TMP_DIR="/tmp/exam_testers"
mkdir -p "$TMP_DIR"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

passed=0
failed=0
skipped=0

run_test() {
    local subject="$1"
    local test_file="$SCRIPT_DIR/${subject}_test.c"
    local binary="$TMP_DIR/${subject}_tester"

    # Find implementation file(s) in render/
    local impl_files=()
    if [ -f "$RENDER_DIR/${subject}.c" ]; then
        impl_files+=("$RENDER_DIR/${subject}.c")
    fi

    # Special cases for subjects with different filenames
    if [ "$subject" = "is_power_of_2" ] && [ -f "$RENDER_DIR/is_power_of_2.c" ]; then
        impl_files=("$RENDER_DIR/is_power_of_2.c")
    fi

    if [ ${#impl_files[@]} -eq 0 ]; then
        echo -e "  ${RED}SKIP${NC} [$subject]: render/${subject}.c not found"
        ((skipped++))
        return
    fi

    # Compile (include both render/ and .tester/ for exam-provided headers)
    local compile_out
    compile_out=$(cc -Wall -Wextra -Werror "-I$RENDER_DIR" "-I$SCRIPT_DIR" \
        "${impl_files[@]}" "$test_file" -o "$binary" 2>&1)
    if [ $? -ne 0 ]; then
        echo -e "  ${RED}COMPILE ERROR${NC} [$subject]:"
        echo "$compile_out" | sed 's/^/    /'
        ((failed++))
        return
    fi

    # Run
    local output
    output=$("$binary" 2>&1)
    local exit_code=$?

    if [ $exit_code -eq 0 ] && echo "$output" | grep -q "ALL TESTS PASSED"; then
        echo -e "  ${GREEN}PASS${NC} [$subject]"
        ((passed++))
    else
        echo -e "  ${RED}FAIL${NC} [$subject]:"
        echo "$output" | sed 's/^/    /'
        ((failed++))
    fi

    rm -f "$binary"
}

echo "=== Exam02 Function Tester ==="
echo "Render dir: $RENDER_DIR"
echo ""

if [ -n "$1" ]; then
    # Test specific subject
    if [ -f "$SCRIPT_DIR/${1}_test.c" ]; then
        run_test "$1"
    else
        echo "No test found for: $1"
        exit 1
    fi
else
    # Test all subjects
    for test_file in "$SCRIPT_DIR"/*_test.c; do
        subject=$(basename "$test_file" _test.c)
        run_test "$subject"
    done
fi

echo ""
echo "=== Results ==="
echo -e "  ${GREEN}Passed : $passed${NC}"
echo -e "  ${RED}Failed : $failed${NC}"
echo "  Skipped: $skipped"
echo ""

[ "$failed" -eq 0 ]
