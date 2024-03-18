import os
import pandas as pd
import pdfplumber
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3
from tkinter import messagebox


def show_anexos(frame):
    # create main frame for anexos
    for widget in frame.winfo_children():
        widget.grid_forget()

    frame_anexos = tk.Frame(frame, bd=2, relief="groove", width=600, height=400)
    frame_anexos.grid(row=0, column=1, pady=10)
    
    def extract_table():
      full_table = []
      file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
      if file_path:
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
          # print(full_table)

        df = pd.DataFrame(full_table)

        df = df.dropna(axis="columns", how="all")
        df.columns = ["GUIA","PRODUCTO","DESTINO","UDS","PESO","FTE FIJO","FTE VARIABLE","FTE TOTAL","TIPO",]

        # set names to columns
        df[["UDS", "FTE FIJO", "PESO", "FTE VARIABLE", "FTE TOTAL"]] = df[["UDS", "FTE FIJO",  "PESO", "FTE VARIABLE", "FTE TOTAL"]].apply(pd.to_numeric, errors="coerce")

        df[["FTE FIJO", "FTE VARIABLE", "FTE TOTAL"]] = (df[["FTE FIJO", "FTE VARIABLE", "FTE TOTAL"]] * 1000)       
       
              
        # Insert data into the treeview
        for index, row in df.iterrows():
          tree.insert("", int(index), values=row.tolist()) # type: ignore       

        sum_items = df["UDS"].sum()
        sum_fte = (df["FTE TOTAL"]).sum()
        sum_kg = (df["PESO"]).sum()
        num_records = len(df)
        
        # Add sum_items and sum_fte to the dataframe
        df.loc["Blanck Space"] = ["", "", "", "", "", "", "", "", ""]
        df.loc["Sum Items"] = ["", "", "", "", "", "", "", "TOTAL GUIAS", num_records]
        df.loc["Total Unidades"] = ["", "", "", "", "", "", "", "TOTAL UNIDADES", sum_items]
        df.loc["Sum Values"] = ["", "", "", "", "", "", "", "VALOR TOTAL", sum_fte ]

        # print(df)
      return df
    
    def export_pdf():
      export = extract_table()      
      file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
      if file_path:
        export.to_excel(file_path, index=False)
        os.startfile(file_path)
      print(export)
      
    frame_add_anexos = tk.Frame(frame_anexos)
    frame_add_anexos.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
    
    # Button to add anexos
    btn_add_anexos = tk.Button(frame_add_anexos, text="Agregar Anexos", command=lambda: extract_table())
    btn_add_anexos.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    btn_export_anexos = tk.Button(frame_add_anexos, text="Exportar excel", command=lambda: export_pdf())
    btn_export_anexos.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
     # Create a Treeview widget
    tree = ttk.Treeview(frame_anexos, selectmode="browse")

    # Define columns
    tree["columns"] = ("GUIA","PRODUCTO","DESTINO","UDS","PESO","FTE FIJO","FTE VARIABLE","FTE TOTAL","TIPO")

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("GUIA", width=100, anchor='center')
    tree.column("PRODUCTO", width=100, anchor='center')
    tree.column("DESTINO", width=100, anchor='center')
    tree.column("UDS", width=100, anchor='center')
    tree.column("PESO", width=100, anchor='center')
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
    tree.heading("PESO", text="PESO")
    tree.heading("FTE FIJO", text="FTE FIJO")
    tree.heading("FTE VARIABLE", text="FTE VARIABLE")
    tree.heading("FTE TOTAL", text="FTE TOTAL")
    tree.heading("TIPO", text="TIPO")

  # Add the treeview to the frame
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(frame_anexos, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)
  
    return frame_anexos    
      # sum_fte = sum_fte.round(2)
      # df.to_csv("output.csv", index=False)

      # connection = sqlite3.connect("d:/intermodal/contro/intermodal_control.db")
      # df.to_sql("Anexos", connection, if_exists="append", index=False) 
      # D:\intermodal\control
      # # print(sum_fte)
      # connection.close()



