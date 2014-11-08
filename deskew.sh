ls -1 img*.png > files
sed s/img[0-9]*[AB]/\&.png\ -o\ 1\&/ files > files2
sed s~img~/opt/deskew/bin/deskew\ img~ files2 > files
echo beep >> files
# ./files
