tmpfile=$(mktemp --suffix $(basename $1))

make "$@" ASSERTS_ENABLED_F=YES -j 8 >& $tmpfile

cat $tmpfile \
    | awk '   /[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ \
           || /[Ee][Rr][Rr][Oo][Rr]/'        \
    | awk '    ! /out of range/              \
            && ! /getline/                   \
            && ! /-Werror/                   \
            && ! /gcc/                       \
            && ! /g\+\+/                     \
            && ! /ASSERTS/                   \
            && ! /deprecated since quex/     \
            && ! /QUEX_ERROR_EXIT/           \
            && ! /QUEX_ERROR_DEPRECATED/'   

rm $tmpfile
