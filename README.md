📑 Leitor de NF-e XML

Este script lê arquivos XML de NFC-e/NF-e dentro de um .zip ou .rar, ignora notas canceladas e gera um relatório resumido por mês com:

📌 Quantidade de notas

💰 Valor total

🔢 Nota inicial e final

Exemplo de saída:

📅 Notas emitidas por mês:
- 06/2025: 2 nota(s) — R$ 126,00
  Nota início: 10  |  Nota final: 30
- 07/2025: 652 nota(s) — R$ 36.695,22
  Nota início: 1001  |  Nota final: 2310

🚀 Como usar
1. Pré-requisitos

Python 3.8+
 instalado

Instale as bibliotecas necessárias:

pip install rarfile


⚠️ Para arquivos .rar, é necessário ter o unrar instalado no sistema:

Windows: baixe em Rarlab

Linux:

sudo apt-get install unrar

2. Baixe o projeto
git clone https://github.com/SEU_USUARIO/nfe-relatorio.git
cd nfe-relatorio

3. Coloque suas notas

Coloque o arquivo .zip ou .rar com os XMLs na pasta do projeto.
Exemplo: notas.rar

4. Rode o script
python main.py

5. Veja o relatório

O programa exibirá o relatório direto no terminal, por exemplo:

📅 Notas emitidas por mês:
- 06/2025: 2 nota(s) — R$ 126,00
  Nota início: 10  |  Nota final: 30
- 07/2025: 652 nota(s) — R$ 36.695,22
  Nota início: 1001  |  Nota final: 2310


👉 Pronto! Relatório gerado de forma simples e rápida 🎉
