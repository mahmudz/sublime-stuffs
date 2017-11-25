:: Assumptions:
:: - Sublime Text has set the working directory and both the source and executable files
::   are in that directory
:: - The script is only capable of handling simple C# apps that do not reference 3rd-party
::   libraries

:: Inputs from Sublime Text
:: %1 - The full path and filename of the source file to build
:: %2 - The name of the executable file
@SET SRC_FILE="%1"
@SET EXE_NAME="%2"

:: Set up build environment. Change this as necessary depending on the version
:: of Visual Studio you wish to use.
@CALL "vsvars32.bat"

cl /O2 /GL /W3  /TP /EHsc %SRC_FILE%
@IF errorlevel 1 GOTO end
del *.obj
:: Execute compiled binary if build was successful.
@ECHO.
@ECHO Executing %EXE_NAME%:
@ECHO.
@%EXE_NAME%

::end