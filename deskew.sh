ls -1 img*.png > files
sed s/img[0-9]*[AB]/\&.png\ -o\ 1\&/ files > files2
# seems that deskew is directly executable now
# sed s~img~/opt/deskew/bin/deskew\ img~ files2 > files
# not sure what is the meaning of ~ below, if there's an extra '/'
sed s~img~/deskew\ img~ files2 > files
echo beep >> files
# ./files
