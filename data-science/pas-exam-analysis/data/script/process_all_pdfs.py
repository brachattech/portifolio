import os
import PyPDF2

# O ponto (.) significa "a pasta atual"
pdf_folder = '.'

# Define o nome do arquivo de saída na pasta atual
output_txt_file = 'combined_text.txt'

def combine_pdfs_to_text(folder_path, output_path):
    combined_text = ""
    # Itera sobre todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processando arquivo: {filename}")
            try:
                # Tenta abrir o PDF
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    # Extrai o texto de cada página
                    for page_num in range(num_pages):
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        if text:
                            combined_text += text + "\n"
            except Exception as e:
                print(f"❌ Erro ao ler {filename}: {e}")

    # Salva o texto combinado em um único arquivo
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(combined_text)
    
    print("\n✅ Concluído! O texto de todos os PDFs foi salvo em 'combined_text.txt'")

if __name__ == "__main__":
    if not os.path.exists(pdf_folder):
        print(f"❌ Erro: A pasta '{pdf_folder}' não foi encontrada.")
        print("Certifique-se de que a pasta existe e contém os seus arquivos PDF.")
    else:
        combine_pdfs_to_text(pdf_folder, output_txt_file)
