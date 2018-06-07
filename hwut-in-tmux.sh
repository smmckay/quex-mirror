quex_path=$PWD
dir_list='
demo
quex/TESTS
quex/engine
quex/output
quex/input
quex/code_base/extra
quex/code_base/buffer/lexatoms
quex/code_base/buffer/bytes
quex/code_base/buffer/TESTS/load/ 
quex/code_base/buffer/TESTS/misc/ 
quex/code_base/buffer/TESTS/move/ 
quex/code_base/buffer/TESTS/navigation/
quex/code_base/analyzer/TEST
quex/code_base/TESTS
quex/code_base/lexeme_converter'

bash development-setup.sh
hwut make clean
hwut make -j 16

tmux new -s work -d
tmux rename-window -t TEST server
tmux send-keys -t TEST "hwut" C-m

for dir_name in $dir_list; do
    tmux new-window -n $dir_name
    tmux send-keys -t $dir_name "export QUEX_PATH=$QUEX_PATH; cd $QUEX_PATH/$dir_name; hwut make-clean; hwut" C-m
done

# tmux select-window -t work:1
tmux attach -t work
