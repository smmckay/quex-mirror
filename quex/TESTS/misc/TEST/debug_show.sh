#! /usr/bin/env bash
case $1 in
    --hwut-info)
        echo "FSM DFA_State Tracer;"
        echo "HAPPY: [0-9]+;"
        ;;

    *)
             # --path-compression-uniform \
        quex --cbm -i debug_show.qx -o Simple \
             --path-compression \
             --template-compression \
             --template-compression-min-gain 0 -\
             --language C --debug-exception 
        gcc -I$QUEX_PATH Simple/Simple.c $q/TEST/lexer.c -I. \
            -DQUEX_OPTION_DEBUG_SHOW_EXT -DQUEX_SETTING_BUFFER_SIZE_EXT=15 -o debug_show -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=0
        ./debug_show data/debug_show.txt 2>&1 \
            | sed -e 's/:[0-9]\+:/:LineNumber:/g' > tmp.txt
        # cat tmp.txt | awk '! (/state_key/ || /template/ || /path/) { print $0; }'
        echo "____________________________________________________________________"
        echo "Extracted (path_walker, state_index, template, etc.)"
        echo "This only proves that there were MegaStates involved."
        echo
        cat tmp.txt | grep -ae 'state_key\|template\|path walker\|path_iterator\|number of token' | sort -u
        rm -rf ./debug_show Simple* tmp.txt
        ;;
esac

