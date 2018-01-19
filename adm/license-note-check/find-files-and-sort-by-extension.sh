grep -L MIT . -r         \
      --exclude     "*.sw?" \
      --exclude     "*.xcf" \
      --exclude     "*.7z" \
      --exclude     "*.zip" \
      --exclude     "*.tgz" \
      --exclude     "*.bz2" \
      --exclude     "*.dat" \
      --exclude     "*.eps" \
      --exclude     "*.exe" \
      --exclude     "*.exrc" \
      --exclude     "*.fig" \
      --exclude     "*.dia" \
      --exclude     "*.dot" \
      --exclude     "*.fly" \
      --exclude     "*.html" \
      --exclude     "*.jpg" \
      --exclude     "*.log" \
      --exclude     "*.out" \
      --exclude     "*.o" \
      --exclude     "*.pdf" \
      --exclude     "*.mm" \
      --exclude     "*.mk" \
      --exclude     "*.png" \
      --exclude     "*.pyc" \
      --exclude     "*-DELETED" \
      --exclude     "*.svg" \
      --exclude     "*.utf8" \
      --exclude     "*.utf16" \
      --exclude     "*.utf16?e" \
      --exclude     "*.utf16-?e" \
      --exclude     "*.utf32?e" \
      --exclude     "*.ucs4-?e" \
      --exclude-dir .svn \
      --exclude-dir OUT  \
      --exclude-dir GOOD > tmp0.txt


cat tmp0.txt | while read line; do file=${line:1}; root=${file%.*}; ext="${file#"$root"}"; echo "'$ext'" $line; done | sort
