from cProfile import label
from configparser import ConfigParser
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk


import guias
import remesas
import anexos
import destinos
import facturacion
import config
from home import show_home

def change_theme(theme):
    try:
        window.style.theme_use(theme)
        parser = ConfigParser()
        parser.read('config.ini')
        parser.set('theme', 'actual_theme', theme)
        with open('config.ini', 'w') as config_file:
            parser.write(config_file)
    
    except Exception as e:
        print(f"Error al cambiar el tema: {e}")


from config import load_config
get_config = load_config()
theme = get_config['theme'] # type: ignore

# Crear la ventana principal
#*****************BOOTSTRAP*******************#

# window = ttk.Window(themename="united",)
window = ttk.Window(themename=theme)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
full_screen = f"{screen_width}x{screen_height}"
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.config(background='red')
window.configure(background='red')

window.title("Control Guias y Facturacion Intermodal")
window.geometry(full_screen)
window.title("Control Guias y Facturacion Intermodal")
window.iconbitmap('assets/faviconV2.ico')
window.state('zoomed')
##********** MENU **********##

menu = ttk.Menu(window, )
menu_archivo = ttk.Menu(menu, tearoff=0)
menu_archivo.add_command(label="Inicio", command=lambda: show_home(main_frame, screen_width, screen_height))
menu_archivo.add_command(label="Salir", command=window.quit)
menu.add_cascade(label="Archivo", menu=menu_archivo)

menu_guias = ttk.Menu(menu, tearoff=0, )
menu_guias.add_command(label="Agregar Guías", command=lambda: guias.show_guias(main_frame,0, screen_width, screen_height))
menu_guias.add_command(label="Buscar Guía", command=lambda: guias.show_guias(main_frame, 1, screen_width, screen_height))
menu_guias.add_command(label="Total Guías", command=lambda: guias.show_guias(main_frame,2, screen_width, screen_height))
menu.add_cascade(label="Guías", menu=menu_guias)

menu_remesas = ttk.Menu(menu, tearoff=0)
menu_remesas.add_command(label="Agregar Remesa", command=lambda: remesas.show_remesas(main_frame,0, screen_width, screen_height))
menu_remesas.add_command(label="Buscar Remesa", command=lambda: remesas.show_remesas(main_frame,1, screen_width, screen_height))
# menu_remesas.add_command(label="Total Remesas", command=lambda: remesas.show_remesas(main_frame))
menu.add_cascade(label="Remesas", menu=menu_remesas)

menu_anexos = ttk.Menu(menu, tearoff=0)
menu_anexos.add_command(label="Agregar Anexo", command=lambda: anexos.show_anexos(main_frame,0, screen_width, screen_height))
menu_anexos.add_command(label="Buscar Anexo", command=lambda: anexos.show_anexos(main_frame,1, screen_width, screen_height))
# menu_anexos.add_command(label="Total Anexos", command=lambda: anexos.show_anexos(main_frame))
menu.add_cascade(label="Anexos", menu=menu_anexos)

menu_facturacion = ttk.Menu(menu, tearoff=0)
menu_facturacion.add_command(label="Agregar Factura", command=lambda: facturacion.show_facturacion(main_frame,0, screen_width, screen_height))
menu_facturacion.add_command(label="Buscar Factura", command=lambda: facturacion.show_facturacion(main_frame,1, screen_width, screen_height))
# menu_facturacion.add_c1ommand(label="Total Facturas", command=lambda: facturacion.show_facturacion(main_frame))
menu.add_cascade(label="Facturación", menu=menu_facturacion)

menu_destinos = ttk.Menu(menu, tearoff=0)
menu_destinos.add_command(label="Destinos y Tarifas", command=lambda: destinos.show_destinos(main_frame, screen_width, screen_height))
menu.add_cascade(label="Destinos", menu=menu_destinos)
menu_config = ttk.Menu(menu, tearoff=0)

menu_opciones = ttk.Menu(menu, tearoff=0)
menu_opciones.add_command(label="Configuración", command=lambda: config.show_config(main_frame, screen_width, screen_height))
menu_opciones.add_command(label="Crear copia de seguridad", command=lambda: config.show_config(main_frame, screen_width, screen_height))
menu.add_cascade(label="Configuración", menu=menu_opciones)

list_light_themes = ['cosmo', 'flatly', 'journal', 'litera', 'minty', 'lumen', 'united','pulse', 'sandstone', 'yeti',  'morph', 'cerculean', 'simplex']
list_dark_themes = ['superhero', 'solar', 'darkly', 'cyborg', 'vapor', ]

theme_var = StringVar(value=theme)  # Inicializar la variable con el tema actual

menu_temas = ttk.Menu(menu, tearoff=0)
menu.add_cascade(label="Temas", menu=menu_temas)

light_themes = ttk.Menu(menu_temas, tearoff=0)
for theme in list_light_themes:
    light_themes.add_radiobutton(label=theme, variable=theme_var, value=theme, command=lambda t=theme: change_theme(t))
menu_temas.add_cascade(label="Temas claros", menu=light_themes)

dark_themes = ttk.Menu(menu_temas, tearoff=0)
for theme in list_dark_themes:
    dark_themes.add_radiobutton(label=theme, variable=theme_var, value=theme, command=lambda t=theme: change_theme(t))
menu_temas.add_cascade(label="Temas oscuros", menu=dark_themes)

window.config(menu=menu)

main_frame = tk.Frame(window,    )
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

guias.show_guias(main_frame,0, screen_width, screen_height)

if __name__ == "__main__":
    window.mainloop()