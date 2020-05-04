@echo off
REM butler push ../crops-in-space$1
REM butler push ../ludum-dare-41-0.0.1-dists/ludum-dare-41-0.0.1-pc.zip joshua-mclean/ludum-dare-41:win-linux

SET /p VERSION=<game\version.txt
SET DIR=../crops-in-space-%VERSION%-dists
SET PREFIX=%DIR%/crops-in-space-%VERSION%-
SET PC=%PREFIX%pc.zip
SET MAC=%PREFIX%mac.zip
SET GAME=joshua-mclean/crops-in-space

SET PC_CMD=butler push %PC% %GAME%:win-linux-dev --userversion %VERSION%
SET MAC_CMD=butler push %MAC% %GAME%:mac-dev --userversion %VERSION%

echo PC build: %PC_CMD%
echo MAC build: %MAC_CMD%

SET /P EXECUTE=Execute command (Y/[N])?
IF /I "%EXECUTE%" NEQ "Y" GOTO END

%PC_CMD%
%MAC_CMD%

:END
