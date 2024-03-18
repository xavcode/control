import os
import pandas as pd
import pdfplumber
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3
from tkinter import messagebox


def show_destinos(frame):
  for widget in frame.winfo_children():
    widget.grid_forget()
  
  # Connect to the SQLite database
  conn = sqlite3.connect('D:/intermodal/control/control_intermodal.db')

  # Create a label widget for "Destinos"
  label = tk.Label(frame, text="Destinos")
  label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

  # Execute the query to fetch the destinations
  query = "SELECT * FROM destinos"
  df = pd.read_sql_query(query, conn)

  # Create a treeview widget to display the destinations
  table = ttk.Treeview(frame, columns=("id_destino", "destino", "valor"), show="headings")
  table.column("#0", width=0, stretch=False, anchor="center")
  table.column("id_destino", width=50, stretch=False, anchor="center")
  table.column("destino", width=150, stretch=False, anchor="center")
  table.column("valor", width=150, stretch=False, anchor="center")
  
  # scrollbar = ttk.Scrollbar(table, orient="horizontal", command=table.yview)
  # table.configure(yscrollcommand=scrollbar.set)
  # scrollbar.grid(row=1, column=5, sticky="")
  
  table.heading("id_destino", text="ID")
  table.heading("destino", text="Destino")
  table.heading("valor", text="Valor")
  

  

  # Insert the data into the table
  for index, row in df.iterrows():
    table.insert("", "end", text='', values=tuple(row)) # type: ignore

  # Display the table
  table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

  # Close the database connection
  conn.close()
