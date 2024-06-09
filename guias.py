import re
from tkinter import filedialog, messagebox
import pandas as pd
import sqlite3

from config import load_config
from tkinter import ttk as ttks
import ttkbootstrap as ttk

def show_guias(frame, tab_to_show, width, height):
    config = load_config()
    db_path = config['db_path']  # type: ignore
    
    def focus_tab(tab):
        tab.select(tab_to_show)    
    def read_xls_file():
        # Read the Excel file into a DataFrame
        file_path = filedialog.askopenfilename(filetypes=[("Archivo excel", "*.xlsx")])
        df_excel = pd.read_excel(file_path)
        df = df_excel.copy()

        # Rest of the code remains the same
        df.drop(df.index[0], axis=0, inplace=True)
        df['Numero guia'] = df['Numero guia'].apply(lambda x: re.sub(r'\D', '', str(x)))
        
        df.head()

        # Create a connection to the database
        connection = sqlite3.connect(db_path)
        df.columns = ["estado","numero_guia","fecha_de_asignacion","remitente","destino","destinatario","direccion_de_entrega","fecha_maxima_de_entrega","unidades","peso_Kg","volumen_m3","valor_declarado_(COP)","fecha_entrega_reexpedidor","hora_entrega_reexpedidor","ultima_causal","fecha_ultima_causal","balance_RCE","balance_FCE","fd","rd","ruta","telefono"]
        
        df_list = df.values.tolist()
        
        
        try: 
            cursor = connection.cursor()
            #create the query for the update 
            for guia in df_list:
                cursor.execute("INSERT OR REPLACE INTO guias (estado, numero_guia, fecha_de_asignacion, remitente, destino, destinatario, direccion_de_entrega, fecha_maxima_de_entrega, unidades, peso_Kg, volumen_m3, 'valor_declarado_(COP)', fecha_entrega_reexpedidor, hora_entrega_reexpedidor, ultima_causal, fecha_ultima_causal, balance_RCE, balance_FCE, fd, rd, ruta, telefono) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", guia)
            connection.commit()
            rows_affected = cursor.rowcount
            messagebox.showinfo("", "Guias importadas con éxito")
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar las guias {str(e)}")
                    
        finally : connection.close()
    def search_guia(number):
        if not number:
            messagebox.showerror("Error", "Ingrese un número de guía")
            return
        try:   
            connection = sqlite3.connect(db_path)
            # Execute a SQL query to search for the guia number
            query = f'''
                        SELECT DISTINCT guias.estado, guias.numero_guia, guias.fecha_de_asignacion, guias.remitente, guias.destino, 
                        guias.destinatario, guias.direccion_de_entrega, guias.unidades, guias.peso_Kg, guias.volumen_m3, guias.ultima_causal, guias.fecha_ultima_causal, 
                        (guias.balance_RCE + guias.balance_FCE) AS balance_cobro, guias.telefono, 
                        COALESCE (remesas_guias.remesa_id,'SIN REMESA' )AS 'remesa' , 
                        COALESCE (anexos_guias.anexo_id, 'SIN ANEXO') AS 'anexo',
                        COALESCE (facturas_guias.factura_id, 'SIN FACTURA') AS 'factura',
						COALESCE (remesas.conductor, "SIN CONDUCTOR" ) as 'Conductor'
                        FROM guias 
                        LEFT JOIN remesas_guias ON guias.numero_guia = remesas_guias.guia_id
						LEFT JOIN remesas ON remesas.id_remesa= remesas_guias.remesa_id
                        LEFT JOIN anexos_guias ON guias.numero_guia = anexos_guias.guia_id
                        LEFT JOIN facturas_guias ON guias.numero_guia = facturas_guias.guia_id
                        WHERE numero_guia = '{number}'
                        LIMIT 1 
                    '''
            
            result = connection.execute(query)
            data = result.fetchall()
                       
            if not data:
                messagebox.showerror("Error", "No se encontraron resultados para la guía")
            
            frame_searched_guia = ttk.LabelFrame(frame_search_guias, text="Guía Encontrada",)
            frame_searched_guia.grid(row=3, column=0, sticky="swen", padx=10, pady=20,)

            # Create a grid layout for the frame_searched_guia
            # for i in range(6):
                # frame_searched_guia.grid_rowconfigure(i, weight=1)
            frame_searched_guia.grid_columnconfigure(1, weight=1)
            frame_searched_guia.grid_columnconfigure(3, weight=1)
            frame_searched_guia.grid_columnconfigure(5, weight=1)
           

            # Create labels and grid them in the frame_searched_guia
            
            for i, row in enumerate(data):
                # Primera fila de etiquetas y entradas
                ttk.Label(frame_searched_guia, text="Estado:", font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
                entry_estado = ttk.Entry(frame_searched_guia)
                entry_estado.grid(row=i, column=1, sticky="we", padx=10, pady=5)
                entry_estado.insert(0, row[0])
                entry_estado.configure(state="readonly")

                ttk.Label(frame_searched_guia, text="Numero Guia:", font=("Arial", 11)).grid(row=i, column=2, sticky="w", padx=10, pady=5)
                entry_numero_guia = ttk.Entry(frame_searched_guia)
                entry_numero_guia.grid(row=i, column=3, sticky="ew", padx=10, pady=5)
                entry_numero_guia.insert(0, row[1])
                entry_numero_guia.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Fecha de Asignación:", font=("Arial", 11)).grid(row=i, column=4, sticky="w", padx=10, pady=5)
                entry_fecha_asignacion = ttk.Entry(frame_searched_guia)
                entry_fecha_asignacion.grid(row=i, column=5, sticky="ew", padx=10, pady=5)
                entry_fecha_asignacion.insert(0, row[2])
                entry_fecha_asignacion.configure(state="readonly" )

                # Segunda fila de etiquetas y entradas
                ttk.Label(frame_searched_guia, text="Remitente:", font=("Arial", 11)).grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
                entry_remitente = ttk.Entry(frame_searched_guia)
                entry_remitente.grid(row=i+1, column=1, sticky="we", padx=10, pady=5)
                entry_remitente.insert(0, row[3])
                entry_remitente.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Destino:", font=("Arial", 11)).grid(row=i+1, column=2, sticky="w", padx=10, pady=5)
                entry_destino = ttk.Entry(frame_searched_guia)
                entry_destino.grid(row=i+1, column=3, sticky="ew", padx=10, pady=5)
                entry_destino.insert(0, row[4])
                entry_destino.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Destinatario:", font=("Arial", 11)).grid(row=i+1, column=4, sticky="w", padx=10, pady=5)
                entry_destinatario = ttk.Entry(frame_searched_guia)
                entry_destinatario.grid(row=i+1, column=5, sticky="we", padx=10, pady=5)
                entry_destinatario.insert(0, row[5])
                entry_destinatario.configure(state="readonly" )

                # Tercera fila de etiquetas y entradas
                ttk.Label(frame_searched_guia, text="Direccion de Entrega:", font=("Arial", 11)).grid(row=i+2, column=0, sticky="w", padx=10, pady=5)
                entry_direccion_entrega = ttk.Entry(frame_searched_guia)
                entry_direccion_entrega.grid(row=i+2, column=1, sticky="we", padx=10, pady=5)
                entry_direccion_entrega.insert(0, row[6])
                entry_direccion_entrega.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Unidades:", font=("Arial", 11)).grid(row=i+2, column=2, sticky="w", padx=10, pady=5)
                entry_unidades = ttk.Entry(frame_searched_guia)
                entry_unidades.grid(row=i+2, column=3, sticky="we", padx=10, pady=5)
                entry_unidades.insert(0, row[7])
                entry_unidades.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Peso Kg:", font=("Arial", 11)).grid(row=i+2, column=4, sticky="w", padx=10, pady=5)
                entry_peso_kg = ttk.Entry(frame_searched_guia)
                entry_peso_kg.grid(row=i+2, column=5, sticky="we", padx=10, pady=5)
                entry_peso_kg.insert(0, row[8])
                entry_peso_kg.configure(state="readonly" )

                # Cuarta fila de etiquetas y entradas
                ttk.Label(frame_searched_guia, text="Volumen m3:", font=("Arial", 11)).grid(row=i+3, column=0, sticky="w", padx=10, pady=5)
                entry_volumen_m3 = ttk.Entry(frame_searched_guia)
                entry_volumen_m3.grid(row=i+3, column=1, sticky="we", padx=10, pady=5)
                entry_volumen_m3.insert(0, row[9])
                entry_volumen_m3.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Ultima Causal:", font=("Arial", 11)).grid(row=i+3, column=2, sticky="w", padx=10, pady=5)
                entry_ultima_causal = ttk.Entry(frame_searched_guia)
                entry_ultima_causal.grid(row=i+3, column=3, sticky="we", padx=10, pady=5)
                entry_ultima_causal.insert(0, row[10] if len(row) > 10 and row[10] is not None else "")
                entry_ultima_causal.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Fecha Ultima Causal:", font=("Arial", 11)).grid(row=i+3, column=4, sticky="w", padx=10, pady=5)
                entry_fecha_ultima_causal = ttk.Entry(frame_searched_guia)
                entry_fecha_ultima_causal.grid(row=i+3, column=5, sticky="ew", padx=10, pady=5)
                entry_fecha_ultima_causal.insert(0, row[11] if len(row) > 11 and row[11] is not None else "")
                entry_fecha_ultima_causal.configure(state="readonly" )

                # Quinta fila de etiquetas y entradas
                ttk.Label(frame_searched_guia, text="Balance cobro:", font=("Arial", 11)).grid(row=i+4, column=0, sticky="w", padx=10, pady=5)
                entry_balance_cobro = ttk.Entry(frame_searched_guia)
                entry_balance_cobro.grid(row=i+4, column=1, sticky="we", padx=10, pady=5)
                entry_balance_cobro.insert(0, "{:,}".format(row[12]))
                entry_balance_cobro.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Telefono:", font=("Arial", 11)).grid(row=i+4, column=2, sticky="w", padx=10, pady=5)
                entry_telefono = ttk.Entry(frame_searched_guia)
                entry_telefono.grid(row=i+4, column=3, sticky="we", padx=10, pady=5)
                entry_telefono.insert(0, row[13])
                entry_telefono.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Remesa:", font=("Arial", 11)).grid(row=i+4, column=4, sticky="w", padx=10, pady=5)
                entry_remesa = ttk.Entry(frame_searched_guia)
                entry_remesa.grid(row=i+4, column=5, sticky="we", padx=10, pady=5)
                entry_remesa.insert(0, row[14])
                entry_remesa.configure(state="readonly" )

                # Sexta fila de etiquetas y entradas
                ttk.Label(frame_searched_guia, text="Anexo:", font=("Arial", 11)).grid(row=i+5, column=0, sticky="w", padx=10, pady=5)
                entry_anexo = ttk.Entry(frame_searched_guia)
                entry_anexo.grid(row=i+5, column=1, sticky="ew", padx=10, pady=5)
                entry_anexo.insert(0, row[15])
                entry_anexo.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Factura:", font=("Arial", 11)).grid(row=i+5, column=2, sticky="w", padx=10, pady=5)
                entry_factura = ttk.Entry(frame_searched_guia)
                entry_factura.grid(row=i+5, column=3, sticky="we", padx=10, pady=5)
                entry_factura.insert(0, row[16])
                entry_factura.configure(state="readonly" )

                ttk.Label(frame_searched_guia, text="Conductor:", font=("Arial", 11)).grid(row=i+5, column=4, sticky="w", padx=10, pady=5)
                entry_conductor = ttk.Entry(frame_searched_guia)
                entry_conductor.grid(row=i+5, column=5, sticky="we", padx=10, pady=5)
                entry_conductor.insert(0, row[17])
                entry_conductor.configure(state="readonly" )
                
 
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar la guía {str(e)}")
            
      
        connection.close()
        return frame
    def show_all_guias():
        try:
            connection = sqlite3.connect(db_path)            
            query = """
                        SELECT "estado", 
                        "numero_guia", 
                        "fecha_de_asignacion", 
                        "remitente", "destino", 
                        "destinatario", 
                        "direccion_de_entrega", 
                        "unidades", 
                        "peso_Kg", 
                        "volumen_m3", 
                        "valor_declarado_(COP)", 
                        (guias.balance_RCE + guias.balance_FCE) AS balance_cobro, 
                        "telefono"
                        FROM guias
                        ORDER BY "fecha_insercion" DESC
                        LIMIT 150
            """
            result = connection.execute(query)
            if not result:
                messagebox.showerror("Error", "No hay guías registradas")
                return
            data = result.fetchall()
            for i, row in enumerate(data):
                table_all_guias.insert("", "end", values=row)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar con la base de datos {str(e)}")
            return
    
    for widget in frame.winfo_children():
        widget.grid_forget()
    
    tab_guias = ttk.Notebook(frame, width=width, height=height)
    tab_guias.grid(row=0, column=0, sticky="nswe")
    tab_guias.grid_propagate(False)
    tab_guias.columnconfigure(0, weight=1)
    tab_guias.rowconfigure(0, weight=1)
    
    
    ##************************************************************
    ##*******************TAB ADD GUIAS ***************************
    ##************************************************************
    
    frame_add_guias = ttk.Frame(tab_guias,   )
    frame_add_guias.grid(row=0, column=0, padx=0, sticky="snwe" )
    frame_add_guias.grid_columnconfigure(0, weight=1)    
    
    frame_import_all = ttk.LabelFrame(frame_add_guias, text= 'Importar desde excel'  ) 
    frame_import_all.grid(row=0, column=0, sticky='ws', padx=10, pady=10) 
    
    import_button = ttk.Button(frame_import_all, text="Importar", command=read_xls_file,)
    import_button.grid(row=3, column=1, sticky="w", padx=20, pady=10)
    
    ##************************************************************    
    ##******************* ENTRIES GUIA SECTION *******************    
    ##************************************************************    
    
    frame_add_guia = ttk.LabelFrame(frame_add_guias, text="Agregar Guía")
    frame_add_guia.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

# Configuración inicial de las columnas
  
    # Configuración inicial de las columnas

    for i in range(6):
        if i%2 !=0:
            frame_add_guia.grid_columnconfigure(i, weight=1)
    # Primera fila
    ttk.Label(frame_add_guia, text="Numero Guía:", anchor="e").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_numero_guia = ttk.Entry(frame_add_guia)
    entry_numero_guia.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Fecha de Asignación:", anchor="e").grid(row=0, column=2, sticky="w", padx=10, pady=5)
    entry_fecha_asignacion = ttk.Entry(frame_add_guia)
    entry_fecha_asignacion.grid(row=0, column=3, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Peso Kg:", anchor="e").grid(row=0, column=4, sticky="w", padx=10, pady=5)
    entry_peso_kg = ttk.Entry(frame_add_guia)
    entry_peso_kg.grid(row=0, column=5, sticky="ew", padx=10, pady=5)

    # Segunda fila
    ttk.Label(frame_add_guia, text="Hora Entrega Reexpedidor:", anchor="e").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_hora_entrega_reexpedidor = ttk.Entry(frame_add_guia)
    entry_hora_entrega_reexpedidor.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Remitente:", anchor="e").grid(row=1, column=2, sticky="w", padx=10, pady=5)
    entry_remitente = ttk.Entry(frame_add_guia)
    entry_remitente.grid(row=1, column=3, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Destino:", anchor="e").grid(row=1, column=4, sticky="w", padx=10, pady=5)
    entry_destino = ttk.Entry(frame_add_guia)
    entry_destino.grid(row=1, column=5, sticky="ew", padx=10, pady=5)

    # Tercera fila
    ttk.Label(frame_add_guia, text="Volumen m3:", anchor="e").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_volumen_m3 = ttk.Entry(frame_add_guia)
    entry_volumen_m3.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Ultima Causal:", anchor="e").grid(row=2, column=2, sticky="w", padx=10, pady=5)
    entry_ultima_causal = ttk.Entry(frame_add_guia)
    entry_ultima_causal.grid(row=2, column=3, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Destinatario:", anchor="e").grid(row=2, column=4, sticky="w", padx=10, pady=5)
    entry_destinatario = ttk.Entry(frame_add_guia)
    entry_destinatario.grid(row=2, column=5, sticky="ew", padx=10, pady=5)

    # Cuarta fila
    ttk.Label(frame_add_guia, text="Direccion de Entrega:", anchor="e").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_direccion_entrega = ttk.Entry(frame_add_guia)
    entry_direccion_entrega.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Valor Declarado (COP):", anchor="e").grid(row=3, column=2, sticky="w", padx=10, pady=5)
    entry_valor_declarado = ttk.Entry(frame_add_guia)
    entry_valor_declarado.grid(row=3, column=3, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Fecha Ultima Causal:", anchor="e").grid(row=3, column=4, sticky="w", padx=10, pady=5)
    entry_fecha_ultima_causal = ttk.Entry(frame_add_guia)
    entry_fecha_ultima_causal.grid(row=3, column=5, sticky="ew", padx=10, pady=5)

    # Quinta fila
    ttk.Label(frame_add_guia, text="Fecha Maxima de Entrega:", anchor="e").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_fecha_maxima_entrega = ttk.Entry(frame_add_guia)
    entry_fecha_maxima_entrega.grid(row=4, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Unidades:", anchor="e").grid(row=4, column=2, sticky="w", padx=10, pady=5)
    entry_unidades = ttk.Entry(frame_add_guia)
    entry_unidades.grid(row=4, column=3, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Fecha Entrega Reexpedidor:", anchor="e").grid(row=4, column=4, sticky="w", padx=10, pady=5)
    entry_fecha_entrega_reexpedidor = ttk.Entry(frame_add_guia)
    entry_fecha_entrega_reexpedidor.grid(row=4, column=5, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Balance RCE:", anchor="e").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_balance_RCE = ttk.Entry(frame_add_guia)
    entry_balance_RCE.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Balance FCE:", anchor="e").grid(row=5, column=2, sticky="w", padx=10, pady=5)
    entry_balance_FCE = ttk.Entry(frame_add_guia)
    entry_balance_FCE.grid(row=5, column=3, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="FD:", anchor="e").grid(row=5, column=4, sticky="w", padx=10, pady=5)
    entry_fd = ttk.Entry(frame_add_guia)
    entry_fd.grid(row=5, column=5, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="RD:", anchor="e").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_rd = ttk.Entry(frame_add_guia)
    entry_rd.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_add_guia, text="Telefono:", anchor="e").grid(row=6, column=2, sticky="w", padx=10, pady=5)
    entry_telefono = ttk.Entry(frame_add_guia)
    entry_telefono.grid(row=6, column=3, sticky="ew", padx=10, pady=5)

    frame_botones = ttk.Frame(frame_add_guia,   )
    frame_botones.grid(row=7, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)
    frame_botones.grid_columnconfigure(0, weight=1)
    frame_botones.grid_columnconfigure(1, weight=1)
    frame_botones.grid_rowconfigure(0, weight=1)

    btn_save = ttk.Button(frame_botones, text="Guardar", width=15)
    btn_save.grid(row=0, column=0, sticky="e", padx=10, pady=5)

    btn_clean = ttk.Button(frame_botones, text="Limpiar", width=15)
    btn_clean.grid(row=0, column=1, sticky="w", padx=10, pady=5)
    
    tab_guias.add(frame_add_guias, text="Agregar Guias")


    ##************************************************************
    ##*********************** TAB GUIAS **************************
    ##************************************************************
    
    frame_search_guias = ttk.Frame(tab_guias,   )
    frame_search_guias.grid(row=0, column=0, sticky="snwe" )
    frame_search_guias.grid_columnconfigure(0, weight=1)
   
    frame_buscar_guias = ttk.Frame(frame_search_guias,)
    frame_buscar_guias.grid( row=2, column=0, sticky='we', )    
    
    ttk.Label(frame_buscar_guias, text="Buscar Guías", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, padx=10, pady=10 )
    ttk.Label(frame_buscar_guias, text="Ingrese Guía:").grid(row=1, column=0, padx=10, sticky="w")    
   
    entry_search_guia = ttk.Entry(frame_buscar_guias, justify='center')
    entry_search_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10,)
    entry_search_guia.bind("<Return>", lambda event: search_button.invoke())

    search_button = ttk.Button(frame_buscar_guias,text="Buscar", command=lambda: search_guia(entry_search_guia.get().strip()))
    search_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    tab_guias.add(frame_search_guias, text="Buscar Guia",) 
    


    
    ##************************************************************
    ##*****************TAB SHOW ALL GUIAS************************
    ##************************************************************
    
    frame_show_all_guias = ttk.Frame(tab_guias,   )
    frame_show_all_guias.grid(row=0, column=0, padx=0, sticky="wens" )
    frame_show_all_guias.grid_columnconfigure(0, weight=1)
    frame_show_all_guias.grid_rowconfigure(0, weight=1)
    cols = ("estado","numero_guia","fecha_de_asignacion","remitente","destino","destinatario","direccion_de_entrega","unidades","peso_Kg","volumen_m3","valor_declarado_(COP)","balance_cobro","telefono")
    table_all_guias = ttks.Treeview(frame_show_all_guias, columns=cols, style="Custom.Treeview")
    table_all_guias.grid(row=0, column=0, sticky="snwe")
    
    vscrollbar = ttk.Scrollbar(frame_show_all_guias, bootstyle = 'primary-round', orient="vertical", command=table_all_guias.yview) # type: ignore
    vscrollbar.grid(row=0, column=1, sticky='ns')
    table_all_guias.configure(yscrollcommand=vscrollbar.set)
    
    hscrollbar = ttk.Scrollbar(frame_show_all_guias, bootstyle = 'primary-round', orient="horizontal", command=table_all_guias.xview) # type: ignore
    hscrollbar.grid(row=2, column=0, sticky='sew', pady=10 )
    table_all_guias.configure(xscrollcommand=hscrollbar.set)

    
    for col in cols:
        table_all_guias.heading(col, text=col)
        table_all_guias.column(col, stretch=False, anchor="center")
    table_all_guias.column("#0", width=0, stretch=False, anchor="center",)
    table_all_guias.column("#8", width=70, stretch=False, anchor="center")
    table_all_guias.column("#9", width=70, stretch=False, anchor="center")
    table_all_guias.column("#10", width=70, stretch=False, anchor="center")
    
    show_all_guias()
    tab_guias.add(frame_show_all_guias, text="Mostrar Guias")
  
    focus_tab(tab_guias)