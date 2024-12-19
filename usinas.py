#pretendo criar uma função para cada usina
import pandas as pd
import numpy as np

#SANTA ADELIA
def santa_adelia():
    #IMPORTANDO BASE DE DADOS, criando um lista bdagro e removendo colunas indesejadas

    lista_bd_agro=['CHAVE',	'CLIENTE',	'SAFRA',	'OBJETIVO',	'TP_PROP',	'FAZENDA',	'SETOR',	'SECAO',	'BLOCO',	'PIVO',	'DESC_FAZ',	'TALHAO',	'VARIEDADE',	'MATURACAO',	'AMBIENTE',	'IRRIGACAO',	'ESTAGIO',	'GRUPO_DASH',	'GRUPO_NDVI',	'NMRO_CORTE',	'DESC_CANA',	'AREA_BD',	'A_EST_MOAGEM',	'A_COLHIDA',	'A_EST_MUDA',	'A_MUDA',	'TCH_EST',	'TC_EST',	'TCH_REST',	'TC_REST',	'TCH_REAL',	'TC_REAL',	'DT_CORTE',	'DT_ULT_CORTE',	'DT_PLANTIO',	'IDADE_CORTE',	'ATR',	'ATR_EST','TAH']
    banco_usa = pd.read_xml('estimativa_safra_202412101713.xml')
    estagios = pd.read_excel('X:/Sigmagis/VERTICAIS/COLABORADORES/Luan_Faria/MODELOS_BANCO/BANCO-SANTA-ADELIA/ESTAGIOS.xlsx')
    bd_usa = banco_usa.drop(labels=['usina','blocoicol','de_obs','no_corte','categoria','rest','gr_est','fornecedor','municipio','quad','qt_area_prod','qt_area_muda','qt_area_dano','idade_corte','idade_atual','fg_refor_plane','fg_temporario','fg_dano_colheita','fg_meiosi','dt_ocorren','n_rest','id_unidade','updated_at','created_at'], axis=1)
    bd_agro = pd.DataFrame(columns=lista_bd_agro)

    #concatenar ID
    bd_usa['id'] = bd_usa['cd_fazenda'].astype(str) + '_' + bd_usa['bloco'].astype(str) + '_' + bd_usa['talhao'].astype(str)

    #remover spot e renomear PRÓPRIAS e FORNECEDORES
    bd_usa = bd_usa[bd_usa['tp_prop'] != 'SPOT'].reset_index(drop=True)

    bd_usa['tp_prop'] = bd_usa['tp_prop'].replace({
        'PRÓPRIA': 'PRÓPRIAS',
        'FORNECEDOR': 'FORNECEDORES'
    })
    
    #verificar se tem duplicados 
    numero_duplicados = bd_usa['id'].duplicated().sum()
    print(f'Número de duplicatas na coluna "id": {numero_duplicados}')
    
    # Substituindo a vírgula por ponto nas colunas 'area_est_col' e 'area_est_mud'
    bd_usa['area_est_col'] = bd_usa['area_est_col'].str.replace(',', '.').astype(float)
    bd_usa['area_est_mud'] = bd_usa['area_est_mud'].str.replace(',', '.').astype(float)

    # Definindo as condições
    condicoes = [
        (bd_usa['area_est_col'] > 0) & (bd_usa['area_est_mud'] > 0),
        (bd_usa['area_est_col'] > 0),
        (bd_usa['area_est_mud'] > 0)
    ]

    # Definindo os valores correspondentes para cada condição
    valores = ['MOAGEM/MUDA', 'MOAGEM', 'MUDA']

    # Aplicando as condições e atribuindo o valor na nova coluna 'OBJETIVO'
    bd_usa['OBJETIVO'] = np.select(condicoes, valores, default='ADEF')

    bd_usa = bd_usa[bd_usa['OBJETIVO'] != 'ADEF'].reset_index(drop=True)
    #esses adef são areas de dano
    contagem_objetivos = bd_usa['OBJETIVO'].value_counts()
    print(contagem_objetivos)

        # Ajuste o nome da coluna, se necessário
    coluna_estagios = 'ESTAGIO'  # Substitua pelo nome correto se for diferente

    # Realizando o merge
    bd_usa = pd.merge(
        bd_usa,
        estagios,
        left_on='da_estagio',  # Coluna no bd_usa
        right_on=coluna_estagios,  # Coluna no estagios
        how='left'
    )

    # Removendo a coluna duplicada se necessário
    if coluna_estagios in bd_usa.columns:
        bd_usa.drop(columns=[coluna_estagios], inplace=True)

    bd_agro['CHAVE'] = bd_usa['id']
    condicoes = [
        (bd_usa['empresa'] == 'SAJB'),
        (bd_usa['empresa'] == 'SAPB')
    ]
    # Definindo os valores correspondentes para cada condição
    valores = ['SANTA ADÉLIA JB','SANTA ADÉLIA PB']
    bd_usa['empresa'] = np.select(condicoes, valores, default='ADEF')
    bd_agro['CLIENTE'] = bd_usa['empresa']
    bd_agro['SAFRA'] = bd_usa['safra'] *1000
    bd_agro['SAFRA'] = bd_agro['SAFRA'].astype(int)
    bd_agro['OBJETIVO'] = bd_usa['OBJETIVO'] 
    bd_agro['TP_PROP'] = bd_usa['tp_prop']
    bd_agro['FAZENDA'] = bd_usa['cd_fazenda']
    bd_agro['SETOR'] = ''
    bd_agro['SECAO'] = ''
    bd_agro['BLOCO'] = bd_usa['bloco']
    bd_agro['PIVO'] = ''
    bd_agro['DESC_FAZ'] = bd_usa['de_fazenda']
    bd_agro['TALHAO'] = bd_usa['talhao']
    bd_agro['VARIEDADE'] = bd_usa['variedade'] 
    bd_agro['MATURACAO'] = bd_usa['amb_manejo']
    bd_agro['AMBIENTE'] = bd_usa['amb_producao']
    bd_agro['IRRIGACAO'] = bd_usa['fg_infr_fertir']
    bd_agro['ESTAGIO'] = bd_usa['ESTAGIO_24']
    bd_agro['GRUPO_DASH'] = bd_usa['GRUPO_DASH'] 
    bd_agro['GRUPO_NDVI'] = bd_usa['GRUPO_NDVI']
    bd_agro['NMRO_CORTE'] = bd_usa['NMRO_CORTE']
    bd_agro['DESC_CANA'] = bd_usa['DESC_CANA']
    bd_agro['AREA_BD'] = bd_usa['area_est_col'] + bd_usa['area_est_mud']
    bd_agro['A_EST_MOAGEM'] = bd_usa['area_est_col']
    bd_agro['A_COLHIDA'] = np.select([bd_usa['fg_ocorren'] == 'F'], [bd_agro['A_EST_MOAGEM']], default=0)
    bd_agro['A_EST_MUDA'] = bd_usa['area_est_mud']
    bd_agro['A_MUDA'] = np.select([bd_usa['fg_ocorren'] == 'F'], [bd_agro['A_EST_MUDA']], default=0)

    

    
    bd_agro.to_excel('BD_AGRO_USA.xlsx', index=False)
    



#ESTIVA
def estiva():
    print('Estiva')

#PEDRA
def pedra():
    print('pedra')

#COCAL
def cocal():
    print('cocal')
