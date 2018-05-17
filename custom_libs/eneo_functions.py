import pandas as _pd
import numpy as _np

def get_version():
    '''
    Exibe a versão da biblioteca.
    '''
    print("eneo_functions 1.0")
    
def carrega_trafego(nome_do_arquivo):
    '''
    Realiza a carga dos dados do arquivo CSV especificado com os tipos de dados corretos.
    '''
    
    df = _pd.read_csv(
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

def media_harmonica(serie_de_dados):
    if len(serie_de_dados) == 0: 
        return None # Caso não existam dados no período a função retornará None
    else:
        serie_de_dados = serie_de_dados[serie_de_dados > 0]
        serie_de_dados = serie_de_dados[serie_de_dados < 120]
        return _np.round(len(serie_de_dados)/(sum(1/serie_de_dados)),2)
    
def calcula_variaveis(data_frame, frequencia):
    '''
    Calcula as variáveis de fluxo, velocidade média e densidade.
    Retorna um data frame.
    '''
    print("Total de faixas para processamento:", data_frame["faixa"].unique().size)
    to_ret = _pd.DataFrame()
    for fx in data_frame["faixa"].unique():
        print("Processando faixa:", fx)
        df = data_frame[data_frame["faixa"] == fx][["faixa","data_hora", "milissegundo", "velocidade_entrada", "velocidade_saida"]].copy()
        df["data_hora_milli"] = df["data_hora"] + _pd.to_timedelta(df["milissegundo"], unit='ms')
        df["time_diff_s"] = df["data_hora_milli"].diff().dt.total_seconds()
        df["velocidade_m/s"] = _np.round(df["velocidade_entrada"]/3.6, 2)
        df["espacamento_metros"] = df["velocidade_m/s"] * df["time_diff_s"]
        df.set_index("data_hora_milli", inplace=True, drop=True)
        df_g = df.resample(frequencia, label="right", closed="left").agg(
            {
                "data_hora":'count',
                "espacamento_metros":'mean',
                "velocidade_entrada":media_harmonica,
                "velocidade_saida":media_harmonica
            }
        )
        df_g["faixa"] = fx
        if to_ret.size == 0:
            to_ret = df_g
        else:
            to_ret = _pd.concat([to_ret, df_g])
    to_ret["densidade"] = (1 / to_ret["espacamento_metros"]) * 1000
    to_ret = to_ret[["faixa", "data_hora", "velocidade_entrada", "velocidade_saida", "densidade", "espacamento_metros"]]
    to_ret.columns = ["faixa", "fluxo", "vel_media_ent", "vel_media_saida", "densidade", "esp_medio_metros"]
    return to_ret
