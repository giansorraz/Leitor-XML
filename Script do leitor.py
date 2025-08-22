import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import zipfile
import rarfile

def extrair_arquivos(arquivo):
    pasta_temp = "temp_xml"
    os.makedirs(pasta_temp, exist_ok=True)

    if zipfile.is_zipfile(arquivo):
        with zipfile.ZipFile(arquivo, 'r') as z:
            z.extractall(pasta_temp)
    elif rarfile.is_rarfile(arquivo):
        with rarfile.RarFile(arquivo, 'r') as r:
            r.extractall(pasta_temp)
    else:
        raise ValueError("Formato de arquivo não suportado. Use .zip ou .rar")
    
    return pasta_temp

def ler_xml_nfe(pasta):
    dados_por_mes = defaultdict(lambda: {"quantidade": 0, "valor": 0.0, "notas": []})

    for raiz, _, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            if arquivo.lower().endswith(".xml"):
                caminho_arquivo = os.path.join(raiz, arquivo)
                try:
                    tree = ET.parse(caminho_arquivo)
                    root = tree.getroot()

                    # Namespace
                    ns = {"ns": root.tag.split("}")[0].strip("{")}

                    # Verifica se é cancelada
                    cancelada = root.find(".//ns:detEvento", ns)
                    if cancelada is not None:
                        continue

                    # Número da nota
                    numero_nota = root.find(".//ns:ide/ns:nNF", ns)
                    numero_nota = int(numero_nota.text) if numero_nota is not None else None

                    # Data de emissão
                    data_emissao = root.find(".//ns:ide/ns:dhEmi", ns)
                    if data_emissao is None:
                        data_emissao = root.find(".//ns:ide/ns:dEmi", ns)
                    if data_emissao is None:
                        continue

                    data_emissao = data_emissao.text.strip()
                    ano_mes = data_emissao[:7]  # AAAA-MM
                    mes_ano_formatado = f"{ano_mes[5:]}/{ano_mes[:4]}"

                    # Valor total
                    valor_total = root.find(".//ns:total/ns:ICMSTot/ns:vNF", ns)
                    valor_total = float(valor_total.text) if valor_total is not None else 0.0

                    # Armazena dados
                    dados_por_mes[mes_ano_formatado]["quantidade"] += 1
                    dados_por_mes[mes_ano_formatado]["valor"] += valor_total
                    if numero_nota is not None:
                        dados_por_mes[mes_ano_formatado]["notas"].append(numero_nota)

                except ET.ParseError:
                    continue

    return dados_por_mes

def exibir_relatorio(dados_por_mes):
    print("📅 Notas emitidas por mês:")
    for mes in sorted(dados_por_mes.keys(), key=lambda x: (x[3:], x[:2])):
        info = dados_por_mes[mes]
        notas_ordenadas = sorted(info["notas"])
        nota_inicio = notas_ordenadas[0] if notas_ordenadas else "-"
        nota_fim = notas_ordenadas[-1] if notas_ordenadas else "-"
        print(f"- {mes}: {info['quantidade']} nota(s) — R$ {info['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        print(f"  Nota início: {nota_inicio}  |  Nota final: {nota_fim}")

if __name__ == "__main__":
    arquivo_comprimido = "notas.rar"  # coloque aqui o nome do seu arquivo .zip ou .rar
    pasta_extraida = extrair_arquivos(arquivo_comprimido)
    dados = ler_xml_nfe(pasta_extraida)
    exibir_relatorio(dados)
