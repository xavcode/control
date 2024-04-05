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
    
        connection = sqlite3.connect(config.db_path)
        # Execute a SQL query to search for the guia number
        query = f'''
                    SELECT guias.estado, guias.numero_guia, guias.fecha_de_asignacion, guias.remitente, guias.destino, 
                    guias.destinatario, guias.direccion_de_entrega, guias.unidades, guias.peso_Kg, guias.volumen_m3, guias.ultima_causal, guias.fecha_ultima_causal, 
                    (guias.balance_RCE + guias.balance_FCE) AS balance_cobro, guias.telefono, 
                    COALESCE (remesas_guias.remesa_id,'SIN REMESA' )AS 'remesa' , 
                    COALESCE (anexos_guias.anexo_id, 'SIN ANEXO') AS 'anexo'
                    FROM guias 
                    LEFT JOIN remesas_guias ON guias.numero_guia = remesas_guias.guia_id
                    LEFT JOIN anexos_guias ON guias.numero_guia = anexos_guias.guia_id
                    WHERE numero_guia = '{number}'
                '''
        
        result = connection.execute(query)

        # Process the query result
        for row in result:
            # Create a new frame for each row
            frame_row = ttk.LabelFrame(frame, )
            frame_row.grid(row=4, column=0, sticky="we", columnspan=2, padx=10, pady=10)

            # Display the data in labels
            ttk.Label(frame_row, text="Estado:").grid(row=0, column=0, sticky="w")
            ttk.Label(frame_row, text=row[0]).grid(row=0, column=1, sticky="w")

            ttk.Label(frame_row, text="Número de Guía:").grid(row=1, column=0, sticky="w")
            ttk.Label(frame_row, text=row[1]).grid(row=1, column=1, sticky="w")

            ttk.Label(frame_row, text="Fecha de Asignación:").grid(row=2, column=0, sticky="w")
            ttk.Label(frame_row, text=row[2]).grid(row=2, column=1, sticky="w")

            ttk.Label(frame_row, text="Remitente:").grid(row=3, column=0, sticky="w")
            ttk.Label(frame_row, text=row[3]).grid(row=3, column=1, sticky="w")

            ttk.Label(frame_row, text="Destino:").grid(row=4, column=0, sticky="w")
            ttk.Label(frame_row, text=row[4]).grid(row=4, column=1, sticky="w")

            ttk.Label(frame_row, text="Destinatario:").grid(row=5, column=0, sticky="w")
            ttk.Label(frame_row, text=row[5]).grid(row=5, column=1, sticky="w")

            ttk.Label(frame_row, text="Dirección de Entrega:").grid(row=6, column=0, sticky="w")
            ttk.Label(frame_row, text=row[6]).grid(row=6, column=1, sticky="w")

            ttk.Label(frame_row, text="Unidades:").grid(row=7, column=0, sticky="w")
            ttk.Label(frame_row, text=row[7]).grid(row=7, column=1, sticky="w")

            ttk.Label(frame_row, text="Peso (Kg):").grid(row=8, column=0, sticky="w")
            ttk.Label(frame_row, text=row[8]).grid(row=8, column=1, sticky="w")

            ttk.Label(frame_row, text="Volumen (m3):").grid(row=9, column=0, sticky="w")
            ttk.Label(frame_row, text=row[9]).grid(row=9, column=1, sticky="w")

            ttk.Label(frame_row, text="Última Causal:").grid(row=10, column=0, sticky="w")
            ttk.Label(frame_row, text=row[10]).grid(row=10, column=1, sticky="w")

            ttk.Label(frame_row, text="Fecha Última Causal:").grid(row=11, column=0, sticky="w")
            ttk.Label(frame_row, text=row[11]).grid(row=11, column=1, sticky="w")
            
            ttk.Label(frame_row, text="Balance de Cobro:").grid(row=12, column=0, sticky="w")
            ttk.Label(frame_row, text=row[12]).grid(row=12, column=1, sticky="w")

            ttk.Label(frame_row, text="Teléfono:").grid(row=13, column=0, sticky="w")
            ttk.Label(frame_row, text=row[13]).grid(row=13, column=1, sticky="w")
            
            ttk.Label(frame_row, text="Remesa:").grid(row=14, column=0, sticky="w")
            ttk.Label(frame_row, text=row[14]).grid(row=14, column=1, sticky="w")
            
            ttk.Label(frame_row, text="Anexo:").grid(row=15, column=0, sticky="w")
            ttk.Label(frame_row, text=row[15]).grid(row=15, column=1, sticky="w")

        # Close the database connection
        connection.close()
        return frame

    def list_all_guias():
        # Create a connection to the database
        connection = sqlite3.connect(config.db_path)
        # Execute a SQL query to fetch all the guias
        #in case that want to show the remesa_id and anexo id_ use this query 
        # ''' 
        #     SELECT guias.estado, guias.numero_guia, guias.fecha_de_asignacion, guias.remitente, guias.destino, 
        #     guias.destinatario, guias.direccion_de_entrega, guias.unidades, guias.peso_Kg, guias.volumen_m3, guias.ultima_causal, guias.fecha_ultima_causal, 
        #     (guias.balance_RCE + guias.balance_FCE) AS balance_cobro, guias.telefono, 
        #     COALESCE (remesas_guias.remesa_id,'SIN REMESA' )AS 'remesa' , 
        #     COALESCE (anexos_guias.anexo_id, 'SIN ANEXO') AS 'anexo'
        #     FROM guias 
        #     LEFT JOIN remesas_guias ON guias.numero_guia = remesas_guias.guia_id
        #     LEFT JOIN anexos_guias ON guias.numero_guia = anexos_guias.guia_id
        #     WHERE numero_guia = '{number}'
        # '''
    
        
        
        query = "SELECT estado, numero_guia, fecha_de_asignacion, remitente, destino, destinatario, direccion_de_entrega, unidades, peso_Kg, volumen_m3, ultima_causal, fecha_ultima_causal, (balance_RCE + balance_FCE) AS balance_cobro, telefono, strftime('%d %m %Y', fecha_insercion) FROM guias ORDER BY fecha_insercion DESC"
        result = connection.execute(query)
        data = result.fetchall()
        for row in data:
            table.insert("", "end", values=row)
        
        connection.close()
    
    frame_guias = ttk.LabelFrame(frame, relief="groove", text="Guias", width=1200, height=700,)
    frame_guias.grid(row=0, column=0, padx=0, pady=10, sticky="n" )
    frame_guias.grid_propagate(False)
    frame_guias.grid_columnconfigure(0, weight=1)
    frame_guias.grid_columnconfigure(1, weight=1)
    

    frame_buscar_guias = ttk.LabelFrame(frame_guias, )
    frame_buscar_guias.grid( row=0, column=0, sticky='we', padx=10, pady=10)
    
    ttk.Label(frame_buscar_guias, text="Buscar Guías", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10 )
    ttk.Label(frame_buscar_guias, text="Ingrese Guía:").grid(row=1, column=0, sticky="w")    

    entry_search_guia = ttk.Entry(frame_buscar_guias)
    entry_search_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10,)
    entry_search_guia.bind("<Return>", lambda event: search_button.invoke())

    search_button = ttk.Button(frame_buscar_guias,text="Buscar", command=lambda: search_guias(entry_search_guia.get()))
    search_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    frame_agregar_guias = ttk.LabelFrame(frame_guias, )
    frame_agregar_guias.grid(row=0, column=1, sticky='we',  padx=10, pady=10)
    
    ttk.Label(frame_agregar_guias, text="Agregar Guías", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10 )
    ttk.Label(frame_agregar_guias, text="Ingrese Guía:").grid(row=1, column=0, sticky="w")
    entry_add_guia = ttk.Entry(frame_agregar_guias)
    entry_add_guia.grid(row=1, column=1, sticky="w", padx=10, pady=10)    
    add_button = ttk.Button(frame_agregar_guias, text="Agregar")
    add_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    frame_import_all = ttk.LabelFrame(frame_guias,  text="Importar Guias", border=2, relief="groove", ) 
    frame_import_all.grid(row=3, column=2, columnspan=2, sticky='s', padx=20, pady=20) 
    import_button = ttk.Button(frame_guias, text="Importar", command=read_xls_file,)
    import_button.grid(row=3, column=1, sticky="e", padx=10, pady=5)

    ##************************************************************
    ##***********************LIST GUIAS***************************
    ##************************************************************


    list_camp = ("Estado", "Numero_guia", "F. Asignacion", "Remitente", "Destino", "Destinatario", "Direccion_de_entrega", "Unidades", "Peso_Kg", "Volumen_m3", "Ultima_causal", "Fecha_ultima_causal", "balance_cobro","Telefono")

    
    table = ttk.Treeview(frame_guias, columns=(list_camp), show="headings", height=15)
    table.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=10)
    table.configure(height=15)
    # table.place(relx=0.1, rely=0.1, relwidth=.9, relheight=.9)
    

    table.column("Estado", width=100, stretch=False, anchor="center")
    table.column("Numero_guia", width=80, stretch=False, anchor="center")
    table.column("F. Asignacion", width=100, stretch=False, anchor="center")
    table.column("Remitente", width=150, stretch=False, anchor="center")
    table.column("Destino", width=100, stretch=False, anchor="center")
    table.column("Destinatario", width=120, stretch=False, anchor="center")
    table.column("Direccion_de_entrega", width=300, stretch=False, anchor="center")
    table.column("Unidades", width=50, stretch=False, anchor="center")
    table.column("Peso_Kg", width=50, stretch=False, anchor="center")
    table.column("Volumen_m3", width=50, stretch=False, anchor="center")
    table.column("Ultima_causal", width=100, stretch=False, anchor="center")
    table.column("Fecha_ultima_causal", width=100, stretch=False, anchor="center")
    table.column("balance_cobro", width=100, stretch=False, anchor="center")    
    table.column("Telefono", width=100, stretch=False, anchor="center")

    
    for camp in list_camp:
        table.heading(camp, text=camp)
    vscrollbar = ttk.Scrollbar(frame_guias, orient="vertical", command=table.yview)
    vscrollbar.grid(row=1, column=3, sticky="ns", pady=15)
    table.configure(yscrollcommand=vscrollbar.set)
    
    hscrollbar = ttk.Scrollbar(frame_guias, orient="horizontal", command=table.xview)
    hscrollbar.grid(row=2, column=0,  columnspan=2, sticky="we")
    table.configure(xscrollcommand=hscrollbar.set)

    
    list_all_guias()