CC = cl.exe
TARGET = core/core.dll
SRC = core/run.cpp
WIN_SDK = C:\Program Files (x86)\Windows Kits\10\Lib\10.0.20348.0\ucrt\x64
UCRT = C:\Program Files (x86)\Windows Kits\10\Include\10.0.20348.0\ucrt

all: $(TARGET) package

$(TARGET): $(SRC)
	@if not exist bin mkdir bin
	cl /EHsc /LD $(SRC) /Fe:$(TARGET) /I"$(UCRT)" /link /LIBPATH:"$(WIN_SDK)"

package: $(TARGET)
	@if not exist dist mkdir dist
	pyinstaller --onefile main.py --name mars-oi

clean:
	@if exist dist rmdir /S /Q dist
	@if exist build rmdir /S /Q build
	@if exist core\*.dll del core\*.dll
	@if exist core\*.exp del core\*.exp
	@if exist core\*.lib del core\*.lib
	@if exist *.spec del *.spec
	@if exist *.obj del *.obj
