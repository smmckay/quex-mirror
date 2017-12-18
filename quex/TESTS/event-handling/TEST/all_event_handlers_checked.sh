
if [[ $1 == "--hwut-info" ]]; then
    echo "Check whether all event handlers from 'blackboard.py' are tested.;"
    exit
fi
# Extract the names of all event handlers available in Quex.
handlers=$(cat /home/fschaef/prj/quex/trunk/quex/blackboard.py \
           | awk 'BEGIN { show_f=0; } /standard_incidence_db *=/ { show_f = 1; } /^}/ { if( show_f ) show_f=0; } { if( show_f ) print; }' \
           | grep E_IncidenceIDs \
           | awk '{ a = $1; gsub(":", "", a); gsub("\"", "", a); print a; }' \
           | sort)

qx_files=$(ls *.qx)

for name in $handlers; do
    cat $qx_files | awk "BEGIN{ verdict=\"[MISSING]\"; } /$name/ { verdict=\"[OK]     \"; } END{ print(verdict, \"$name\"); }"
done
