

cd "$(dirname "$0")"

echo "Compiling Java Employee Scheduler..."
echo ""

mkdir -p bin

javac -d bin -sourcepath src src/Main.java src/scheduler/*.java src/runner/*.java src/util/*.java

if [ $? -eq 0 ]; then
    echo "✓ Compilation successful!"
    echo ""
    echo "Run with: ./run.sh [mode]"
    echo "Or: cd bin && java Main [mode]"
else
    echo "✗ Compilation failed!"
    exit 1
fi
