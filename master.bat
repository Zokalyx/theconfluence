echo off
cd executables
call retrieverun.bat
call createbasic.bat
call updatelast.bat
call updatewebsite.bat
call gitpush.bat
cd ..