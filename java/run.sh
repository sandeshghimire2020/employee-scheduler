

cd "$(dirname "$0")"

if [ ! -d "bin" ] || [ ! -f "bin/Main.class" ]; then
    echo "Not compiled yet. Compiling..."
    ./compile.sh
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

cd bin
java Main "$@"
