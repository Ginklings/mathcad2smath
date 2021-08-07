@echo off
if exist dist\*.* del dist\*.* /q
if exist src\*egg-info\*.* del src\*egg-info\*.* /q
if exist src\*egg-info rmdir src\*egg-info /q
if exist src\mathcad2smath\__pycache__\*.* del src\mathcad2smath\__pycache__\*.* /q
if exist src\mathcad2smath\__pycache__ rmdir src\mathcad2smath\__pycache__ /q
python -m build

if "%1"=="test_upload" python -m twine upload --repository testpypi dist/*
if "%1"=="upload" python -m twine upload dist/*

if "%1"=="test_upload" python -m pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps mathcad2smath
if "%1"=="upload" python -m pip install --upgrade mathcad2smath
