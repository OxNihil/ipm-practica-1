import json, locale
import urllib.request
import webbrowser
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk


class ViewManager():
	ApiHandler = None
	song_view = None
	fav_view = None
	url_view = None
	interval_label = None 
	note_label = None
	distance_label = None
	def __init__(self):
		self.ApiHandler = ApiHandler()
		#Label
		self.interval_label = Gtk.Label(label="INTERVALO: ")
		self.note_label = Gtk.Label(label="NOTAS: ")
		self.distance_label = Gtk.Label(label="DISTANCIA: ")
		self.interval_label.set_xalign(0.5)
		self.note_label.set_xalign(0.5)
		self.distance_label.set_xalign(0.5)
		song_list, fav_list,url_list = self.get_songs_list_all("2m","asc") #Default value list
		#Lista
		
		cell = Gtk.CellRendererText()
		self.song_view = Gtk.TreeView(model=song_list)
		self.fav_view = Gtk.TreeView(model=fav_list)
		self.url_view = Gtk.TreeView(model=url_list)
		song_col = Gtk.TreeViewColumn("Canciones", cell, text=0)
		fav_col = Gtk.TreeViewColumn("Favoritos", cell, text=0)
		url_col = Gtk.TreeViewColumn("Reproducir", cell, text=0) 
		self.song_view.append_column(song_col)
		self.fav_view.append_column(fav_col)
		self.url_view.append_column(url_col)
	def get_ord_list(self):
		ord_store = Gtk.ListStore(str)
		for i in ["asc","des"]:
			ord_store.append([i])
		return ord_store
	def get_songs_list_all(self,inter,orden):
		song_list = Gtk.ListStore(str)
		is_fav = Gtk.ListStore(str)
		youtube_url = Gtk.ListStore(str)
		items = self.ApiHandler.WebHandler.get_songs(inter,orden)
		cut = self.ApiHandler.WebHandler.cut_text #Cambiar a esta clase
		if items is not None:
			for item in items['data']:
				if len(item) == 4:
					name_song = item[0]+item[1]
					song_list.append([cut(name_song)])
					youtube_url.append([item[2]])
					is_fav.append([item[3]])
				else:
					song_list.append([cut(item[0])])
					youtube_url.append([item[1]])
					is_fav.append([item[2]])
		return song_list, is_fav, youtube_url
	def get_interval_list(self):  
		interval_store = Gtk.ListStore(str)
		inter = self.ApiHandler.WebHandler.get_intervale_name()
		if inter is not None:
			for i in inter:
				interval_store.append([i])
		return interval_store
	def get_note_list(self,notacion):
		note_store = Gtk.ListStore(str)
		for i in notacion:
			note_store.append([i])
		return note_store
	def note_list_piano(self,notacion):
		msg = ""
		for i in range(len(notacion)):
			note = notacion[i]
			if  len(note.strip("/")) < 4:
				msg += "\t"+note.upper()+"\t\t"
		notes_label = Gtk.Label(label=(msg),halign=Gtk.Align.CENTER)
		notes_label.set_markup("<b><small>"+msg+"</small></b>");
		return notes_label
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

class MainWindows(Gtk.Window):
    #Para que sea mvc solo hay que hacer que todas las llamadas se ejecuten desede contorer
    #cambiar llamadas de lo de la lista, funcion update_list
    #Añadir col con boton de play
    def __init__(self):
        super(MainWindows,self).__init__()
        self.set_title("CheckTheTone - Practica P1 IPM")
        self.set_default_size(560,400)
        self.set_border_width(0)
        self.set_resizable(False)
       
        self.view = ViewManager()
        self.draw_zone = Gtk.DrawingArea()
        self.build_view()
    def build_view(self):
        grid = Gtk.Grid()
        mainbox = Gtk.HBox(spacing=8) #MAIN
        hbox = Gtk.HBox(spacing=8) #PIANO
        hbox2 = Gtk.HBox(spacing=8) #NOTAS
        cbox = Gtk.HBox(spacing=4) #container
        vbox = Gtk.VBox(spacing=0) #Label 
        listbox = Gtk.HBox(spacing=4) #listbox
        #Main
        notacion = self.view.ApiHandler.AppData.get_notacion()
        interval_store = self.view.get_interval_list()
        note_store =  self.view.get_note_list(notacion)
        ord_store = self.view.get_ord_list() 
        renderer_text = Gtk.CellRendererText()
        #cordenadas ZonaDibujo
        px,py = 480,170
        
        	
        #Listas:
        #self.view.url_view.connect("row-activated",self.play_song)
        listbox.add(self.view.song_view)
        listbox.add(self.view.fav_view)
        listbox.add(self.view.url_view)
        listbox.set_margin_top(4)	
        #COMBO
        interval_combo = Gtk.ComboBox(model=interval_store)
        ord_combo = Gtk.ComboBox(model=ord_store)
        #COMBOBOX1
        interval_combo.connect("changed", self.interval_change,ord_combo,py)
        interval_combo.pack_start(renderer_text, False)
        interval_combo.add_attribute(renderer_text,"text",0)
        interval_combo.set_active(0)
        mainbox.add(interval_combo)      
        #COMBOBOX2
        ord_combo.connect("changed", self.ord_change,interval_combo,ord_combo,py)
        ord_combo.pack_start(renderer_text, False)
        ord_combo.add_attribute(renderer_text,"text",0)
        ord_combo.set_active(0)
        mainbox.add(ord_combo)
        #Play buttom
        button = Gtk.Button.new_with_label("Play")
        button.connect("clicked", self.play_song)
        mainbox.add(button)
        #Labels
        
        vbox.add(self.view.interval_label)
        vbox.add(self.view.distance_label)
        vbox.add(self.view.note_label)
		#Piano
        self.draw_zone.connect("draw",self.draw_piano)
        self.draw_zone.set_size_request (px, py)
        hbox.add(self.draw_zone)
        hbox.set_margin_top(10)
                    
        #Notas piano
        notas = self.view.note_list_piano(notacion)
        hbox2.add(notas)
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
        #Check Conection
        if (not self.view.ApiHandler.WebHandler.check_con()):
        	self.error_dialog()
        
        self.connect('delete-event',Gtk.main_quit)
    def update_lists(self,interval,orden):
    	song_list, fav_list, url_list = self.view.get_songs_list_all(interval,orden) 
    	self.view.song_view.set_model(song_list)
    	self.view.fav_view.set_model(fav_list)
    	self.view.url_view.set_model(url_list)
    def update_label(self,interval,orden):
    	notacion = self.view.ApiHandler.AppData.get_notacion()
    	dist_intervale = self.view.ApiHandler.WebHandler.get_intervals()
    	intervale_list = self.view.ApiHandler.WebHandler.get_intervale_name()
    	notas = ""
    	if dist_intervale is not None:
	    	note_list = self.view.calculate_interval(dist_intervale[interval],orden)
	    	for i in note_list:
	    		notas += notacion[i]+str(" ")
	    	acc = 0
	    	for i in (intervale_list):
	    		if i == interval:
	    			self.view.distance_label.set_markup("<b>DISTANCIA:</b> <small> "+dist_intervale[i]+"</small>")
	    		acc+=1
	    	self.view.interval_label.set_markup("<b>INTERVAL:</b> <small> "+interval+" "+orden+"</small>")
	    	self.view.note_label.set_markup("<b>NOTAS:</b>"+"<small>"+notas+"</small>")
	    	self.view.note_label.set_line_wrap(True)
	    	self.view.note_label.set_max_width_chars(10)
    def draw_clear(self,event,widget,py):
    	y = 0
    	x = 20
    	x2 = 60
    	for i in range(12):
    		if self.view.ApiHandler.AppData.get_es_sostenido(i):
    			widget.set_source_rgb(0,0,0)
    			y = py-80
	    		widget.rectangle(x2,y,40,10)
	    	else:
	    		widget.set_source_rgb(240,240,240)
	    		y = py-10
	    		widget.rectangle(x,y,60,10)
	    	widget.fill()
    		if i % 2 == 0: #Pares,tecla abajo
	    		x+=65
	    	else:
	    		x2+=65
    def draw_piano(self,event,ctx):
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
    def draw_interval(self,event,widget,interval,orden,py): 
    	notacion = self.view.ApiHandler.AppData.get_notacion()
    	dist_intervale = self.view.ApiHandler.WebHandler.get_intervals()
    	if dist_intervale is not None:
	    	note_list = self.view.calculate_interval(dist_intervale[interval],orden)
	    	x=20
	    	x2=60
	    	for i in range(len(notacion)):
	    		if i in note_list: #Si es la nota elegida
	    			widget.set_source_rgb(0.9, 0.1, 0.1)
	    			if self.view.ApiHandler.AppData.get_es_sostenido(i):
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
    #CALLBACK
    def interval_change(self,interval_combo,ord_combo,py):
    	interval_model = interval_combo.get_model()
    	if len(interval_model) > 0:
	    	interval = interval_model[interval_combo.get_active()][0]
	    	ord_model = ord_combo.get_model()
	    	orden = ord_model[ord_combo.get_active()][0]
	    	self.update_label(interval,orden)
	    	self.update_lists(interval,orden) #obtenemos list_store
	    	self.draw_zone.connect("draw",self.draw_clear,py)
	    	self.draw_zone.connect("draw",self.draw_interval,interval,orden,py)
    def error_dialog(self):
    	dialog = Gtk.MessageDialog(parent=self,
                                   buttons=Gtk.ButtonsType.OK,title="Error",
                                   message_type=Gtk.MessageType.ERROR,text="No hay conexion con el servidor")
    	dialog.set_default_size(150, 100)
    	response = dialog.run()
    	dialog.destroy()
    def ord_change(self,event,interval_combo,ord_combo,py):
    	interval_model = interval_combo.get_model()
    	if len(interval_model) > 0:
	    	interval = interval_model[interval_combo.get_active()][0]
	    	ord_model = ord_combo.get_model()
	    	orden = ord_model[ord_combo.get_active()][0]
	    	self.update_label(interval,orden)
	    	self.update_lists(interval,orden) #obtenemos list_store
	    	self.draw_zone.connect("draw",self.draw_clear,py)
	    	self.draw_zone.connect("draw",self.draw_interval,interval,orden,py)
    def play_song(self,event):
    	tree = self.view.url_view
    	model = tree.get_model()
    	path = tree.get_selection().get_selected()[1]
    	if path is not None:
    		url_ind = model.get_string_from_iter(path)
    		url = model[url_ind][0]
    		if url != "": webbrowser.open(url)
    	



class AppData(Gtk.Application):
    notacion_latina = ["DO","DO♯/RE♭","RE","RE♯/MI♭","MI","FA","FA♯/SOL♭","SOL","SOL♯/LA♭","LA","LA♯/SI♭","SI"]
    notacion_inglesa = ["C","C♯/D♭","D","D♯/E♭","E","F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B"]
    def get_es_sostenido(self,i):
    	if (len(self.get_notacion()[i]) > 4):
    		return True
    	else:
    		return False
    def get_notacion(self):
        idioma = locale.setlocale(locale.LC_ALL,'')
        if idioma == "es_ES.utf8":
           return self.notacion_latina
        else:
           return self.notacion_inglesa

class ApiHandler():
    def __init__(self):
    	self.AppData = AppData()
    	self.WebHandler = WebHandler()

class WebHandler():
    url = "http://127.0.0.1:5000"
    intervals = None
    def __init__(self):
        self.intervals = self.get_intervals()
    def check_con(self):
    	if self.get_intervals() is not None:
    		return True
    	return False
    def cut_text(self,text):
    	if len(text) > 30:
    		text = str(text[0:30])+"..."
    	return text
    def get_intervals(self):
        try:
            url = self.url+"/intervals"
            with urllib.request.urlopen(url) as response:
                resp = response.read()
            notes = json.loads(resp)
            return notes['data']
        except:
            return None
    def get_intervale_name(self):
    	if self.intervals is not None:
    		return self.intervals.keys()
    def get_intervale_distance(self):
        if self.intervals is not None:
        	return list(self.intervals.values())
    def get_songs(self,interval,orden):
        try:
            url = self.url+"/songs/"+str(interval)+"/"+str(orden)
            with urllib.request.urlopen(url) as response:
                resp = response.read()
            lista = json.loads(resp)
            return lista
        except:
            return None



# necesario llamarla para que aparezca una ventana, funcion bloqueante
       # Bucle principal o bucle de eventos


if __name__ == '__main__':
    win = MainWindows()
    win.show_all() #ventana esta visible
    Gtk.main() 
    #exit_status = app.run(sys.argv)
    #sys.exit(exit_status)
