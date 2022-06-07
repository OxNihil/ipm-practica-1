#!/usr/bin/env python3
# -*- coding: UTF-8

import json, locale, gettext
import urllib.request
import webbrowser
import threading
import gi
from pathlib import Path
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GLib

_ = gettext.gettext
N_ = gettext.ngettext

class View(Gtk.Window):
	@classmethod
	def main(cls):
		Gtk.main()
	
	@classmethod
	def main_quit(cls,w,e):
		Gtk.main_quit()
	
	def __init__(self):
		super(View,self).__init__()
		self.set_title(_("CheckTheTone - Practica P1 IPM"))
		self.set_default_size(580,400)
		self.set_border_width(0)
		self.set_resizable(False)
        #Widgets
		self.draw_zone = Gtk.DrawingArea()
		self.interval_label = Gtk.Label()
		self.note_label = Gtk.Label()
		self.distance_label = Gtk.Label()
		self.notas_piano = Gtk.Label()
		self.interval_combo = Gtk.ComboBox()
		self.ord_combo = Gtk.ComboBox()
		self.song_view = Gtk.TreeView()
		self.fav_view = Gtk.TreeView()
		self.url_view = Gtk.TreeView()
		self.button = Gtk.Button()
		self.spinner = Gtk.Spinner()
	def build_view(self):
		#Layaout vars
		grid = Gtk.Grid()
		mainbox = Gtk.HBox(spacing=8) #MAIN
		hbox = Gtk.HBox(spacing=8) #PIANO
		hbox2 = Gtk.HBox(spacing=6) #NOTAS
		cbox = Gtk.HBox(spacing=4) #container
		vbox = Gtk.VBox(spacing=2) #Label 
		listbox = Gtk.HBox(spacing=4) #listbox
		cell = Gtk.CellRendererText()
		cell.set_property("ellipsize",3)
		cell.set_property("ellipsize-set", True)
		cell.set_property("width-chars",25)
		#cordenadas ZonaDibujo
		px,py = 480,170
        #TreeViews
		song_col = Gtk.TreeViewColumn(_("Canciones"), cell, text=0)
		fav_col = Gtk.TreeViewColumn(_("Favoritos"), cell, text=0)
		url_col = Gtk.TreeViewColumn(_("Reproducir"), cell, text=0) 
		self.song_view.append_column(song_col)
		self.fav_view.append_column(fav_col)
		self.url_view.append_column(url_col)
        #Listas:
		listbox.add(self.song_view)
		listbox.add(self.fav_view)
		listbox.add(self.url_view)
		listbox.set_margin_top(4)	
        #COMBO
        #COMBOBOX1
		self.interval_combo.pack_start(cell, False)
		self.interval_combo.add_attribute(cell,"text",0)
		self.interval_combo.set_active(0)
		mainbox.add(self.interval_combo)      
        #COMBOBOX2
		self.ord_combo.pack_start(cell, False)
		self.ord_combo.add_attribute(cell,"text",0)
		self.ord_combo.set_active(0)
		mainbox.add(self.ord_combo)
		#Play buttom
		self.button.set_label("Reproducir")
		mainbox.add(self.button)
		#Labels
		self.interval_label.set_markup("<b>"+_("INTERVALO:")+" </b>")
		self.note_label.set_markup("<b>"+_("NOTAS:")+" </b>")
		self.distance_label.set_markup("<b>"+_("DISTANCIA:")+" </b>")
		self.interval_label.set_xalign(0.5)
		self.note_label.set_xalign(0.5)
		self.distance_label.set_xalign(0.5)
		vbox.add(self.interval_label)
		vbox.add(self.distance_label)
		vbox.add(self.note_label)
        #Piano
		self.draw_zone.set_size_request(px, py)
		hbox.add(self.draw_zone)
		hbox.set_margin_top(10)
		#Notas piano
		hbox2.add(self.notas_piano)
		#Container
		cbox.set_size_request(380,240) 
		cbox.add(listbox)
        #LAYOUT
		grid.attach(hbox,0,0,1,1)
		grid.attach_next_to(vbox, hbox, Gtk.PositionType.RIGHT, 1, 1)
		grid.attach_next_to(hbox2, hbox, Gtk.PositionType.BOTTOM, 1, 1)
		grid.attach_next_to(cbox,hbox, Gtk.PositionType.TOP, 100, 100)
		grid.attach_next_to(mainbox, cbox, Gtk.PositionType.TOP, 1, 1)
		self.add(grid)
	def update_view(self, **kwargs): 
		for name, value in kwargs.items():
			if name == "interval_label":
				self.interval_label.set_markup("<b>"+_("INTERVAL:")+"</b><small> "+value+"</small>")
			elif name == "distance_label":
				self.distance_label.set_markup("<b>"+_("DISTANCIA:")+"</b><small> "+value+"</small>")
			elif name == "notes_label":
				self.note_label.set_markup("<b>"+_("NOTAS:")+"</b><small> "+value+"</small>")
				self.note_label.set_line_wrap(True)
				self.note_label.set_max_width_chars(10)
			elif name == "song_list":
				self.spinner.stop()
				song_list = Gtk.ListStore(str)
				is_fav = Gtk.ListStore(str)
				youtube_url = Gtk.ListStore(str)
				if value is not None:
					for item in value['data']:
						if len(item) == 4:
							name_song = item[0]+" "+item[1]
							song_list.append([name_song])
							youtube_url.append([item[2]])
							is_fav.append([item[3]])
						else:
							song_list.append([(item[0])])
							youtube_url.append([item[1]])
							is_fav.append([item[2]])
						self.song_view.set_model(song_list)
						self.fav_view.set_model(is_fav)
						self.url_view.set_model(youtube_url)
			elif name == "combo_interval":
				interval_store = Gtk.ListStore(str)
				for i in value:
					interval_store.append([i])
				self.interval_combo.set_model(interval_store)
			elif name == "ord_combo":
				ord_store = Gtk.ListStore(str)
				for i in value:
					ord_store.append([i])
				self.ord_combo.set_model(ord_store)
			elif name == "piano_label":
				self.notas_piano.set_markup("<b><small>"+value+"</small></b>");
			else:
				raise TypeError(_(f"update_view() got an unexpected keyboard argument '{name}'"))
	def connect_delete_event(self,fun):
		self.connect("delete-event",self.main_quit)
	def connect_draw_piano(self,fun):
		self.draw_zone.connect("draw",fun)
	def connect_draw_interval(self,fun):
		self.draw_zone.connect("draw",fun)
	def connect_interval_change(self,fun): 
			self.interval_combo.connect("changed", fun)
	def connect_ord_change(self,fun):
			self.ord_combo.connect("changed",fun)
	def connect_button_clicked(self,fun):
			self.button.connect("clicked", fun)
	def error_dialog(self,text):
		dialog = Gtk.MessageDialog(parent=self,
                                   buttons=Gtk.ButtonsType.OK,title="Error",
                                   message_type=Gtk.MessageType.ERROR,text=text)
		dialog.set_default_size(150, 100)
		dialog.run()
		dialog.destroy()
    	
class Controller():
	def main(self):
		self.view.show_all()
		self.view.main()
	def set_model(self,model):
		self.model = model
	def set_view(self,view):
		self.view = view
		view.build_view()
		self.model.WebHandler.get_intervals_list(self)
		notacion = self.model.get_notacion()
		intervals = self.model.WebHandler.get_intervale_name() 
		ord_store = self.model.get_ord_list()
		notas_piano = self.model.note_list_piano()
		self._update_view(ord_combo=ord_store,
						  piano_label=notas_piano,
						  combo_interval=intervals)
		view.connect_button_clicked(self.on_play_button)
		view.connect_interval_change(self.on_interval_change)
		view.connect_ord_change(self.on_interval_change)
		view.connect_draw_piano(self.on_draw_piano)
		view.connect_delete_event(self.view.main_quit)
	def _update_view(self, **kwargs):
		self.view.update_view(**kwargs)
	def update_songs(self, lista):
		self.view.update_view(song_list=lista)
	def on_play_button(self,event):
		tree = self.view.url_view
		model = tree.get_model()
		path = tree.get_selection().get_selected()[1]
		if path is not None:
			url_ind = model.get_string_from_iter(path)
			url = model[url_ind][0]
			if url != "": webbrowser.open(url)
	def on_interval_change(self,event):
		self.view.connect_draw_interval(self.on_draw_interval)
		interval_model = self.view.interval_combo.get_model()
		#Check Conection
		if (not self.model.WebHandler.check_con()):
			self.view.error_dialog(_("No hay conexion"))
		if len(interval_model) > 0:
			interval = interval_model[self.view.interval_combo.get_active()][0]
			ord_model = self.view.ord_combo.get_model()
			orden = ord_model[self.view.ord_combo.get_active()][0]
			self.model.WebHandler.obtain_songs(interval,orden,self)
			notacion = self.model.get_notacion()
			dist_list = self.model.WebHandler.get_intervals()
			dist_intervale = self.model.calculate_distancia(dist_list[interval],orden)
			note_list = self.model.calculate_interval(dist_list[interval],orden)
			note_str = "" 
			for nota in note_list:
				note_str+=" "+notacion[nota]
			self._update_view(interval_label=interval,
							   distance_label=dist_list[interval],
							   notes_label=note_str)
	def on_draw_piano(self,event,ctx):
		x = 20
		y = 0
		for i in range(7):
			ctx.set_source_rgb(240,240,240)
			ctx.rectangle(x,y,60,160) #Teclas blancas
			ctx.fill()
			x+=65
		ctx.set_source_rgb(0,0,0)
		ctx.rectangle(60,y,40,100)
		ctx.rectangle(125,y,40,100)
		ctx.rectangle(255,y,40,100)
		ctx.rectangle(320,y,40,100)
		ctx.rectangle(385,y,40,100)
		ctx.fill()
	def on_draw_interval(self,event,widget):
		interval_model = self.view.interval_combo.get_model()
		if len(interval_model) > 0:
			interval = interval_model[self.view.interval_combo.get_active()][0]
			ord_model = self.view.ord_combo.get_model()
			orden = ord_model[self.view.ord_combo.get_active()][0]
		notacion = self.model.get_notacion()
		dist_intervale = self.model.WebHandler.get_intervals()
		if dist_intervale is not None:
			note_list = self.model.calculate_interval(dist_intervale[interval],orden) 
			x=20
			x2=60
			py = 170
			for i in range(len(notacion)):
				if i in note_list: #Si es la nota elegida
					widget.set_source_rgb(0.9, 0.1, 0.1)
					if self.model.get_es_sostenido(i):
						y = py-80
						widget.rectangle(x2,y,40,10)
					else:
						y = py-10
						widget.rectangle(x,y,60,10)
					widget.fill()
				if i % 2 == 0: #Pares,tecla abajo
					x+=65
				else:
					x2+=65
				
class Model():
	notacion =  [_("DO"),_("DO\u266f/RE\u266D"),_("RE"),_("RE\u266f/MI\u266D"),_("MI"),_("FA"),_("FA\u266f/SOL\u266D"),
	_("SOL"),_("SOL\u266f/LA\u266D"),_("LA"),_("LA\u266f/SI\u266D"),_("SI") ]
	WebHandler = None
	def __init__(self):
		self.WebHandler = WebHandler()
	def get_es_sostenido(self,i):
		if (len(self.get_notacion()[i]) > 4):
			return True
		else:
			return False
	def get_notacion(self):
		return self.notacion
	def get_ord_list(self):
		return ["asc","des"]
	def note_list_piano(self):
		msg = ""
		notacion = self.get_notacion()
		for i in range(len(notacion)):
			note = notacion[i]
			if  len(note.strip("/")) < 4:
				msg += "\t"+note.upper()+"\t\t"
		return msg
	def calculate_distancia(self,interval,orden):
		tones =[]
		distancia = 0
		if interval == "1ST":
			tones = [0,1]
		else:
			tones = [int(tono) for tono in interval if tono.isdigit() ]
		if len(tones) > 1:
			distancia = (tones[0]*2)+tones[1]
		else:
			distancia = tones[0]*2
		return distancia
	def calculate_interval(self,interval,orden):
		distancia = self.calculate_distancia(interval,orden)
		list_dist = []
		if orden == "asc":
			for i in range(11):
				if i % distancia == 0:
					list_dist.append(i%12)
		else:
			for i in range(11):
				ind = 11-i
				if ind % distancia == 0:
					list_dist.append(i%12)
		return list_dist
    
    	
class WebHandler():
    url = "http://127.0.0.1:5000"
    intervals = None
    def check_con(self):
    	try:
    		url = self.url+"/intervals"
    		urllib.request.urlopen(url, timeout=1)
    		return True
    	except:
    		return False
    def get_intervals_list(self,controller):
    	try:
    		url = self.url+"/intervals"
    		with urllib.request.urlopen(url) as response:
    			resp = response.read()
    		notes = json.loads(resp)
    		self.set_intervals(notes['data'])
    	except Exception as e:
    		print(e)
    def get_intervals(self):
    	return self.intervals
    def set_intervals(self,lista):
    	self.intervals = lista
    def get_intervale_name(self):
    	if self.intervals is not None:
    		return self.intervals.keys()
    def get_intervale_distance(self):
    	if self.intervals is not None:
    		return list(self.intervals.values())
    def obtain_songs(self,interval,orden,controller):
    	controller.view.spinner.start()
    	threading.Thread(target=self.get_songs,args=(interval,orden,controller),daemon=True).start()
    def get_songs(self,interval,orden,controller):
    	lista = None
    	url = self.url+"/songs/"+str(interval)+"/"+str(orden)
    	with urllib.request.urlopen(url) as response:
    		resp = response.read()
    	lista = json.loads(resp)
    	GLib.idle_add(controller.update_songs,lista) #update combo - nova


if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL,'')
	LOCALE_DIR = Path(__file__).parent / "locales"
	locale.bindtextdomain('checkthetone',LOCALE_DIR)
	gettext.bindtextdomain('checkthetone',LOCALE_DIR)
	gettext.textdomain('checkthetone')
	win = View()
	model = Model()
	control = Controller()
	control.set_model(model)
	control.set_view(win)
	control.main()
