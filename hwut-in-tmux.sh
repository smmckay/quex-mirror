quex_path=$PWD
dir_list='
TEST
demo
quex/engine
quex/output
quex/input
quex/code_base/extra
quex/code_base/buffer/lexatoms
quex/code_base/buffer/bytes
quex/code_base/buffer/TESTS
quex/code_base/analyzer/TEST
quex/code_base/TEST
quex/code_base/lexeme_converter'

tmux new-s -t ut
for dir_name in $dir_list; do
    tmux new-w -t ut -n $(basename $dir_name)
    tmux send-keys "export QUEX_PATH=$QUEX_PATH; cd $QUEX_PATH/$dir_name; hwut make-clean; hwut" C-m
done

