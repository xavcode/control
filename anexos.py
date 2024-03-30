import os
import pandas as pd
import pdfplumber
import tkinter as tk
from tkinter import ttk, filedialog,messagebox
import PyPDF2
import re
import sqlite3

import config



def show_anexos(frame):
    # create main frame for anexos
    for widget in frame.winfo_children():
        widget.grid_forget()

    frame_anexos = ttk.LabelFrame(frame,  text="Anexos")
    frame_anexos.grid(row=0, column=0, sticky='', pady=10)
    # frame_anexos.grid_propagate(False)
    # frame_anexos.grid_rowconfigure(0, weight=1)
    # frame_anexos.grid_columnconfigure(0, weight=1)
    
    def extract_table():
      full_table = []
      file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
      if file_path:
        #for get the number of the anexo
        with open(file_path, 'rb') as file:
          #extraer el numero del anexo con re
          pdf_reader = PyPDF2.PdfReader(file)
          text = pdf_reader.pages[0].extract_text()               
          number_anexo = r'Documento No: (\d+)' 
          date_anexo = r'Fecha: (\d{4}-\d{2}-\d{2})'  # Updated regular expression pattern for date
          result_number = re.search(number_anexo, text)
          result_date = re.search(date_anexo, text)
          if result_number:
            numero_documento = result_number.group(1)
            entry_num_anexo.insert(0, numero_documento)
          if result_date:
            entry_fecha_anexo.insert(0, result_date.group(1))
            
           
          
          file.close()
          
        with pdfplumber.open(file_path) as pdf:          
          # Iterar sobre las páginas del PDF          
          total_pages = len(pdf.pages)
          last_page = total_pages - 1
          text = pdf.pages[last_page].extract_text()
          # print(text)
          for page in pdf.pages:
            # Extraer todas las tablas de la página
            tables = page.extract_tables()
            # Iterar sobre las tablas extraídas
            for table in tables:
              # Omitir la primera fila (suponiendo que es la fila de encabezados)
              table_data = table[2:]  # Comenzar desde la segunda fila
              # Agregar las filas de la tabla (sin los encabezados) a la lista
              full_table.extend(table_data)

        df = pd.DataFrame(full_table)
        df = df.dropna(axis="columns", how="all")
        df.columns = ["GUIA","PRODUCTO","DESTINO","UDS","PESO","FTE FIJO","FTE VARIABLE","FTE TOTAL","TIPO",]
        # set names to columns
        df[["UDS", "FTE FIJO", "PESO", "FTE VARIABLE", "FTE TOTAL"]] = df[["UDS", "FTE FIJO",  "PESO", "FTE VARIABLE", "FTE TOTAL"]].apply(pd.to_numeric, errors="coerce")
        df[["FTE FIJO", "FTE VARIABLE", "FTE TOTAL"]] = (df[["FTE FIJO", "FTE VARIABLE", "FTE TOTAL"]] * 1000)
        df[["FTE FIJO", "FTE TOTAL", "FTE VARIABLE"]] = df[["FTE FIJO", "FTE TOTAL", "FTE VARIABLE"]].astype(int)
                      
        # Insert data into the treeview
        for index, row in df.iterrows():
          tree.insert("", int(index), values=row.tolist()) # type: ignore

        sum_items = int(df["UDS"].sum())
        sum_fte = int((df["FTE TOTAL"]).sum())
        # sum_kg = (df["PESO"]).sum()
        num_records = int(len(df))
        
        entry_total_unidades.insert(0, str(sum_items))
        entry_total_guias.insert(0, str(num_records))
        entry_total_fte.insert(0, str(sum_fte))
        
        
        # Add sum_items and sum_fte to the dataframe
        df.loc["Blanck Space"] = ["", "", "", "", "", "", "", "", ""]
        df.loc["Sum Items"] = ["", "", "", "", "", "", "", "TOTAL GUIAS", num_records]
        df.loc["Total Unidades"] = ["", "", "", "", "", "", "", "TOTAL UNIDADES", sum_items]
        df.loc["Sum Values"] = ["", "", "", "", "", "", "", "VALOR TOTAL", sum_fte ]
      
      return df
    def export_pdf():
      export = extract_table()      
      file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
      if file_path:
        export.to_excel(file_path, index=False)
        os.startfile(file_path)
    
     # Create a Treeview widget
    def save_anexo():
      id_anexo = entry_num_anexo.get()
      fecha = entry_fecha_anexo.get()
      total_unidades = entry_total_unidades.get()
      total_guias = entry_total_guias.get()
      fte_total = entry_total_fte.get()
      
      
      # rows_to_insert = []
      # for row in tree.get_children():
      #   rows_to_insert.append((tree.item(row)["values"][0], tree.item(row)["values"][7], tree.item(row)["values"][8]))
        
      # connection = sqlite3.connect(config.db_path)
      # query_anexos = f"INSERT INTO anexos_guias (anexo_id, guia_id, valor, tipo) VALUES "
      # for i in range(len(rows_to_insert)):
      #   row = rows_to_insert[i]
      #   query_anexos += f"('{id_anexo}', '{row[0]}', {row[1]}, '{row[2]}')"
      #   if i != len(rows_to_insert) - 1:
      #       query_anexos += ", "  # Agregamos una coma para separar los valores
      #   else:
      #       query_anexos += ";"  # Agregamos un punto y coma al final de la consulta        
      # print(query_anexos)
        
      
      try:
        connection = sqlite3.connect(config.db_path)
        query = f"INSERT INTO anexos (id_anexo, fecha_anexo, total_unidades, total_guias, fte_total) VALUES ('{id_anexo}', '{fecha}', '{(int(total_unidades))}', '{int(total_guias)}', '{(fte_total)}');"
        
        
                
        
        
        result = connection.execute(query)
        connection.commit()
        
        if result:
          messagebox.showinfo("", "Anexo guardado con éxito")
              
      except Exception as e:
        messagebox.showerror("", f"Error al guardar el anexo: {str(e)}")
      connection.close()
    


    tree = ttk.Treeview(frame_anexos, height=20, show='headings', selectmode="browse")
    tree.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
    
    # Define columns
    tree["columns"] = ("GUIA","PRODUCTO","DESTINO","UDS","PESO","FTE FIJO","FTE VARIABLE","FTE TOTAL","TIPO")
    
    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("GUIA", width=100, anchor='center')
    tree.column("PRODUCTO", width=100, anchor='center')
    tree.column("DESTINO", width=100, anchor='center')
    tree.column("UDS", width=50, anchor='center')
    tree.column("PESO", width=50, anchor='center')
    tree.column("FTE FIJO", width=100, anchor='center')
    tree.column("FTE VARIABLE", width=100, anchor='center')
    tree.column("FTE TOTAL", width=100, anchor='center')
    tree.column("TIPO", width=100, anchor='center')

    # Create headings
    tree.heading("#0", text="")
    tree.heading("GUIA", text="GUIA")
    tree.heading("PRODUCTO", text="PRODUCTO")
    tree.heading("DESTINO", text="DESTINO")
    tree.heading("UDS", text="UDS")
    tree.heading("PESO", text="KG")
    tree.heading("FTE FIJO", text="FTE FIJO")
    tree.heading("FTE VARIABLE", text="FTE VARIABLE")
    tree.heading("FTE TOTAL", text="FTE TOTAL")
    tree.heading("TIPO", text="TIPO")

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(frame_anexos, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=4, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)
    
    frame_add_anexos = ttk.Frame(frame_anexos)
    frame_add_anexos.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='se')
    
    # Button to add anexos
    btn_save_anexos = ttk.Button(frame_add_anexos, text="Guardar Anexo", command=lambda: save_anexo())
    btn_save_anexos.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    
    
    btn_add_anexos = ttk.Button(frame_add_anexos, text="Seleccionar Anexo", command=lambda: extract_table())
    btn_add_anexos.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    
    btn_export_anexos = ttk.Button(frame_add_anexos, text="Exportar excel", command=lambda: export_pdf())
    btn_export_anexos.grid(row=0, column=3, padx=10, pady=5, sticky="e")
    
    label__fecha_anexo = ttk.Label(frame_anexos, text="Fecha Anexo:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
    entry_fecha_anexo = ttk.Entry(frame_anexos)
    entry_fecha_anexo.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    entry_fecha_anexo.config(justify="center")
    
    label_num_anexo = ttk.Label(frame_anexos, text="Numero de Anexo:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_num_anexo = ttk.Entry(frame_anexos)
    entry_num_anexo.grid(row=0, column=1, padx=10, pady=5, sticky="ew", )
    entry_num_anexo.config(justify="center")
    
    label_total_guias = ttk.Label(frame_anexos, text="Total Guias:").grid(row=4, column=2, padx=10, pady=5, sticky="e")
    entry_total_guias = ttk.Entry(frame_anexos)
    entry_total_guias.grid(row=4, column=3, padx=10, pady=5, sticky="ew")
    entry_total_guias.config(justify="center")
    
    label_total_unidades = ttk.Label(frame_anexos, text="Total Unidades:").grid(row=5, column=2, padx=10, pady=5, sticky="e")
    entry_total_unidades = ttk.Entry(frame_anexos)
    entry_total_unidades.grid(row=5, column=3, padx=10, pady=5, sticky="ew")
    entry_total_unidades.config(justify="center")
    
    label_total_fte = ttk.Label(frame_anexos, text="Total FTE:").grid(row=6, column=2, padx=10, pady=5, sticky="e")
    entry_total_fte = ttk.Entry(frame_anexos)
    entry_total_fte.grid(row=6, column=3, padx=10, pady=5, sticky="ew")
    entry_total_fte.config(justify="center")
    
    return frame_anexos 