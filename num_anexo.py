import PyPDF2
import re

def extraer_numero_desde_pdf(pdf_path):
  # Abrir el archivo PDF en modo de lectura binaria
  with open(pdf_path, 'rb') as file:
    # Crear un objeto PDFReader
    pdf_reader = PyPDF2.PdfReader(file)
      
    # Extraer texto del PDF
    texto = ""
    for page in pdf_reader.pages:
      texto += page.extract_text()
            
      # Cerrar el archivo
    file.close()

    # Utilizar expresiones regulares para encontrar el número deseado
    # Aquí puedes ajustar el patrón según el formato de tu número
    patron_numero = r'Documento No: (\d+)' # Por ejemplo, buscamos un texto que diga "Número: " seguido de uno o más dígitos
    resultado = re.search(patron_numero, texto)

    if resultado:
        numero = resultado.group(1)
        return numero
    else:
        return None

# Ruta al archivo PDF
pdf_path = 'anexo2024_1.pdf'

# Llamar a la función para extraer el número
numero_extraido = extraer_numero_desde_pdf(pdf_path)

if numero_extraido:
    print("El número extraído es:", numero_extraido)
else:
    print("No se pudo encontrar el número en el PDF.")