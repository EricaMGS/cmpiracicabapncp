import requests
import pandas as pd

# CNPJ da Câmara Municipal de Piracicaba (apenas números)
cnpj_orgao = "51327708000192"
ano_auditoria = "2026"

# Endpoint oficial de contratos do PNCP
url = f"https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj_orgao}/contratos"

# Parâmetros de busca (a API do PNCP utiliza paginação)
parametros = {
    "dataInicial": f"{ano_auditoria}-01-01",
    "dataFinal": f"{ano_auditoria}-12-31",
    "pagina": 1,
    "tamanhoPagina": 50 
}

print(f"Buscando contratações do CNPJ {cnpj_orgao}...")
resposta = requests.get(url, params=parametros)

if resposta.status_code == 200:
    dados = resposta.json()
    
    # Os dados dos contratos geralmente vêm dentro da chave 'data'
    contratos = dados.get('data', [])
    
    if contratos:
        df_contratos = pd.DataFrame(contratos)
        
        # Filtrando colunas essenciais para a análise de controladoria
        colunas_interesse = [
            'numeroContrato', 
            'objetoContrato', 
            'valorInicial', 
            'dataPublicacaoPncp',
            'nomeRazaoSocialFornecedor'
        ]
        
        # Garante que vai puxar apenas as colunas que realmente vieram na resposta
        colunas_disponiveis = [col for col in colunas_interesse if col in df_contratos.columns]
        df_auditoria = df_contratos[colunas_disponiveis]
        
        print("\nExtração concluída com sucesso! Primeiros registros da Câmara de Piracicaba:")
        print(df_auditoria.head())
        
        # Opcional: exportar para CSV caso queira baixar o artefato depois
               
    else:
        print("Nenhum contrato encontrado para os parâmetros informados.")
else:
    print(f"Erro na extração. Código HTTP: {resposta.status_code}")
    print(f"Detalhe: {resposta.text}")
