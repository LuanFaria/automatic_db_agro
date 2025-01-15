#pretendo criar uma função para cada usina
import pandas as pd
import numpy as np
import locale

#SANTA ADELIA
def santa_adelia():
    #IMPORTANDO BASE DE DADOS, criando um lista bdagro e removendo colunas indesejadas

    lista_bd_agro=['CHAVE',	'CLIENTE',	'SAFRA',	'OBJETIVO',	'TP_PROP',	'FAZENDA',	'SETOR',	'SECAO',	'BLOCO',	'PIVO',	'DESC_FAZ',	'TALHAO',	'VARIEDADE',	'MATURACAO',	'AMBIENTE',	'IRRIGACAO',	'ESTAGIO',	'GRUPO_DASH',	'GRUPO_NDVI',	'NMRO_CORTE',	'DESC_CANA',	'AREA_BD',	'A_EST_MOAGEM',	'A_COLHIDA',	'A_EST_MUDA',	'A_MUDA',	'TCH_EST',	'TC_EST',	'TCH_REST',	'TC_REST',	'TCH_REAL',	'TC_REAL',	'DT_CORTE',	'DT_ULT_CORTE',	'DT_PLANTIO',	'IDADE_CORTE',	'ATR',	'ATR_EST','TAH']
    banco_usa = pd.read_xml('input/estimativa_safra_202412101713.xml')
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
    bd_usa = bd_usa.replace('.',',').astype({'tch_rest': float, 'tch_est': float})
    bd_agro['TCH_EST'] = np.select([(bd_agro['A_EST_MOAGEM'] > 0)& (bd_usa['tch_rest'].isna()),(bd_agro['A_EST_MOAGEM'] > 0) & (bd_usa['tch_rest'] > 0)],[bd_usa['tch_est'],bd_usa['tch_rest']],default=0)
    bd_agro['TC_EST'] = bd_agro['TCH_EST'] * bd_agro['A_EST_MOAGEM']
    bd_agro['TCH_REST'] = np.select([(bd_agro['OBJETIVO'] == 'MOAGEM/MUDA') | (bd_agro['OBJETIVO'] == 'MOAGEM') ], [bd_usa['tch_est']], default=0)
    bd_agro['TC_REST'] = bd_agro['TCH_REST'] * bd_agro['A_EST_MOAGEM']
    bd_usa['cana_ent'] = bd_usa['cana_ent'].astype(str).str.replace(r'\.', '', regex=True)
    bd_usa['cana_ent'] = bd_usa['cana_ent'].str.replace(',', '.')
    bd_usa['cana_ent'] = pd.to_numeric(bd_usa['cana_ent'], errors='coerce')
    bd_agro['TCH_REAL'] = np.select([bd_usa['fg_ocorren'] == 'F'], [bd_usa['cana_ent']/bd_usa['area_est_col']], default=0)
    bd_agro['TC_REAL'] = bd_agro['TCH_REAL'] * bd_agro['A_COLHIDA']
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Para exibir a data em português
    bd_agro['DT_CORTE'] = pd.to_datetime(bd_usa['dt_corte_atual'], format='%d/%m/%Y', errors='coerce')
    bd_agro['DT_ULT_CORTE'] = pd.to_datetime(bd_usa['dt_corte_anterior'], format='%d/%m/%Y', errors='coerce')
    bd_agro['DT_PLANTIO'] = pd.to_datetime(bd_usa['dt_plantio'], format='%d/%m/%Y', errors='coerce')
    bd_agro['DT_CORTE'] = bd_agro['DT_CORTE'].dt.date
    bd_agro['DT_ULT_CORTE'] = bd_agro['DT_ULT_CORTE'].dt.date
    bd_agro['DT_PLANTIO'] = bd_agro['DT_PLANTIO'].dt.date
    bd_agro['DT_ULT_CORTE'] = np.select([bd_agro['NMRO_CORTE'] != 1], [bd_agro['DT_ULT_CORTE']], default=pd.to_datetime('1900-01-01').date())
    bd_agro['DT_CORTE'] = bd_agro['DT_CORTE'].fillna(pd.to_datetime('1900-01-01').date())
    bd_agro['DT_ULT_CORTE'] = bd_agro['DT_ULT_CORTE'].fillna(pd.to_datetime('1900-01-01').date())
    bd_agro['DT_PLANTIO'] = bd_agro['DT_PLANTIO'].fillna(pd.to_datetime('1900-01-01').date())
    bd_agro['DT_CORTE'] = pd.to_datetime(bd_agro['DT_CORTE'])
    bd_agro['DT_PLANTIO'] = pd.to_datetime(bd_agro['DT_PLANTIO'])
    bd_agro['DT_ULT_CORTE'] = pd.to_datetime(bd_agro['DT_ULT_CORTE'])
    bd_agro['IDADE_CORTE'] = np.where(
        bd_agro['NMRO_CORTE'] == 1,
        (bd_agro['DT_CORTE'] - bd_agro['DT_PLANTIO']).dt.days / 30,
        (bd_agro['DT_CORTE'] - bd_agro['DT_ULT_CORTE']).dt.days / 30)
    bd_agro.loc[(bd_agro['IDADE_CORTE'] > 35) | (bd_agro['IDADE_CORTE'] < 0), 'IDADE_CORTE'] = 0    
    bd_agro.to_excel('output/BD_AGRO_USA.xlsx', index=False)
    
#ESTIVA
def estiva():
    #IMPORTANDO BASE DE DADOS, criando um lista bdagro e removendo colunas indesejadas
    lista_bd_agro=['CHAVE',	'CLIENTE',	'SAFRA',	'OBJETIVO',	'TP_PROP',	'FAZENDA',	'SETOR',	'SECAO',	'BLOCO',	'PIVO',	'DESC_FAZ',	'TALHAO',	'VARIEDADE',	'MATURACAO',	'AMBIENTE',	'IRRIGACAO',	'ESTAGIO',	'GRUPO_DASH',	'GRUPO_NDVI',	'NMRO_CORTE',	'DESC_CANA',	'AREA_BD',	'A_EST_MOAGEM',	'A_COLHIDA',	'A_EST_MUDA',	'A_MUDA',	'TCH_EST',	'TC_EST',	'TCH_REST',	'TC_REST',	'TCH_REAL',	'TC_REAL',	'DT_CORTE',	'DT_ULT_CORTE',	'DT_PLANTIO',	'IDADE_CORTE',	'ATR',	'ATR_EST','TAH']
    banco_estiva = pd.read_csv('input/TALHAO_PDUOS_202501151415.csv', sep = ';', encoding = 'utf-8')
    estagios = pd.read_excel('X:/Sigmagis/VERTICAIS/COLABORADORES/Luan_Faria/MODELOS_BANCO/BANCO-SANTA-ADELIA/ESTAGIOS.xlsx')
    bd_estiva = banco_estiva.drop(labels=['SOLO', 'ESPACAMENTO', 'DISTANCIA', 'A_REFORMA', 'A_TIPO_APLIC_VINHACA', 'ID_DIVI4'], axis=1)
    bd_agro = pd.DataFrame(columns=lista_bd_agro)

    #concatenar ID
    bd_estiva['id'] = bd_estiva['FAZENDA'].astype(str) + '_' + bd_estiva['SECAO'].astype(str) + '_' + bd_estiva['TALHAO'].astype(str)

    #renomear tp_prop
    bd_estiva['TP_PROP'] = bd_estiva['TP_PROP'].replace({
    'CANA PROPRIA': 'PRÓPRIAS',
    'FORNECEDOR': 'FORNECEDORES'})

    #remover outras safras
    bd_estiva = bd_estiva.loc[bd_estiva['SAFRA'] != 2024]
    bd_estiva = bd_estiva.loc[bd_estiva['TP_PROP'] != 'FORNECEDORES']

    #verificar se tem duplicados 
    numero_duplicados = bd_estiva['id'].duplicated().sum()
    print(f'Número de duplicatas na coluna "id": {numero_duplicados}')

    # Definindo as condições de objetivo
    condicoes = [
        (bd_estiva['ESTAGIO'] == 'PLANTIO'),
        (bd_estiva['ESTAGIO'] == 'TEMPORARIO'),
        (bd_estiva['OBJETIVO'] == 'MOAGEM'),
        (bd_estiva['OBJETIVO'] == 'MUDA'),
        (bd_estiva['A_MUDA'] > 0) & (bd_estiva['A_EST_MOAGEM'] > 0),
        (bd_estiva['A_MUDA'] > 0) & (bd_estiva['A_EST_MOAGEM'] == 0)]

    # Definindo os valores correspondentes para cada condição
    valores = ['PLANTIO', 'TEMPORARIO', 'MOAGEM', 'MUDA', 'MOAGEM/MUDA','MUDA']

    # Aplicando as condições e atribuindo o valor na nova coluna 'OBJETIVO'
    bd_estiva['OBJETIVO'] = np.select(condicoes, valores, default='ADEF')

    bd_estiva = bd_estiva[bd_estiva['OBJETIVO'] != 'ADEF'].reset_index(drop=True)

    #esses adef são areas de dano
    contagem_objetivos = bd_estiva['OBJETIVO'].value_counts()
    print(contagem_objetivos)

    # Ajuste o nome da coluna, se necessário
    coluna_estagios = 'ESTAGIO'  # Substitua pelo nome correto se for diferente

    # Realizando o merge
    bd_estiva = pd.merge(
        bd_estiva,
        estagios,
        left_on='ESTAGIO',  # Coluna no bd_estiva
        right_on=coluna_estagios,  # Coluna no estagios
        how='left'
    )

    # Removendo a coluna duplicada se necessário
    if coluna_estagios in bd_estiva.columns:
        bd_estiva.drop(columns=[coluna_estagios], inplace=True)

    bd_agro['CHAVE'] = bd_estiva['id']
    bd_agro['CLIENTE'] = 'USINA ESTIVA'
    bd_agro['SAFRA'] = bd_estiva['SAFRA']
    bd_agro['OBJETIVO'] = bd_estiva['OBJETIVO']
    bd_agro['TP_PROP'] = bd_estiva['TP_PROP']
    bd_agro['FAZENDA'] = bd_estiva['FAZENDA']
    bd_agro['SETOR'] = bd_estiva['SETOR']
    bd_agro['SECAO'] = bd_estiva['SECAO']
    bd_agro['BLOCO'] = ''
    bd_agro['PIVO'] = ''
    bd_agro['DESC_FAZ'] = bd_estiva['DSC_FAZENDA']
    bd_agro['TALHAO'] = bd_estiva['TALHAO']
    bd_agro['VARIEDADE'] = bd_estiva['VARIEDADE'] 
    bd_agro['MATURACAO'] = bd_estiva['MATURACAO']
    bd_agro['AMBIENTE'] = bd_estiva['AMBIENTE']
    bd_agro['IRRIGACAO'] = bd_estiva['IRRIGACAO']
    bd_agro['ESTAGIO'] = bd_estiva['ESTAGIO_24']
    bd_agro['GRUPO_DASH'] = bd_estiva['GRUPO_DASH'] 
    bd_agro['GRUPO_NDVI'] = bd_estiva['GRUPO_NDVI']
    bd_agro['NMRO_CORTE'] = bd_estiva['NMRO_CORTE']
    bd_agro['DESC_CANA'] = bd_estiva['DESC_CANA']
    bd_agro['AREA_BD'] = bd_estiva['AREA_BD']
    bd_agro['A_EST_MOAGEM'] = bd_estiva['A_EST_MOAGEM']
    bd_agro['A_COLHIDA'] = bd_estiva['A_COLHIDA']
    bd_agro['A_EST_MUDA'] = bd_estiva['A_MUDA']
    bd_agro['A_MUDA'] = bd_estiva['A_MUDA']
    bd_estiva = bd_estiva.replace('.',',')
    bd_agro['TCH_EST'] = bd_estiva['TCH_EST']
    bd_agro['TC_EST'] =bd_agro['A_EST_MOAGEM'] * bd_estiva['TCH_EST']
    bd_agro['TCH_REST'] = ''
    bd_agro['TC_REST'] = ''
    bd_agro['TCH_REAL'] = np.select([bd_estiva['STATUS_TALHAO'] == 'ENCERRADA'], [bd_estiva['TCH_REAL']], default=0)
    bd_agro['TC_REAL'] = np.select([bd_agro['TCH_REAL']>0], [bd_agro['TCH_REAL'] * bd_agro['A_COLHIDA']], default=0)
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Para exibir a data em português
    bd_agro['DT_CORTE'] = bd_estiva['DT_CORTE']
    bd_agro['DT_ULT_CORTE'] = bd_estiva['DT_ULT_CORTE']
    bd_agro['DT_PLANTIO'] = bd_estiva['DT_PLANTIO']
    bd_agro['DT_ULT_CORTE'] = np.select([bd_agro['NMRO_CORTE'] != 1], [bd_agro['DT_ULT_CORTE']], default=pd.to_datetime('1900-01-01').date())
    bd_agro['DT_CORTE'] = bd_agro['DT_CORTE'].fillna(pd.to_datetime('1900-01-01').date())
    bd_agro['DT_ULT_CORTE'] = bd_agro['DT_ULT_CORTE'].fillna(pd.to_datetime('1900-01-01').date())
    bd_agro['DT_PLANTIO'] = bd_agro['DT_PLANTIO'].fillna(pd.to_datetime('1900-01-01').date())
    bd_agro['DT_CORTE'] = pd.to_datetime(bd_agro['DT_CORTE'])
    bd_agro['DT_PLANTIO'] = pd.to_datetime(bd_agro['DT_PLANTIO'])
    bd_agro['DT_ULT_CORTE'] = pd.to_datetime(bd_agro['DT_ULT_CORTE'])
    bd_agro['IDADE_CORTE'] = np.where(
    bd_agro['NMRO_CORTE'] == 1,
        (bd_agro['DT_CORTE'] - bd_agro['DT_PLANTIO']).dt.days / 30,
        (bd_agro['DT_CORTE'] - bd_agro['DT_ULT_CORTE']).dt.days / 30)
    bd_agro.loc[(bd_agro['IDADE_CORTE'] > 35) | (bd_agro['IDADE_CORTE'] < 0), 'IDADE_CORTE'] = 0  

    #gerando excel
    bd_agro.to_excel('output/BD_AGRO_ESTIVA.xlsx', index=False)


#PEDRA
def pedra():
    print('pedra')

#COCAL
def cocal():
    print('cocal')
