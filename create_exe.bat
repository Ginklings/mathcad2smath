pyinstaller --clean -y --onedir --name XMCD2SM --windowed --icon "C:\dev\mathcad2smath\src\mathcad2smath\app\icons\icon.ico" --add-data ".\src\mathcad2smath\app\app.ui;." --add-data ".\src\mathcad2smath\app\icons\*.*;.\icons" --add-data ".\src\mathcad2smath\app\icons\icon.ico;." .\src\mathcad2smath\app\app.py