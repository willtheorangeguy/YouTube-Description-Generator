@echo off
setlocal enabledelayedexpansion

for /d %%F in (*) do (
    if exist "%%F\description.txt" (
        set "folder=%%F"
        set "newname=%%F.txt"
        set "count=1"

        :check_exists
        if exist "!newname!" (
            set "newname=%%F_!count!.txt"
            set /a count+=1
            goto check_exists
        )

        move "%%F\description.txt" "!newname!"
        echo Moved and renamed: %%F\description.txt → !newname!
    )
)

echo Done.
pause