#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from cx_Freeze import setup, Executable

build_exe_options = {"packages": [],
                     "include_files":["basetinta.dat", "Interfaz.glade"]}
setup(
 name="Gestor Impresoras",
 version="0.4 Reloaded",
 description="Programa de gestion de tintas",
 executables = [Executable("Interfaz.py", base="Win32GUI")],
 options = {"build_exe": build_exe_options}

 )