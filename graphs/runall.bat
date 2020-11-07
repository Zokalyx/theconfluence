cd leaderboard
python -m htmlcreator
call rendervideo.bat
cd ..\retention
python -m creategraph
cd ..\population
python -m creategraph
cd ..
pause