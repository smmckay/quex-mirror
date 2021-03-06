#! /usr/bin/env bash
tmpfile=$(mktemp --suffix $(basename $1))

make "$@" >& $tmpfile

cat $tmpfile \
    | awk '/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || (/[Ee][Rr][Rr][Oo][Rr]/ && ! /--error/)'        \
    | awk '    ! /out of range/              \
            && ! /getline/                   \
            && ! /-Werror/                   \
            && ! /gcc/                       \
            && ! /g\+\+/                     \
            && ! /ASSERTS/                   \
            && ! /deprecated since quex/     \
            && ! /QUEX_ERROR_EXIT/           \
            && ! /QUEX_ERROR_DEPRECATED/'   

# echo "BEGIN: CAT TEMPFILE DURING MAKE PROCESS __________________"
# cat $tmpfile
# echo "END: _____________________________________________________"
rm $tmpfile
