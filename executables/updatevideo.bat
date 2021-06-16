cd ..
cd website
cd leaderboard
copy /y names.txt "C:\Users\White Python\Desktop\Fran\Coding\ManimCE\leaderboard"
cd "C:\Users\White Python\Desktop\Fran\Coding\ManimCE\venv\Scripts"
call activate.bat
cd "C:\Users\White Python\Desktop\Fran\Coding\ManimCE\leaderboard"
call manim makevideo.py Render -qm -r 2400,800 --media_dir "C:\Users\White Python\Desktop\Fran\theconfluence\website\videos"
cd "C:\Users\White Python\Desktop\Fran\Coding\ManimCE\venv\Scripts"
call deactivate.bat
cd "C:\Users\White Python\Desktop\Fran\Coding\theconfluence\website\leaderboard"
pause