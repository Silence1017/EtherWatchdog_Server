import requests

def bitqueryAPICall(query: str):
    headers = {'X-API-KEY': 'BQYMlGZXUMMzcPCkoJ4Egn7aMVHOJuzu'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,query))


# The GraphQL query

query = """
query ($network: EthereumNetwork!, $hash: String!, $limit: Int!, $offset: Int!) {
  ethereum(network: $network) {
    smartContractCalls(
      txHash: {is: $hash}
      options: {limit: $limit, offset: $offset}
    ) {
      smartContract {
        address {
          address
        }
      }
      smartContractMethod(smartContractMethod: {}) {
        name
      }
      address: caller {
        address
      }
    }
  }
}

"""

variables = {
  "limit": 10,
  "offset": 0,
  "network": "ethereum",
  "hash": "0x6c929e1c3d860ee225d7f3a7addf9e3f740603d243260536dfa2f3cf02b51de4"
}

result = bitqueryAPICall(query)
#inflow = result['data']['bitcoin']['inputs'][0]['value']
#outflow = result['data']['bitcoin']['outputs'][0]['value']
#balance = outflow-inflow
#print ("The balance of the Bitcoin wallet is {}".format(balance))
print(result)
print(type(result))
