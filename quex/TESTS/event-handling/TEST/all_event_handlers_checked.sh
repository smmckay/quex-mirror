# Extract the names of all event handlers available in Quex.
handlers=$(cat /home/fschaef/prj/quex/trunk/quex/blackboard.py \
           | awk 'BEGIN { show_f=0; } /standard_incidence_db *=/ { show_f = 1; } /^}/ { if( show_f ) show_f=0; } { if( show_f ) print; }' \
           | grep E_IncidenceIDs \
           | awk '{ a = $1; gsub(":", "", a); gsub("\"", "", a); print a; }')

qx_files=$(make hwut-info | sed -e 's/\.exe/.qx/g')

for name in $handlers; do
    cat $qx_files | awk "BEGIN{ verdict=\"[MISSING]\"; } /$name/ { verdict=\"[OK]     \"; } END{ print(verdict, \"$name\"); }"
done
