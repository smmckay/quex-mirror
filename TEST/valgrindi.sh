# PURPOSE: Calling an application with 'valgrind' to check on memory
#          leaks and other failures.
#
# $1:        output file name
# $2:        application name
# Remainder: remaining arguments to be passed to application
#
# RESULT:  Filtererd valgrind output file stored in '$1'.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
output_file=$1
shift

raw_log_file=$(mktemp --suffix=$(basename $1))
valgrind --log-file=$raw_log_file \
         --leak-check=full \
         --show-leak-kinds=all \
         "$@" 

# -- filter experiment results
python $QUEX_PATH/TEST/show-valgrind.py $raw_log_file > $output_file
rm $raw_log_file
