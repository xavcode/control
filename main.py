from tkinter import * # type: ignore

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# from ttkthemes import ThemedTk
import guias
import remesas
import anexos
import destinos
import facturacion
import config

# Crear la ventana principal
#*****************BOOTSTRAP*******************#

# window = ttk.Window(themename="united",)
window = ttk.Window(themename="superhero",)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
full_screen = f"{screen_width}x{screen_height}"


window.title("Control Guias y Facturacion Intermodal")
window.geometry(full_screen)
window.state('zoomed')
# window.grid_columnconfigure(0, weight=1)
# window.grid_rowconfigure(0, weight=1)

##********** MENU **********##

menu = ttk.Menu(window, )
menu_archivo = ttk.Menu(menu, tearoff=0)
menu_archivo.add_command(label="Salir", command=window.quit)

menu.add_cascade(label="Archivo", menu=menu_archivo)

menu_guias = ttk.Menu(menu, tearoff=0, background='#2b2b2b', foreground='white', activebackground='#3b3b3b', activeforeground='white')
menu_guias.add_command(label="Buscar Guía", command=lambda: guias.show_guias(main_frame, 0, screen_width, screen_height))
menu_guias.add_command(label="Agregar Guías", command=lambda: guias.show_guias(main_frame,1, screen_width, screen_height))
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
# menu_destinos.add_command(label="Buscar Destino", command=lambda: destinos.show_destinos(main_frame, screen_width, screen_height))
# menu_destinos.add_command(label="Total Destinos", command=lambda: destinos.show_destinos(main_frame, screen_width, screen_height))
menu.add_cascade(label="Destinos", menu=menu_destinos)
menu_config = ttk.Menu(menu, tearoff=0)

menu_opciones = ttk.Menu(menu, tearoff=0)
menu_opciones.add_command(label="Configuración", command=lambda: config.show_config(main_frame, screen_width, screen_height))
menu_opciones.add_command(label="Crear copia de seguridad", command=lambda: config.show_config(main_frame, screen_width, screen_height))
menu.add_cascade(label="Configuración", menu=menu_opciones)

window.config(menu=menu)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

def main_frame_show():
    for widget in main_frame.winfo_children():
        widget.destroy()

main_frame = ttk.Frame(window,   )
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)


# image_path = "assets/intermodal_hero.png"
# image = tk.PhotoImage(file=image_path)
# label = ttk.Label(main_frame, image=image)
# label.grid(row=0, column=0, columnspan=3, rowspan=3, sticky="")


if __name__ == "__main__":
    window.mainloop()
