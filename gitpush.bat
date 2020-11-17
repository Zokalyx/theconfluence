git add .
set /p id="Commit message: "
git commit -m %id%
git push
pause