import requests
import pandas as pd
from datetime import datetime, timedelta

# 🔹 CONFIGURAÇÕES GERAIS
UNISWAP_API = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
TOP_POOLS_QUERY = """
{
  pools(first: 20, orderBy: volumeUSD, orderDirection: desc) {
    id
    token0 { symbol decimals }
    token1 { symbol decimals }
    volumeUSD
    totalValueLockedUSD
    feeTier
  }
}
"""

def get_top_pools():
    response = requests.post(UNISWAP_API, json={"query": TOP_POOLS_QUERY})
    data = response.json()["data"]["pools"]
    return pd.DataFrame(data)

def analyze_pools(df):
    df["volumeUSD"] = df["volumeUSD"].astype(float)
    df["totalValueLockedUSD"] = df["totalValueLockedUSD"].astype(float)
    df["feeTier"] = df["feeTier"].astype(float)
    df["yield_estimate_%"] = (df["volumeUSD"] * (df["feeTier"]/1e6)) / df["totalValueLockedUSD"] * 100
    df = df.sort_values(by="yield_estimate_%", ascending=False)
    return df[["token0", "token1", "feeTier", "yield_estimate_%", "totalValueLockedUSD", "volumeUSD"]]

def main():
    print(f"📊 Atualização diária — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    pools = get_top_pools()
    analyzed = analyze_pools(pools)
    print("\nTop 10 pools com melhor potencial de rendimento:")
    print(analyzed.head(10))

if __name__ == "__main__":
    main()
