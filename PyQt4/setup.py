import sys
from cx_Freeze import setup, Executable

setup( name="Demo",
    version="1.0",
    description = "실행 파일로 배포",
    author="jay",
    executables = [Executable("hufsgrade_temp.py", base="Win32GUI")])
