#!/usr/bin/env python3

import textwrap
import sys
from p1libs.p1 import e2e
from collections import namedtuple

import gi 
gi.require_version('Atspi','2.0')
from gi.repository import Atspi

"""
Dado que la aplicacion se esta ejecutando
cuando el usuario seleciona un intervalo 3M asc
entonces...
"""


#Test Funs

def show(text):
	print(textwrap.dedent(text))

def show_passed():
	print('\033[92m'," PASSED ",'\033[0m')		

def show_not_passed(e):
	print('\033[91m'," NOT PASSED ",'\033[0m')	
	print(textwrap.indent(str(e), " "))

######

def given_he_lanzado_la_aplicacion(ctx):
        process,app = e2e.run(ctx.path)
        assert app is not None
        return Ctx(path= ctx.path,process=process,app=app)

def when_generic(ctx,rol,name,action):
        gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == rol and node.get_name() == name)
        boton = next(gen,None)
        assert boton is not None
        e2e.do_action(boton,action)
        return ctx

def then_table_cell(ctx,name):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == "table cell" and node.get_name().startswith(name))
	text = next(gen,None)
	assert text and text.get_text(0,-1).startswith(name)
	return ctx
	

def then_label(ctx,name,expected):
        gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and node.get_text(0,-1).startswith(name))
        label = next(gen,None)
        print(label.get_text(0,-1))
        assert label and label.get_text(0,-1) == expected
        return ctx

	
def testDistanceIntervale(ctx,intervalo,expected):
	msg = "GIVEN he lanzado la aplicación\nWHEN selecciono el intervalo "+str(intervalo)+"\nTHEN la distancia es de "+str(expected)
	show(msg)
	try:
		ctx = given_he_lanzado_la_aplicacion(ctx)
		ctx = when_generic(ctx,"combo box","2M","press")
		ctx = when_generic(ctx,"menu item",intervalo,"click")
		ctx = then_label(ctx, "DISTANCIA","DISTANCIA: "+str(expected))
		show_passed()
	except Exception as e: 
		show_not_passed(e)
	finally:
		e2e.stop(ctx.process)

	
def testNoteIntervale(ctx,intervalo,orden,expected):
	msg = "GIVEN he lanzado la aplicación\nWHEN selecciono el intervalo "+str(intervalo) +"\nTHEN muestra  "+str(expected)
	show(msg)
	try:
		ctx = given_he_lanzado_la_aplicacion(ctx)
		ctx = when_generic(ctx,"combo box","2M","press")
		ctx = when_generic(ctx,"menu item",intervalo,"click")
		ctx = when_generic(ctx,"combo box","asc","press")
		ctx = when_generic(ctx,"menu item",orden,"click")
		ctx = then_label(ctx, "NOTAS","NOTAS:  "+str(expected))
		show_passed()
	except Exception as e: 
		show_not_passed(e)
	finally:
		e2e.stop(ctx.process)
	
def testSongfromIntervalList(ctx,interval,orden,cancion):
	msg = "GIVEN he lanzado la aplicación "+"\nWHEN selecciono el intervalo "+str(interval)+" "+str(orden)
	msg += "\nTHEN aparace la cancion "+str(cancion)
	show(msg)
	try:
		ctx = given_he_lanzado_la_aplicacion(ctx)
		ctx = when_generic(ctx,"combo box","2M","press")
		ctx = when_generic(ctx,"menu item",interval,"click")
		ctx = when_generic(ctx,"combo box","asc","press")
		ctx = when_generic(ctx,"menu item",orden,"click")
		ctx = then_table_cell(ctx,cancion)
		show_passed()
	except Exception as e: 
		show_not_passed(e)
	finally:
		e2e.stop(ctx.process)
	
if __name__ == '__main__':
		Ctx = namedtuple("Ctx","path process app")
		ex_path = sys.argv[1]
		initial_ctx = Ctx(path= ex_path, process=None,app=None) #Contexto pruebas
		ctx = initial_ctx
		testDistanceIntervale(ctx,"3M","2T")
		testDistanceIntervale(ctx,"2m","1ST")
		testNoteIntervale(ctx,"3M","asc","DO MI SOL♯/LA♭")
		testNoteIntervale(ctx,"4j","asc","DO FA LA♯/SI♭")
		testSongfromIntervalList(ctx,"3M","asc","Blue Danube")
		testSongfromIntervalList(ctx,"7m","des","Watermelon")
		
