CC = cl.exe
BIN = bin
TARGET = $(BIN)\core.dll
SRC = core\run.cpp
WIN_SDK = C:\Program Files (x86)\Windows Kits\10\Lib\10.0.20348.0\ucrt\x64
UCRT = C:\Program Files (x86)\Windows Kits\10\Include\10.0.20348.0\ucrt

all: $(TARGET) package 
	copy $(TARGET) dist\core.dll

$(TARGET): $(SRC)
	@if not exist bin mkdir bin
	cl /EHsc /LD $(SRC) /Fe:$(TARGET) /Fo:$(BIN) /I"$(UCRT)" /link /LIBPATH:"$(WIN_SDK)"

package:
	@if not exist dist mkdir dist
	pyinstaller --onefile main.py --name mars-oi

clean:
	@if exist dist rmdir /S /Q dist
	@if exist build rmdir /S /Q build
	@if exist $(BIN)\*.dll del $(BIN)\*.dll
	@if exist $(BIN)\*.exp del $(BIN)\*.exp
	@if exist $(BIN)\*.lib del $(BIN)\*.lib
	@if exist *.spec del *.spec
	@if exist *.obj del *.obj
