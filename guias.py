import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import sqlite3
from sqlite3 import IntegrityError
import config

# define ui guias module
def show_guias(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()

    # Read the CSV file into a DataFrame
    def read_xls_file():
        # Read the Excel file into a DataFrame
        file_path = filedialog.askopenfilename(filetypes=[("Archivo excel", "*.xlsx")])
        df_excel = pd.read_excel(file_path)
        df = df_excel.copy()

        # Rest of the code remains the same
        df.drop(df.index[0], axis=0, inplace=True)
        df['Numero guia'] = df['Numero guia'].apply(lambda x: re.sub(r'\D', '', str(x)))
        # df.iloc[:, 1] = df.iloc[:, 1].str[3:]
        df.head()

        # Create a connection to the database
        connection = sqlite3.connect(config.db_path)
        # Insert the DataFrame records into the 'test' table in the database
        df.columns = ["estado","numero_guia","fecha_de_asignacion","remitente","destino","destinatario","direccion_de_entrega","fecha_maxima_de_entrega","unidades","peso_Kg","volumen_m3","valor_declarado_(COP)","fecha_entrega_reexpedidor","hora_entrega_reexpedidor","ultima_causal","fecha_ultima_causal","balance_RCE","balance_FCE","fd","rd","ruta","telefono"]
        for i in range(len(df)):
            try:
                df.iloc[i:i+1].to_sql("guias", connection, if_exists='append', index=False, method='multi')
            except IntegrityError:
                pass #or any other action   
            
        messagebox.showinfo("", "Guias importadas con éxito")
        connection.close()

    def search_guias(number):
        if not number:
            messagebox.showerror("Error", "Ingrese un número de guía")
            return
        try:   
            connection = sqlite3.connect(config.db_path)
            # Execute a SQL query to search for the guia number
            query = f'''
                        SELECT DISTINCT guias.estado, guias.numero_guia, guias.fecha_de_asignacion, guias.remitente, guias.destino, 
                        guias.destinatario, guias.direccion_de_entrega, guias.unidades, guias.peso_Kg, guias.volumen_m3, guias.ultima_causal, guias.fecha_ultima_causal, 
                        (guias.balance_RCE + guias.balance_FCE) AS balance_cobro, guias.telefono, 
                        COALESCE (remesas_guias.remesa_id,'SIN REMESA' )AS 'remesa' , 
                        COALESCE (anexos_guias.anexo_id, 'SIN ANEXO') AS 'anexo',
                        COALESCE ( facturas_guias.factura_id, 'SIN FACTURA') AS 'factura'
                        FROM guias 
                        LEFT JOIN remesas_guias ON guias.numero_guia = remesas_guias.guia_id
                        LEFT JOIN anexos_guias ON guias.numero_guia = anexos_guias.guia_id
                        JOIN facturas_guias ON guias.numero_guia = facturas_guias.guia_id
                        WHERE numero_guia = '{number}'
                    '''
            
            result = connection.execute(query)
            data = result.fetchall()
                       
            if not data:
                messagebox.showerror("Error", "No se encontraron resultados para la guía")

            for i, row in enumerate(data):
                ttk.Label(frame_searched_guia, text="Estado:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[0], width=30, font=("Arial", 11)).grid(row=0, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Numero Guia:", font=("Arial", 11)).grid(row=0, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[1], width=30, font=("Arial", 11)).grid(row=0, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Fecha de Asignación:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[2], width=30, font=("Arial", 11)).grid(row=1, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Remitente:", font=("Arial", 11)).grid(row=1, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[3], width=30, font=("Arial", 11)).grid(row=1, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Destino:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[4], width=30, font=("Arial", 11)).grid(row=2, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Destinatario:", font=("Arial", 11)).grid(row=2, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[5], width=30, font=("Arial", 11)).grid(row=2, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Direccion de Entrega:", font=("Arial", 11)).grid(row=3, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[6], width=30, font=("Arial", 11)).grid(row=3, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Unidades:", font=("Arial", 11)).grid(row=3, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[7], width=30, font=("Arial", 11)).grid(row=3, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Peso Kg:", font=("Arial", 11)).grid(row=4, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[8], width=30, font=("Arial", 11)).grid(row=4, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Volumen m3:", font=("Arial", 11)).grid(row=4, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[9], width=30, font=("Arial", 11)).grid(row=4, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Ultima Causal:", font=("Arial", 11)).grid(row=5, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[10], width=30, font=("Arial", 11)).grid(row=5, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Fecha Ultima Causal:", font=("Arial", 11)).grid(row=5, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[11], width=30, font=("Arial", 11)).grid(row=5, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Balance Cobro:", font=("Arial", 11)).grid(row=6, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[12], width=30, font=("Arial", 11)).grid(row=6, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Telefono:", font=("Arial", 11)).grid(row=6, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[13], width=30, font=("Arial", 11)).grid(row=6, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Remesa:", font=("Arial", 11)).grid(row=7, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[14], width=30, font=("Arial", 11)).grid(row=7, column=1, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Anexo:", font=("Arial", 11)).grid(row=7, column=2, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[15], width=30, font=("Arial", 11)).grid(row=7, column=3, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text="Factura:", font=("Arial", 11)).grid(row=8, column=0, sticky="w", padx=10, pady=5,)
                ttk.Label(frame_searched_guia, text=row[16], width=30, font=("Arial", 11)).grid(row=8, column=1, sticky="w", padx=10, pady=5,)
        except:
            messagebox.showerror("Error", "Se ha producido un error al buscar la guía")
            
      
        connection.close()
        return frame
   
    frame_guias = ttk.LabelFrame(frame, relief="groove", text="Guias", width=1200, height=700,)
    frame_guias.grid(row=0, column=0, padx=0, pady=10, sticky="nwe" )
    frame_guias.grid_columnconfigure(0, weight=1)
    # frame_guias.grid_propagate(False)

    # Process the query result
    frame_searched_guia = ttk.LabelFrame(frame_guias, text="Guía Encontrada",)
    frame_searched_guia.grid(row=3, column=0, sticky="nwe",  pady=10)
  
    frame_buscar_guias = ttk.LabelFrame(frame_guias, )
    frame_buscar_guias.grid( row=0, column=0, sticky='we', padx=10, pady=10)
    
    ttk.Label(frame_buscar_guias, text="Buscar Guías", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10 )
    ttk.Label(frame_buscar_guias, text="Ingrese Guía:").grid(row=1, column=0, sticky="w")    

    entry_search_guia = ttk.Entry(frame_buscar_guias)
    entry_search_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10,)
    entry_search_guia.bind("<Return>", lambda event: search_button.invoke())

    search_button = ttk.Button(frame_buscar_guias,text="Buscar", command=lambda: search_guias(entry_search_guia.get().strip()))
    search_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    
    # ttk.Label(frame_agregar_guias, text="Agregar Guías", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10 )
    # ttk.Label(frame_agregar_guias, text="Ingrese Guía:").grid(row=1, column=0, sticky="w")
    # entry_add_guia = ttk.Entry(frame_agregar_guias)
    # entry_add_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10)    
    # add_button = ttk.Button(frame_agregar_guias, text="Agregar")
    # add_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    frame_import_all = ttk.Frame(frame_guias, ) 
    frame_import_all.grid(row=2, column=0, sticky='ws', padx=10, pady=10) 
    
    ttk.Label(frame_import_all,  text= 'Importar Guias', font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="w")
    
    import_button = ttk.Button(frame_import_all, text="Importar", command=read_xls_file,)
    import_button.grid(row=3, column=1, sticky="w", padx=10, pady=5)

    ##************************************************************
    ##***********************LIST GUIAS***************************
    ##************************************************************