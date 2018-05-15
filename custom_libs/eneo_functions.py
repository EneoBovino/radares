import pandas as pd
import numpy as np

def get_version():
    '''
    Exibe a versão da biblioteca.
    '''
    print("eneo_functions 1.0")
    
def carrega_trafego(nome_do_arquivo):
    '''
    Realiza a carga dos dados do arquivo CSV especificado com os tipos de dados corretos.
    '''
    
    df = pd.read_csv(
        "../input/"+nome_do_arquivo,
        delimiter=",",
        dtype = {
            "numero_de_serie":int,
            "milissegundo":int,
            "faixa":int,
            "velocidade_entrada":int,
            "velocidade_saida":int,
            "classificacao":int,
            "tamanho": float,
            "placa":str,
            "tempo_ocupacao_laco":int
        },
        parse_dates=["data_hora"]
    )
    
    return df
    
