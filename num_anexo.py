import PyPDF2
import re

def extraer_numero_desde_pdf(pdf_path):
  # Abrir el archivo PDF en modo de lectura binaria
  with open(pdf_path, 'rb') as file:
    # Crear un objeto PDFReader
    pdf_reader = PyPDF2.PdfReader(file)
      
    # Extraer texto de la primera página del PDF
    texto = pdf_reader.pages[0].extract_text()
        
    # Cerrar el archivo
    file.close()

    # Utilizar expresiones regulares para encontrar el número deseado    
    patron_numero = r'Documento No: (\d+)' 
    resultado = re.search(patron_numero, texto)

    if resultado:
        numero = resultado.group(1)
        return numero
    else:
        return None

# Ruta al archivo PDF
pdf_path = '719624 17-02-2024.pdf'

# Llamar a la función para extraer el número
numero_extraido = extraer_numero_desde_pdf(pdf_path)

if numero_extraido:
  print("El número extraído es:", numero_extraido)
else:
  print("No se pudo encontrar el número en el PDF.")