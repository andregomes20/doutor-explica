import flet as ft
import requests
import os
from gtts import gTTS
from fpdf import FPDF

# Pega o seu token hf_jZl... que você configurou no Render
HF_TOKEN = os.getenv("HF_TOKEN")
# Modelo Llama-3 (Gratuito e muito inteligente)
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

def main(page: ft.Page):
    page.title = "Doutor Explica Grátis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.padding = 20
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE_700)

    # Função para conversar com a IA do Hugging Face
    def consultar_ia(texto_medico):
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        # Comando para a IA agir como médico
        prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nVocê é um médico muito didático. Explique os termos médicos de forma simples e acolhedora para um paciente leigo.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nExplique o seguinte laudo: {texto_medico}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 500, "temperature": 0.7}
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            output = response.json()
            # Pega apenas a resposta da IA, ignorando o comando inicial
            texto_completo = output[0]['generated_text']
            return texto_completo.split("assistant")[-1].strip()
        except Exception as e:
            return f"A IA está processando... Tente novamente em alguns segundos. (Erro: {e})"

    # --- Funções Extras ---
    def salvar_pdf(e):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=txt_resultado.value.encode('latin-1', 'replace').decode('latin-1'))
        pdf.output("explicacao_medica.pdf")
        page.snack_bar = ft.SnackBar(ft.Text("PDF gerado com sucesso!")); page.snack_bar.open = True; page.update()

    def ouvir_audio(e):
        tts = gTTS(text=txt_resultado.value, lang='pt-br')
        tts.save("audio.mp3")
        page.snack_bar = ft.SnackBar(ft.Text("Áudio pronto para ouvir!")); page.snack_bar.open = True; page.update()

    def traduzir_clique(e):
        if not txt_entrada.value: return
        progresso.visible = True
        btn_acao.disabled = True
        page.update()

        txt_resultado.value = consultar_ia(txt_entrada.value)
        
        progresso.visible = False
        btn_acao.disabled = False
        botoes_baixar.visible = True
        page.update()

    # --- Layout da Tela ---
    header = ft.Column([
        ft.Icon(ft.icons.HEALTH_AND_SAFETY, color=ft.colors.BLUE_700, size=60),
        ft.Text("Doutor Explica", size=32, weight="bold"),
        ft.Text("Seu tradutor de saúde gratuito", italic=True, color=ft.colors.GREY_600),
    ], horizontal_alignment="center")

    txt_entrada = ft.TextField(
        label="Cole aqui o texto do seu exame",
        multiline=True, min_lines=4, border_radius=15
    )

    btn_acao = ft.ElevatedButton(
        "Traduzir para Linguagem Simples",
        icon=ft.icons.AUTO_AWESOME,
        on_click=traduzir_clique,
        style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE)
    )

    progresso = ft.ProgressBar(visible=False, color="blue")
    txt_resultado = ft.Text("", size=16, color=ft.colors.BLACK)
    
    botoes_baixar = ft.Row([
        ft.IconButton(ft.icons.PICTURE_AS_PDF, on_click=salvar_pdf, tooltip="Salvar PDF"),
        ft.IconButton(ft.icons.VOLUME_UP, on_click=ouvir_audio, tooltip="Ouvir Áudio"),
    ], alignment="center", visible=False)

    page.add(
        ft.Column([
            header,
            txt_entrada,
            ft.Center(btn_acao),
            progresso,
            ft.Divider(),
            ft.Container(content=txt_resultado, padding=10),
            botoes_baixar,
            ft.Text("Este app não substitui o médico.", size=10, color="red")
        ], spacing=20, horizontal_alignment="center")
    )

ft.app(target=main)
