@ECHO OFF
ECHO Updating pip...
py -m pip install -U -q pip
ECHO Verifying twine installation...
py -m pip install -U -q twine
ECHO Verifying PyPA build installation...
py -m pip install -U -q build
ECHO Removing old dist/ folder...
rmdir /s /q dist
ECHO Creating source distribution...
py -m build
ECHO Executing upload...
twine upload dist/*
PAUSE
