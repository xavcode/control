import tkinter as tk

import guias, remesas, anexos, destinos, config

# Crear la ventana principal
window = tk.Tk()
window.title("Control Guias y Facturacion Intermodal")
window.geometry("1360x768")
window.configure( )

main_frame = tk.Frame(window, bd=2, relief="groove",width=1200, height=600)
main_frame.grid(row=0, column=50, sticky="wens", pady=10, padx=10)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_propagate(False)

# Frame para los botones

frame_botones = tk.Frame(window)
frame_botones.grid(row=0,column=0, sticky="we", padx=10, pady=20,)
frame_botones.config()

# Botón para mostrar el boton home
btn_home = tk.Button(frame_botones, text="Inicio", width=12)
btn_home.grid(row=0, column=0, pady=10)

# Botón para mostrar el formulario de guías
btn_guias = tk.Button(frame_botones, text="Guías", command=lambda: guias.show_guias(main_frame), width=12)
btn_guias.grid(row=1, column=0, pady=10)

# Botón para mostrar el formulario de remesas
btn_remesas = tk.Button(frame_botones, text="Remesas", command=lambda: remesas.show_remesas(main_frame), width=12,)
btn_remesas.grid(row=2, column=0, pady=10)

# Botón para mostrar el formulario de anexos
btn_anexos = tk.Button(frame_botones, text="Anexos", width=12, command=lambda: anexos.show_anexos(main_frame))
btn_anexos.grid(row=3, column=0, pady=10)
# Botón para mostrar el formulario de anexos

btn_anexos = tk.Button(frame_botones, text="Destinos", width=12, command=lambda: destinos.show_destinos(main_frame))
btn_anexos.grid(row=4, column=0, pady=10)

# Botón para mostrar el formulario de facturación
btn_facturacion = tk.Button(frame_botones, text="Facturación", width=12, state="disabled") 
btn_facturacion.grid(row=5, column=0, pady=10)

btn_config = tk.Button(frame_botones, text='Configuración', width=12, command=lambda: config.show_config(main_frame))
btn_config.grid(row=6, column=0, pady=10)




if __name__ == "__main__":
    window.mainloop()
