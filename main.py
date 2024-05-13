import tkinter as tk
from tkinter import *
from tkinter import ttk
from config import load_config


import guias, remesas, anexos, destinos, facturacion, config
load_config()
# Crear la ventana principal
window = tk.Tk()
window.title("Control Guias y Facturacion Intermodal")
window.geometry("1360x800")
window.resizable(False, False)

##********** MENU **********##

menu = Menu(window)
menu_archivo = Menu(menu, tearoff=0)
menu_archivo.add_command(label="Guías", command=lambda: guias.show_guias(main_frame))
menu_archivo.add_command(label="Remesas", command=lambda: remesas.show_remesas(main_frame))
menu_archivo.add_command(label="Anexos", command=lambda: anexos.show_anexos(main_frame))
menu_archivo.add_command(label="Facturación", command=lambda: facturacion.show_facturacion(main_frame))
menu_archivo.add_command(label="Destinos", command=lambda: destinos.show_destinos(main_frame))
menu_archivo.add_command(label="Configuración", command=lambda: config.show_config(main_frame))
menu_archivo.add_command(label="Salir", command=window.quit)

menu.add_cascade(label="Archivo", menu=menu_archivo)

menu_guias = Menu(menu, tearoff=0)
menu_guias.add_command(label="Agregar Guía", command=lambda: guias.show_guias(main_frame))
menu_guias.add_command(label="Buscar Guía", command=lambda: guias.show_guias(main_frame))
menu_guias.add_command(label="Total Guías", command=lambda: guias.show_guias(main_frame))
menu.add_cascade(label="Guías", menu=menu_guias)

menu_remesas = Menu(menu, tearoff=0)
menu_remesas.add_command(label="Agregar Remesa", command=lambda: remesas.show_remesas(main_frame))
menu_remesas.add_command(label="Buscar Remesa", command=lambda: remesas.show_remesas(main_frame))
menu_remesas.add_command(label="Total Remesas", command=lambda: remesas.show_remesas(main_frame))
menu.add_cascade(label="Remesas", menu=menu_remesas)

menu_anexos = Menu(menu, tearoff=0)
menu_anexos.add_command(label="Agregar Anexo", command=lambda: anexos.show_anexos(main_frame))
menu_anexos.add_command(label="Buscar Anexo", command=lambda: anexos.show_anexos(main_frame))
menu_anexos.add_command(label="Total Anexos", command=lambda: anexos.show_anexos(main_frame))
menu.add_cascade(label="Anexos", menu=menu_anexos)

menu_facturacion = Menu(menu, tearoff=0)
menu_facturacion.add_command(label="Agregar Factura", command=lambda: facturacion.show_facturacion(main_frame))
menu_facturacion.add_command(label="Buscar Factura", command=lambda: facturacion.show_facturacion(main_frame))
menu_facturacion.add_command(label="Total Facturas", command=lambda: facturacion.show_facturacion(main_frame))
menu.add_cascade(label="Facturación", menu=menu_facturacion)

menu_destinos = Menu(menu, tearoff=0)
menu_destinos.add_command(label="Agregar Destino", command=lambda: destinos.show_destinos(main_frame))
menu_destinos.add_command(label="Buscar Destino", command=lambda: destinos.show_destinos(main_frame))
menu_destinos.add_command(label="Total Destinos", command=lambda: destinos.show_destinos(main_frame))
menu.add_cascade(label="Destinos", menu=menu_destinos)
menu_config = Menu(menu, tearoff=0)

menu_opciones = Menu(menu, tearoff=0)
menu_opciones.add_command(label="Configuración", command=lambda: config.show_config(main_frame))
menu_opciones.add_command(label="Crear copia de seguridad", command=lambda: config.show_config(main_frame))
menu.add_cascade(label="Configuración", menu=menu_opciones)


window.config(menu=menu)


window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

main_frame = ttk.LabelFrame(window, width=1200, height=700)
main_frame.grid(row=0, column=1, sticky="wens", padx=10, pady=10, )
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_propagate(False)


def main_frame_show():
    for widget in main_frame.winfo_children():
        widget.destroy()

main_frame = ttk.LabelFrame(window, width=1200, height=700, )
main_frame.grid(row=0, column=0, sticky="wens", padx=10, pady=10, )
# main_frame.grid_rowconfigure(0, weight=1)
# main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_propagate(False)  
image_path = "assets/intermodal_camion.png"
image = tk.PhotoImage(file=image_path)
label = ttk.Label(main_frame, image=image)
label.grid(row=0, column=0, sticky="") 

# Frame para los botones
frame_botones = ttk.Frame(window)
frame_botones.grid(row=0,column=0, sticky="nswe", padx=10, pady=20)
frame_botones.config()

# frame_botones = ttk.Frame(window)
# frame_botones.grid(row=0,column=0, sticky="nswe", padx=10, pady=20)
# frame_botones.config()


# btn_home = ttk.Button(frame_botones, text="Inicio", width=12, command=lambda: main_frame_show())
# btn_home.grid(row=0, column=0, pady=10)


# btn_guias = ttk.Button(frame_botones, text="Guías", command=lambda: guias.show_guias(main_frame), width=12)
# btn_guias.grid(row=1, column=0, pady=10)


# btn_remesas = ttk.Button(frame_botones, text="Remesas", command=lambda: remesas.show_remesas(main_frame), width=12,)
# btn_remesas.grid(row=2, column=0, pady=10)


# btn_anexos = ttk.Button(frame_botones, text="Anexos", width=12, command=lambda: anexos.show_anexos(main_frame))
# btn_anexos.grid(row=3, column=0, pady=10)


# btn_facturacion = ttk.Button(frame_botones, text="Facturación", width=12, command=lambda: facturacion.show_facturacion(main_frame))
# btn_facturacion.grid(row=4, column=0, pady=10)


# btn_destinos = ttk.Button(frame_botones, text="Destinos", width=12, command=lambda: destinos.show_destinos(main_frame))
# btn_destinos.grid(row=5, column=0, pady=10)

btn_config = ttk.Button(frame_botones, text='Configuración', width=12, command=lambda: config.show_config(main_frame))
btn_config.grid(row=6, column=0, pady=10)
# btn_config = ttk.Button(frame_botones, text='Configuración', width=12, command=lambda: config.show_config(main_frame))
# btn_config.grid(row=6, column=0, pady=10)


if __name__ == "__main__":
    window.mainloop()

##**-------------------------------------------------**##
# style = ttk.Style(window)
# style.configure("TButton", background="white")
# style.configure("TLabel", background="white")
# style.configure("TFrame", background="white")
# style.configure("TLabelFrame", background="white")

# main_frame = ttk.Frame(window, width=1200, height=700, style="TLabelFrame.TFrame")
# main_frame.grid(row=0, column=1, sticky="wens", padx=10, pady=10, )
# main_frame.grid_rowconfigure(0, weight=1)
# main_frame.grid_columnconfigure(0, weight=1)
# main_frame.grid_propagate(False)
##**-------------------------------------------------**##