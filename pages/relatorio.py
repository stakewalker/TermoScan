from fpdf import FPDF

nome_sala = "Sala de Condimentos"

class PDFReport(FPDF):
    def cabecalho(self):
        # Inserir a logo da empresa e título personalizado
        self.image('assets/logo.png', 10, 8, 33)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Relatório de Temperaturas", 0, 1, "C")
        self.cell(0, 5, nome_sala, 0, 1, "C")

    # def rodape(self):
    #     self.set_y(-15)
    #     self.set_font("Arial", "I", 8)
    #     self.cell(0, 10, "Página %s" % self.page_no(), 0, 0, "C")

def gerar_relatorio(caminho_arquivo, imagens, descricoes):
    pdf = PDFReport()
    pdf.add_page()
    pdf.cabecalho()

    # Adicione imagens dos gráficos com descrição
    for caminho_img, descricao in zip(imagens, descricoes):
        # Adicione imagem à posição específica na página
        pdf.image(caminho_img, x=20, y=pdf.get_y() + 5, w=160)

        # Posição do texto de descrição (abaixo da imagem)
        pdf.set_xy(20, pdf.get_y() + 55)  # Ajustar altura (X e Y)
        # Adicione texto de descrição à célula multi-linha
        pdf.multi_cell(160, 5, descricao)

        # Quebra de linha entre as imagens e descrições
        pdf.ln(5)  # Ajuste conforme necessário

    # pdf.rodape()  # Use the overridden method
    pdf.output(caminho_arquivo)

# Exemplo de uso
imagens = [
    'assets/temp/grafico_3m.png',
    'assets/temp/grafico_1m.png',
    'assets/temp/grafico_1w.png',
]
descricoes = [
    'Esta é a descrição escrita pelo usuário, representando a temperatura dos últimos 3 meses.',
    'Aqui está a descrição do segundo gráfico, mostrando a variação de temperatura ao longo deste mês.',
    'Descrição do terceiro gráfico, ilustrando a temperatura destos últimos 7 dias (uma semana).'
]

gerar_relatorio("relatorio_temperaturas.pdf", imagens, descricoes)
