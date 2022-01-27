#!/usr/bin/python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# You may contact Stan S via electronic mail with the address vfpro777@yahoo.com
#
# Based off of GPL'd code snippets I found.
# <http://www.eurion.net/python-snippets/snippet/Webkit%20Browser.html>
# <https://github.com/uiri/pygmy/>

import gi
gi.require_version('WebKit2', '4.0')
gi.require_version('Gtk', '3.0')
import os, time, threading, urllib, platform
from gi.repository import Gtk as gtk, Gdk, WebKit2, GObject as gobject

from operator import itemgetter

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class Browser:
    refresh_button = []
    forward_button = []
    back_button = []
    web_view = []
    scroll_window = []
    newtab = []
    closetab = []
    etcbutton = []
    jsbutton = []
    websettings = []
    historybutton = []
    hbox = []
    vbox = []
    url_bar = []
    history = []
    n = 0
    change_title = 0
    is_fullscreen = False
        
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.prefsfile = open(os.path.expanduser("~/pyExcalibur/prefs"), 'w')
        for p in self.preferences:
            p = str(p) + "\n"
            self.prefsfile.writelines(p)
        self.prefsfile.close()
        self.historyfile = open(os.path.expanduser("~/pyExcalibur/history"), 'w')
        for a in self.history:
            a = str(a[0] + ": " + a[1])
            self.historyfile.writelines(a)
        self.historyfile.close()
        gtk.main_quit()

    def __init__(self, urlwhichshallbeopened=None):
        if not os.path.exists(os.path.expanduser("~/pyExcalibur")):
            os.mkdir(os.path.expanduser("~/pyExcalibur"))
        if not os.path.exists(os.path.expanduser("~/pyExcalibur/prefs")):
            self.prefsfile = open(os.path.expanduser("~/pyExcalibur/prefs"), 'w')
            self.prefsfile.write("1\nhttp://bestinternetsearch.com/\n0\n1\n15\n")
            self.prefsfile.close()
        if urlwhichshallbeopened != None:
            self.preferences = [None, None, None, None, None]
        else:
            prefsfile = open(os.path.expanduser("~/pyExcalibur/prefs"), 'r')
            tmppref = prefsfile.readlines()
            self.preferences = []
            prefsfile.close()
            for pref in tmppref:
                self.preferences.append(pref.rstrip())
        self.window = gtk.Window(type=gtk.WindowType.TOPLEVEL)
        self.window.set_resizable(True)
        self.window.set_title("pyExcalibur Web")
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_default_size(1000,600)
        self.tabbook = gtk.Notebook()
        self.tabbook.set_scrollable(True)
        self.tabbook.popup_enable()
        if self.preferences[1] == '0':
            self.preferences[1] = "http://bestinternetsearch.com/"
        if self.preferences[0] == '1':
            self.tabbook.set_tab_pos(gtk.PositionType.LEFT)
        elif self.preferences[0] == '2':
            self.tabbook.set_tab_pos(gtk.PositionType.TOP)
        elif self.preferences[0] == '3':
            self.tabbook.set_tab_pos(gtk.PositionType.RIGHT)
        elif self.preferences[0] == '4':
            self.tabbook.set_tab_pos(gtk.PositionType.BOTTOM)
        else:
            self.tabbook.set_tab_pos(gtk.PositionType.LEFT)
        if urlwhichshallbeopened != None:
            self.addtab(openurl=urlwhichshallbeopened)
        else:
            self.addtab(openurl=self.preferences[1])

        self.mainbox.pack_start(self.tabbook, True, True, 0)
        self.tabbook.set_current_page(1)
        self.window.add(self.mainbox)
        self.window.show_all()
        self.tabbook.connect("switch_page", self.set_window_title)
        self.kbd_shortcuts(self.tabbook)

        #if self.preferences != None:
        #    if self.preferences[3] != '1': 
        if not os.path.exists(os.path.expanduser("~/pyExcalibur/history")):
            self.historyfile = open(os.path.expanduser("~/pyExcalibur/history"), 'w')
            self.historyfile.write("BestInternetSearch: http://www.bestinternetsearch.com\n")
            self.historyfile.close()
        self.historyfile = open(os.path.expanduser("~/pyExcalibur/history"), 'r')
        self.historytemp = self.historyfile.readlines()
        self.history = []
        for a in self.historytemp:
            a = a.split(": ")
            self.history.append(a)
            while 1:
                try:
                    self.history.remove('\n')
                except:
                    break
        self.historyfile.close()

    def addtab(self, widget=None, dummy=None, dummier=None, dummiest=None, openurl="http://bestinternetsearch.com/"):
        self.web_view.append(WebKit2.WebView())
        self.websettings.append(WebKit2.Settings())
        # to set user agent, uncomment
        self.websettings[len(self.websettings)-1].set_property('user-agent', 'iPad') # won't set at all
        # to enable, disable javascript
        self.websettings[len(self.websettings)-1].set_property('enable_javascript', True)
        # to enable, disable webgl
        self.websettings[len(self.websettings)-1].set_property("enable-webgl", True)
        
        self.web_view[len(self.web_view)-1].set_settings(self.websettings[len(self.websettings)-1])
        
        self.web_view[len(self.web_view)-1].load_uri(openurl)
        
        self.back_button.append(gtk.ToolButton(stock_id=gtk.STOCK_GO_BACK))
        self.back_button[len(self.back_button)-1].connect("clicked", self.go_back)

        self.forward_button.append(gtk.ToolButton(stock_id=gtk.STOCK_GO_FORWARD))
        self.forward_button[len(self.forward_button)-1].connect("clicked", self.go_forward)

        self.refresh_button.append(gtk.ToolButton(stock_id=gtk.STOCK_REFRESH))
        self.refresh_button[len(self.refresh_button)-1].connect("clicked", self.refresh)

        self.url_bar.append(gtk.Entry())
        self.url_bar[len(self.url_bar)-1].connect("activate", self.on_active)

        # enable (green), disable (red) javascript
        self.jsbutton.append(gtk.Button.new_with_label("js"))
        self.jsbutton[len(self.jsbutton)-1].connect("activate", self.toggle_js)
        self.jsbutton[len(self.jsbutton)-1].connect("clicked", self.toggle_js)

        #self.jsbutton[len(self.jsbutton)-1].modify_bg(gtk.StateType.NORMAL, Gdk.color_parse("red")) 
        self.jsbutton[len(self.jsbutton)-1].set_name("name_entry")
        provider = gtk.CssProvider()
        provider.load_from_data(bytes('#name_entry { background: green; }'.encode() ))
        self.jsbutton[len(self.jsbutton)-1].get_style_context().add_provider(provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.etcbutton.append(gtk.Button.new_with_label("Prefs"))
        self.historybutton.append(gtk.Button.new_with_label("Hist"))
        self.historybutton[len(self.historybutton)-1].connect("activate", self.historytab)
        self.historybutton[len(self.historybutton)-1].connect("clicked", self.historytab)
        self.etcbutton[len(self.etcbutton)-1].connect("activate", self.show_prefs)
        self.etcbutton[len(self.etcbutton)-1].connect("clicked", self.show_prefs)
        self.newtab.append(gtk.Button.new_with_label("+"))
        self.newtab[len(self.newtab)-1].connect("activate", self.addtab)
        self.newtab[len(self.newtab)-1].connect("clicked", self.addtab)
        self.closetab.append(gtk.Button.new_with_label("X"))
        self.closetab[len(self.closetab)-1].connect("activate", self.removetab)
        self.closetab[len(self.closetab)-1].connect("clicked", self.removetab)

        self.web_view[len(self.web_view)-1].connect("load_changed", self.on_load_changed)
        #self.web_view[len(self.web_view)-1].connect("download_requested", self.download)

        self.scroll_window.append(gtk.ScrolledWindow(hadjustment=None, vadjustment=None))
        self.scroll_window[len(self.scroll_window)-1].add(self.web_view[len(self.web_view)-1])
        self.scroll_window[len(self.scroll_window)-1].set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)

        self.hbox.append(gtk.HBox(homogeneous=False, spacing=0))
        self.vbox.append(gtk.VBox(homogeneous=False, spacing=0))
        self.mainbox = gtk.VBox(homogeneous=False, spacing=0)
        self.hbox[len(self.hbox)-1].pack_start(self.back_button[len(self.back_button)-1], False, True, 0)
        self.hbox[len(self.hbox)-1].pack_start(self.forward_button[len(self.forward_button)-1], False, True, 0)
        self.hbox[len(self.hbox)-1].pack_start(self.refresh_button[len(self.refresh_button)-1], False, True, 0)
        self.hbox[len(self.hbox)-1].pack_start(self.newtab[len(self.newtab)-1], False, True, 3)
        self.hbox[len(self.hbox)-1].pack_start(self.closetab[len(self.closetab)-1], False, True, 0)
        self.hbox[len(self.hbox)-1].pack_start(self.url_bar[len(self.url_bar)-1], True, True, 3)
        
        self.hbox[len(self.hbox)-1].pack_start(self.jsbutton[len(self.jsbutton)-1], False, True, 0)
        
        self.hbox[len(self.hbox)-1].pack_start(self.historybutton[len(self.historybutton)-1], False, True, 0)
        self.hbox[len(self.hbox)-1].pack_start(self.etcbutton[len(self.etcbutton)-1], False, True, 0)
        self.vbox[len(self.vbox)-1].pack_start(self.hbox[len(self.hbox)-1], False, True, 0)
        self.vbox[len(self.vbox)-1].pack_start(self.scroll_window[len(self.scroll_window)-1], True, True, 0)
        self.tabbook.append_page(self.vbox[len(self.vbox)-1])
        self.tabbook.show_all()
        self.tabbook.set_current_page(len(self.vbox)-1+self.n)

    def on_active(self, widge, data=None):
        '''When the user enters an address in the bar, we check to make
           sure they added the http://, if not we add it for them.  Once
           the url is correct, we just ask WebKit2 to open that site.'''
        url = self.url_bar[self.tabbook.get_current_page()-self.n].get_text()
        try:
            url.index(" ")
            url = "http://google.ca/search?q=" + url
        except:
            try:
                url.index("mailto")
                try:
                    platform.system().index("Win")
                    os.system("start "+url)
                except:
                    try:
                        platform.system().index("Dar")
                        os.system("open "+url)
                    except:
                        try:
                            platform.system().index("Lin")
                            os.system("xdg-open "+url)
                        except:
                            print( "Good for you for running this on an unsupported system. Sorry, this thing can't open mailto urls for you")
            except:
                try:
                    url.index("://")
                except:
                    url = "http://"+url
        self.url_bar[self.tabbook.get_current_page()-self.n].set_text(url)
        try:
            url.index("mailto")
        except:
            self.web_view[self.tabbook.get_current_page()-self.n].load_uri(url)

    def go_back(self, widget, data=None, other=None, etc=None):
        '''Webkit will remember the links and this will allow us to go
           backwards.'''
        self.web_view[self.tabbook.get_current_page()-self.n].go_back()

    def go_forward(self, widget, data=None, other=None, etc=None):
        '''Webkit will remember the links and this will allow us to go
           forwards.'''
        self.web_view[self.tabbook.get_current_page()-self.n].go_forward()

    def refresh(self, widget, data=None, etc=None, more=None):
        '''Simple makes WebKit2 reload the current back.'''
        self.web_view[self.tabbook.get_current_page()-self.n].reload()

    def on_load_changed(self, widget, event):
    
        # set_tab_title
        if event == WebKit2.LoadEvent.FINISHED:
            #if self.preferences != None:
            #   maxlen = self.preferences[4]
            #else:
            maxlen = '15'
            
            if self.web_view[self.tabbook.get_current_page()-self.n].get_title() != None:
                real_title = self.web_view[self.tabbook.get_current_page()-self.n].get_title()
                if len(self.web_view[self.tabbook.get_current_page()-self.n].get_title()) > int(maxlen):
                    newmaxlen = int(maxlen) - 3
                    script = 'document.title=document.title.substring(0,' + str(newmaxlen) + ') + "...";'
                    self.web_view[self.tabbook.get_current_page()-self.n].run_javascript(script)
                self.tabbook.set_tab_label_text(self.vbox[self.tabbook.get_current_page()-self.n], self.web_view[self.tabbook.get_current_page()-self.n].get_title())
                self.tabbook.get_tab_label(self.vbox[self.tabbook.get_current_page()-self.n]).set_tooltip_text(real_title)
                self.window.set_title(self.tabbook.get_tab_label(self.vbox[self.tabbook.get_current_page()-self.n]).get_text() + " - pyExcalibur Web")
            else:
                newmaxlen = int(maxlen) - 3
                if len(self.web_view[self.tabbook.get_current_page()-self.n].get_main_frame().get_uri()) > int(maxlen):
                    uri = self.web_view[self.tabbook.get_current_page()-self.n].get_main_frame().get_uri()[0:newmaxlen] + "..."
                else:
                    uri = self.web_view[self.tabbook.get_current_page()-self.n].get_main_frame().get_uri()
                self.tabbook.set_tab_label_text(self.vbox[self.tabbook.get_current_page()-self.n], uri)
                self.tabbook.get_tab_label(self.vbox[self.tabbook.get_current_page()-self.n]).set_tooltip_text(self.web_view[self.tabbook.get_current_page()-self.n].get_main_frame().get_uri())
                self.window.set_title("pyExcalibur Web")
            self.change_title = 0
        
        # update_buttons
        if event == WebKit2.LoadEvent.COMMITTED:
            '''Gets the current url entry and puts that into the url bar.
               It then checks to see if we can go back, if we can it makes the
               back button clickable.  Then it does the same for the forward
               button.'''        
            self.url = widget.get_uri()
            histthread = threading.Thread(target=self.addhistoryitem)
            histthread.daemon = True
            histthread.start()
            self.url_bar[self.tabbook.get_current_page()-self.n].set_text(self.url)
            self.tabbook.set_tab_label_text(self.vbox[self.tabbook.get_current_page()-self.n], "Loading...")
            self.tabbook.get_tab_label(self.vbox[self.tabbook.get_current_page()-self.n]).set_tooltip_text("LOADING!")
            self.window.set_title("Loading...")
            self.back_button[self.tabbook.get_current_page()-self.n].set_sensitive(self.web_view[self.tabbook.get_current_page()-self.n].can_go_back())
            self.forward_button[self.tabbook.get_current_page()-self.n].set_sensitive(self.web_view[self.tabbook.get_current_page()-self.n].can_go_forward())
        

    def addhistoryitem(self):
        url = self.url
        view = self.web_view[self.tabbook.get_current_page()-self.n]
        time.sleep(10)
        nurl = url + "\n"
        unique = 0
        for h in self.history:
            if nurl == h[1]:
                unique = 1
            if url == h[1]:
                unique = 1
        if unique == 0:
            self.history.append([view.get_title(), url + "\n"])
            try:
                self.historybox
                uri = url.rstrip()
                self.historyliststore.append([self.history[len(self.history)-1][0], uri])
            except:
                uri = url.rstrip()

    def set_window_title(self, widget, weirdpointerthing, n):
        if n-self.n >= 0:
            if self.tabbook.get_tab_label(self.vbox[n-self.n]) != None:
                self.window.set_title(self.tabbook.get_tab_label(self.vbox[n-self.n]).get_text() + " - pyExcalibur Web")
            else:
                self.window.set_title("pyExcalibur Web")
        else:
            if self.tabbook.get_tab_label_text(self.tabbook.get_nth_page(n)) == "History":
                self.window.set_title("History - pyExcalibur Web")
                
    def removetab(self, widget=None, dummy=None, dummier=None, dummiest=None):
        if self.tabbook.get_current_page()-self.n >= 0:
            self.web_view.pop(self.tabbook.get_current_page()-self.n)
            self.back_button.pop(self.tabbook.get_current_page()-self.n)
            self.forward_button.pop(self.tabbook.get_current_page()-self.n)
            self.refresh_button.pop(self.tabbook.get_current_page()-self.n)
            self.url_bar.pop(self.tabbook.get_current_page()-self.n)
            self.newtab.pop(self.tabbook.get_current_page()-self.n)
            self.closetab.pop(self.tabbook.get_current_page()-self.n)
            self.scroll_window.pop(self.tabbook.get_current_page()-self.n)
            self.hbox.pop(self.tabbook.get_current_page()-self.n)
            self.vbox.pop(self.tabbook.get_current_page()-self.n)
            
            self.jsbutton.pop(self.tabbook.get_current_page()-self.n)
        else:
            self.n = self.n - 1
        self.tabbook.remove_page(self.tabbook.get_current_page())
        if self.tabbook.get_current_page() == -1:
            self.destroy(self.tabbook)

    def kbd_shortcuts(self, widget):
        self.kbdgroup = gtk.AccelGroup()
        self.window.add_accel_group(self.kbdgroup)
        self.kbdgroup.connect(Gdk.keyval_from_name('O'), Gdk.ModifierType.CONTROL_MASK, 0, self.select_all_url)
        self.kbdgroup.connect(Gdk.keyval_from_name('W'), Gdk.ModifierType.CONTROL_MASK, 0, self.removetab)
        self.kbdgroup.connect(Gdk.keyval_from_name('T'), Gdk.ModifierType.CONTROL_MASK, 0, self.addtab)
        self.kbdgroup.connect(Gdk.keyval_from_name('R'), Gdk.ModifierType.CONTROL_MASK, 0, self.refresh)
        self.kbdgroup.connect(Gdk.keyval_from_name('H'), Gdk.ModifierType.CONTROL_MASK, 0, self.historytab)
        self.kbdgroup.connect(Gdk.KEY_bracketright, Gdk.ModifierType.CONTROL_MASK, 0, self.go_back)
        self.kbdgroup.connect(Gdk.KEY_bracketleft, Gdk.ModifierType.CONTROL_MASK, 0, self.go_forward)
        self.kbdgroup.connect(Gdk.keyval_from_name('F'), Gdk.ModifierType.CONTROL_MASK, 0, self.search_page)
        self.kbdgroup.connect(Gdk.keyval_from_name('P'), Gdk.ModifierType.MOD1_MASK, 0, self.show_prefs)

    def select_all_url(self, kbdgroup, window, key, mod):
        self.url_bar[self.tabbook.get_current_page()-self.n].grab_focus()

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.window.unfullscreen()
            self.is_fullscreen = False
        else:
            self.window.fullscreen()
            self.is_fullscreen = True        
        
    def on_key_press(self, widget, event):
        ctrl = (event.get_state() & Gdk.ModifierType.CONTROL_MASK)
        
        if event.keyval == Gdk.KEY_Escape:
            gtk.main_quit()
        elif event.keyval == Gdk.KEY_F11:
            self.toggle_fullscreen()
        elif event.keyval == Gdk.KEY_s and ctrl:
            self.take_screenshot()
        elif event.keyval == Gdk.KEY_p and ctrl:
            self.export_to_pdf()
        
    def _get_view_image(self):
        window = Gdk.Screen.get_active_window(Gdk.Screen.get_default())
        #window = Gdk.get_default_root_window().get_screen().get_active_window()
        x, y, width, height = window.get_geometry()
        pixbuf = Gdk.pixbuf_get_from_window(window, 0, 0, width, height)
        return pixbuf

    def take_screenshot(self, path=None):
        if path is None:
            path = time.strftime("%m%d%y-%H%M%S.png")
            
        pixbuf = self._get_view_image()
        pixbuf.savev(path, "png", [],[])

    def export_to_pdf(self, path=None):
        if path is None:
            path = time.strftime("%m%d%y-%H%M%S.pdf")
            
        operation = gtk.PrintOperation()
        operation.set_export_filename(path)
        operation.connect("begin-print", self.__begin_print_cb)
        operation.connect("draw-page", self.__draw_page_cb)
        operation.run(gtk.PrintOperationAction.EXPORT, self.window)
        
    def __begin_print_cb(self, operation, context, data=None):
        settings = operation.get_print_settings()
        pixbuf = self._get_view_image()
        rect = self.window.get_allocation()
        paper_size = gtk.PaperSize.new_custom("custom", "custom",
             pixel_to_mm(rect.width),
             pixel_to_mm(rect.height), gtk.Unit.MM)
        settings.set_paper_size(paper_size)
        page_setup = gtk.PageSetup()
        page_setup.set_top_margin(0, gtk.Unit.POINTS)
        page_setup.set_bottom_margin(0, gtk.Unit.POINTS)
        page_setup.set_left_margin(0, gtk.Unit.POINTS)
        page_setup.set_right_margin(0, gtk.Unit.POINTS)

        operation.set_default_page_setup(page_setup)
        settings.set_orientation
        operation.set_n_pages(1)

    def __draw_page_cb(self, operation, context, page_nr):
        cr = context.get_cairo_context()
        layout = context.create_pango_layout()
        pango_context = layout.get_context()
        pixbuf = self._get_view_image()
        #cr.set_source_pixbuf(pixbuf,0,0)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        #cr.show_layout(layout)
        #PangoCairo.show_layout(cr, layout)
        
    def toggle_js(self, widget):
        if self.websettings[self.tabbook.get_current_page()-self.n].get_property('enable_javascript') == False:
            self.websettings[self.tabbook.get_current_page()-self.n].set_property('enable_javascript', True)
            self.jsbutton[self.tabbook.get_current_page()-self.n].set_name("name_entry2")
            provider = gtk.CssProvider()
            provider.load_from_data(bytes('#name_entry2 { background: green; }'.encode() ))
            self.jsbutton[len(self.jsbutton)-1].get_style_context().add_provider(provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        else:
            self.websettings[self.tabbook.get_current_page()-self.n].set_property('enable_javascript', False)
            self.jsbutton[self.tabbook.get_current_page()-self.n].set_name("name_entry3")
            provider = gtk.CssProvider()
            provider.load_from_data(bytes('#name_entry3 { background: red; }'.encode() ))
            self.jsbutton[len(self.jsbutton)-1].get_style_context().add_provider(provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)



    def historytab(self, something=None, other=None, somethingelse=None, lol=None):
        self.historysearch = gtk.Entry()
        histclosebutton = gtk.Button(label='X')
        histclosebutton.connect("activate", self.removetab)
        histclosebutton.connect("clicked", self.removetab)
        self.historysearch.connect("activate", self.search_history)
        historysearchbutton = gtk.Button(label='Search')
        historysearchbutton.connect("activate", self.search_history)
        historysearchbutton.connect("clicked", self.search_history)
        historysearchbox = gtk.HBox(homogeneous=False, spacing=0)
        historysearchbox.pack_start(self.historysearch, False, True, 0)
        historysearchbox.pack_start(historysearchbutton, False, True, 0)
        historysearchbox.pack_end(histclosebutton, False, True, 0)
        self.historyliststore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        for item in self.history:
            uri = item[1].rstrip()
            self.historyliststore.append([item[0], uri])
        self.historylistview = gtk.TreeView(model=self.historyliststore)
        historylistcell = gtk.CellRendererText()
        historylistcell2 = gtk.CellRendererText()
        historylistcol = gtk.TreeViewColumn('Title', historylistcell, text=0)
        historylistcol2 = gtk.TreeViewColumn('URL', historylistcell2, text=1)
        historylistscroll = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        historylistscroll.set_policy(gtk.PolicyType.NEVER, gtk.PolicyType.AUTOMATIC)
        historylistscroll.add(self.historylistview)
        self.historylistview.append_column(historylistcol)
        self.historylistview.append_column(historylistcol2)
        self.historybox = gtk.VBox(homogeneous=False, spacing=0)
        self.historybox.pack_start(historysearchbox, False, True, 0)
        self.historybox.pack_start(historylistscroll, True, True, 0)
        self.tabbook.prepend_page(self.historybox)
        self.tabbook.show_all()
        self.tabbook.set_tab_label_text(self.historybox, "History")
        self.tabbook.get_tab_label(self.historybox).set_tooltip_text("History")
        self.tabbook.set_current_page(0)
        self.n = self.n + 1
        self.historylistview.connect("row-activated", self.openhistoryitem)

    def openhistoryitem(self, treeview, path, view_column):
        historyrow, historydata = self.historylistview.get_selection().get_selected()
        historydata = historyrow.get_iter(path[0])
        histurl = historyrow.get_value(historydata, 1)
        self.addtab(None, None, None, None, histurl)

    def search_history(self, whatever=None, something=None, overboard=None):
        histres = []
        if self.historysearch.get_text == "":
            histres = self.history
        else:
            terms = self.historysearch.get_text()
            for row in self.history:
                if row[1].rstrip().find(terms) != -1:
                    histres.append([row[0], row[1].rstrip()])
        histresstore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        for item in histres:
            histresstore.append([item[0], item[1]])
        self.historylistview.set_model(histresstore)

    def search_page(self, some=None, thing=None, other=None, etc=None):
        try:
            self.searchbox.show()
            self.searchentry.grab_focus()
        except:
            self.searchentry = gtk.Entry()
            searchbutton = gtk.Button('Search')
            searchbutton.connect("activate", self.perform_search)
            searchbutton.connect("clicked", self.perform_search)
            self.searchentry.connect("activate", self.perform_search)
            closesearch = gtk.Button('X')
            self.searchbox = gtk.HBox(False, 0)
            closesearch.connect("activate", self.remove_search, self.searchbox, self.searchentry)
            closesearch.connect("clicked", self.remove_search, self.searchbox, self.searchentry)
            self.searchbox.pack_start(self.searchentry, False, True, 0)
            self.searchbox.pack_start(searchbutton, False, True, 0)
            self.searchbox.pack_end(closesearch, False, True, 5)
            self.vbox[self.tabbook.get_current_page()-self.n].pack_end(self.searchbox, False, True, 0)
            self.vbox[self.tabbook.get_current_page()-self.n].show_all()
            self.searchentry.grab_focus()

    def perform_search(self, some=None, thing=None, other=None, etc=None):
        self.web_view[self.tabbook.get_current_page()-self.n].search_text(self.searchentry.get_text(), False, True, True)
        
    def remove_search(self, some, searchbox, searchentry):
        searchbox.hide()

    def download(self, widget, download):
        saveas = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        saveas.set_default_response(gtk.RESPONSE_OK)
        resp = saveas.run()
        if resp == gtk.RESPONSE_OK:
            downloadto = saveas.get_filename()
        saveas.destroy()
        downloadfrom = download.get_network_request().get_uri()
        urllib.urlretrieve(downloadfrom, downloadto)

    def show_prefs(self, widget, some=None, thing=None, other=None):
        self.prefwin = gtk.Window()
        self.prefwin.set_title("pyExcalibur Preferences")
        self.prefwin.set_default_size(200, 200)

        tabposbox = gtk.HBox(homogeneous=False, spacing=0)
        self.leftbutton = gtk.RadioButton.new_with_label_from_widget(None, label="Left")
        self.topbutton = gtk.RadioButton.new_with_label_from_widget(self.leftbutton, label="Top")
        self.rightbutton = gtk.RadioButton.new_with_label_from_widget(self.leftbutton, label="Right")
        self.bottombutton = gtk.RadioButton.new_with_label_from_widget(self.leftbutton, label="Bottom")
        
        tabposlabel = gtk.Label(label="Tab Position:")
        tabposbox.pack_start(tabposlabel, False, False, 0)
        tabposbox.pack_start(self.leftbutton, False, False, 0)
        tabposbox.pack_start(self.topbutton, False, False, 0)
        tabposbox.pack_start(self.rightbutton, False, False, 0)
        tabposbox.pack_start(self.bottombutton, False, False, 0)

        homebox = gtk.HBox(homogeneous=False, spacing=0)
        homelabel = gtk.Label(label="Homepage: ")
        self.homeentry = gtk.Entry()
        homebox.pack_start(homelabel, False, True, 10)
        homebox.pack_start(self.homeentry, True, True, 10)

        checkbox = gtk.HBox(homogeneous=False, spacing=0)
        self.rssbutton = gtk.CheckButton(label="Show RSS Tab", stock=False)
        self.histbutton = gtk.CheckButton(label="Record History", stock=False)
        checkbox.pack_start(self.rssbutton, False, True, 0)
        checkbox.pack_start(self.histbutton, False, True, 0)

        widthbox = gtk.HBox(homogeneous=False, spacing=0)
        widthlabel = gtk.Label(label="Tab width (in characters):")
        self.widthbutton = gtk.SpinButton()
        self.widthbutton.set_range(0, 99)
        self.widthbutton.set_value(15)
        self.widthbutton.set_increments(1.0, 1.0)
        widthbox.pack_start(widthlabel, False, True, 5)
        widthbox.pack_start(self.widthbutton, False, True, 5)

        donebox = gtk.HBox(homogeneous=False, spacing=0)
        cancelbutton = gtk.Button(label="Cancel")
        okbutton = gtk.Button(label="OK")
        donebox.pack_start(cancelbutton, True, False, 0)
        donebox.pack_start(okbutton, True, False, 0)

        okbutton.connect("activate", self.write_prefs)
        okbutton.connect("clicked", self.write_prefs)
        cancelbutton.connect("activate", self.write_prefs)
        cancelbutton.connect("clicked", self.write_prefs)

        if self.preferences != None:
            if self.preferences[0] == '4':
                self.bottombutton.set_active(True)
            elif self.preferences[0] == '2':
                self.topbutton.set_active(True)
            elif self.preferences[0] =='3':
                self.rightbutton.set_active(True)
            else:
                self.leftbutton.set_active(True)
            self.homeentry.set_text(self.preferences[1])
            if self.preferences[2] != '0':
               self.rssbutton.set_active(True)
            if self.preferences[3] == '0':
                self.histbutton.set_active(True)
            self.widthbutton.set_value(float(self.preferences[4]))
        
        prefbox = gtk.VBox(homogeneous=False, spacing=0)
        prefbox.pack_start(tabposbox, False, True, 5)
        prefbox.pack_start(homebox, False, True, 5)
        prefbox.pack_start(checkbox, False, True, 5)
        prefbox.pack_start(widthbox, False, True, 5)
        prefbox.pack_start(donebox, False, True, 5)
        self.prefwin.add(prefbox)
        self.prefwin.show_all()
            
    def write_prefs(self, first):
        if first.get_label() == 'OK':
            self.preferences = []
            if self.bottombutton.get_active():
               self.preferences.append('4')
            elif self.topbutton.get_active():
               self.preferences.append('2')
            elif self.rightbutton.get_active():
               self.preferences.append('3')
            else:
               self.preferences.append('1')
            if self.homeentry.get_text():
                self.preferences.append(self.homeentry.get_text())
            else:
                self.preferences.append('0')
            if self.rssbutton.get_active():
                self.preferences.append('1')
            else:
                self.preferences.append('0')
            if self.histbutton.get_active():
                self.preferences.append('0')
            else:
                self.preferences.append('1')
            self.preferences.append(str(self.widthbutton.get_value_as_int()))
        self.prefwin.hide()

    def destroy_prefs(self):
        self.prefwin.hide()

    def main(self):
        gtk.main()

def pixel_to_mm(pixels, dpi=600):
    # empirically obtained :P
    return pixels / 2.9
        
if __name__ == "__main__":
    browser = Browser()
    browser.main()

    
