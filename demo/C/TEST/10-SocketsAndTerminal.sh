#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "10-SocketsAndTerminal: Lexers on pipes, sockets, and the command line.;\n" \
    "CHOICES:  stdin, stdin-utf8, socket, socket-utf8, command-line, command-line-utf8;\n"
    
choice=$1

cd ../10-SocketsAndTerminal

function make_silent() {
    $QUEX_PATH/TEST/call-make.sh $1 $2 >& /dev/null
}

function observe() {
    $QUEX_PATH/TEST/valgrindi.sh tmp.txt ./$1  | grep -v '^\#\#'
}

if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
    make_silent clean
fi

case $1 in 
    command-line)
        make_silent lexer-command-line 
        printf "A message\nof a kilobyte\nstarts with a bit.\n" \
               | observe ./lexer-command-line
    ;;
    command-line-utf8)
        make_silent lexer-command-line-utf8
        printf "Сообщение о\nкилобайт начинается\nс одного бита.\nΈνα μήνυμα\nενός kilobyte\nξεκινά με ένα μόνο bit.\n" \
               | observe ./lexer-command-line-utf8
    ;;
    stdin)
        make_silent lexer-stdin 
        cat example-feed.txt | observe ./lexer-stdin 
    ;;
    stdin-utf8)
        make_silent lexer-stdin-utf8 
        cat example-feed-utf8.txt | observe ./lexer-stdin-utf8
    ;;
    socket)
        while ps axg | grep -v grep | grep lexer-socket > /dev/null; do sleep 1; done
        make_silent lexer-socket feed-socket 
        # If there is a 'lexer-socket' application running already => stop it.
        observe ./lexer-socket &
        sleep 3
        ./feed-socket file   example-feed.txt 5 1  >& tmp-feed.txt
        ./feed-socket string bye              1 10 >> tmp-feed.txt 2>&1
        cat tmp-feed.txt
        rm -f tmp-feed.txt
        while ps axg | grep -v grep | grep lexer-socket > /dev/null; do sleep 1; done
    ;;
    socket-utf8)
        while ps axg | grep -v grep | grep lexer-socket > /dev/null; do sleep 1; done
        make_silent lexer-socket-utf8 feed-socket 
        # If there is a 'lexer-socket' application running already => stop it.
        observe ./lexer-socket-utf8 &
        sleep 3
        ./feed-socket file   example-feed-utf8.txt 5 1  >& tmp-feed.txt
        ./feed-socket string bye                   1 10 >> tmp-feed.txt 2>&1
        cat tmp-feed.txt
        rm -f tmp-feed.txt
        while ps axg | grep -v grep | grep lexer-socket > /dev/null; do sleep 1; done
    ;;
esac

cat tmp.txt | grep -v '^\#\#'

if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
    make_silent clean 
fi
