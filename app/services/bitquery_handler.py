import requests
import json
from config import BITQUERY_API_KEY

# Endpoint API GraphQL Bitquery
API_ENDPOINT = "https://graphql.bitquery.io/"
HEADERS = {
    'Content-Type': 'application/json',
   'Authorization': 'Bearer ' + BITQUERY_API_KEY
}

def get_address_info(address: str):
    """
    Mengambil statistik dan tag (annotation) sebuah alamat dari Bitquery.
    Menggabungkan dua query menjadi satu untuk efisiensi.
    """
    if not BITQUERY_API_KEY:
        print("Error: BITQUERY_API_KEY tidak disetel.")
        return None

    # Query GraphQL
    query = """
    query ($address: String!) {
      # Alias 'stats' untuk query statistik
      stats: ethereum(network: ethereum) {
        addressStats(address: {is: $address}) {
          address {
            balance
            callTxCount
            sendTxCount
            receiveTxCount
            firstTransferAt {
              iso8601: time(format: "%Y-%m-%dT%H:%M:%SZ")
            }
          }
        }
      }
      # Alias 'info' untuk query anotasi/tag
      info: ethereum(network: ethereum) {
        address(address: {is: $address}) {
          annotation # Ini adalah field untuk 'tag'
        }
      }
    }
    """

    variables = {"address": address}

    try:
        response = requests.post(
            API_ENDPOINT,
            json={"query": query, "variables": variables},
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            print(f"GraphQL Error: {data['errors']}")
            return None

        # --- Ekstrak data dari kedua bagian query ---
        
        # 1. Ekstrak data statistik
        stats_data_list = data.get('data', {}).get('stats', {}).get('addressStats')
        if not stats_data_list or not stats_data_list[0].get('address'):
            return {"error": "Statistik alamat tidak ditemukan."}
        stats_data = stats_data_list[0]['address']

        # 2. Ekstrak data tag
        info_data_list = data.get('data', {}).get('info', {}).get('address')
        tag = "N/A"
        if info_data_list and info_data_list[0].get('annotation'):
            tag = info_data_list[0]['annotation']
        
        # --- Gabungkan hasil ---
        total_tx = (stats_data.get('callTxCount', 0) or 0) + \
                   (stats_data.get('sendTxCount', 0) or 0) + \
                   (stats_data.get('receiveTxCount', 0) or 0)

        result = {
            "address": address,
            "tag": tag,
            "balance_eth": stats_data.get('balance', 0),
            "transaction_count": total_tx,
            "first_tx_date": stats_data.get('firstTransferAt', {}).get('iso8601')
        }
        
        return result

    except requests.exceptions.RequestException as e:
        print(f"Error saat menghubungi API Bitquery: {e}")
        return None
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")
        return None

# # --- Contoh Penggunaan (untuk testing) ---
# if __name__ == '__main__':
#     test_address = "0xf977814e90da44bfa03b6295a0616a897441acec" 
    
#     print(f"Mencari info lengkap untuk alamat: {test_address}")
#     info = get_address_info(test_address) 
    
#     if info:
#         print(json.dumps(info, indent=2))