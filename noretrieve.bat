echo off
cd executables
call createbasic.bat
call updatelast.bat
call updatewebsite.bat
call gitpush.bat
cd ..