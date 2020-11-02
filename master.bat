cd csv
call generateallcsv.bat
cd ..
cd graphs
call runall.bat
cd..
cd website
call python -m scriptupdater
pause