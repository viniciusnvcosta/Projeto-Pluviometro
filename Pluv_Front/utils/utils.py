import json
import pandas as pd
import quantstats as qs


def load(data_load,col_index=None,sort_index=False,ffill=False):
    
    if not data_load:
        return pd.DataFrame()
        
    df_load  = pd.DataFrame(json.loads(data_load)) 
    
    if col_index: 
        df_load = df_load.set_index('data')
    if sort_index:
        df_load = df_load.sort_index()
    if ffill:
        df_load  = df_load.ffill()
            
    return df_load

        
def merge_data_to_json(df,df_resp):
    if df.empty:
        return df_resp.to_json(orient='records')
    
    df_merge = df.merge(df_resp,on='data',how='outer')
    result = df_merge.to_json(orient='records')
    
    return result

def concate_to_json(df,df_resp):
    if df.empty:
        return df_resp.to_json(orient='records')
    
    df_concat = pd.concat([df,df_resp.reset_index()])
    result = df_concat.to_json(orient='records')
    
    return result

def merge(df,df_resp):
    if df.empty:
        return df_resp
    
    df_merge = df.merge(df_resp,on='data',how='outer')
    # result = df_merge.to_json(orient='records')
    
    return df_merge

def concate(df,df_resp):
    if df.empty:
        return df_resp
    
    df_concat = pd.concat([df,df_resp.reset_index()])
    # result = df_concat.to_json(orient='records')
    
    return df_concat

def vol(retorno_diario: pd.Series):
    df_retorno_diario = retorno_diario.add(-1)
    df_vol = qs.stats.rolling_volatility(df_retorno_diario, rolling_period=255)
    
    df_vol =  df_vol.mul(100)
    df_vol =  df_vol.round(2)
    df_vol =  df_vol.fillna(0)
    
    return df_vol

def cumprod(retorno_diario: pd.Series):
    df_cumprod = retorno_diario.cumprod()
    df_cumprod = df_cumprod.add(-1).mul(100).round(2)
    
    return df_cumprod


def drawdown(retorno_diario: pd.Series):
    df_retorno_diario = retorno_diario.add(-1)
    df_drawdown = qs.stats.to_drawdown_series(df_retorno_diario)
    df_drawdown = df_drawdown.mul(100).round(2)

    return df_drawdown



def porcentagem(df):
    columns = df.select_dtypes(['number']).columns

    df[columns] = df[columns].add(-1)
    df[columns] = df[columns].mul(100)
    df = round_numbers(df)

    return df

def round_numbers(df):
    columns = df.select_dtypes(['number']).columns
    df[columns] = df[columns].round(2) 

    return df