import grpc
import currency_pb2, currency_pb2_grpc

channel = grpc.insecure_channel('localhost:50053')
# stub = american_banks_pb2_grpc.AmericanBanksStub(channel)
# stub = latinamerican_banks_pb2_grpc.LatinAmericanBanksStub(channel)
# stub = european_banks_pb2_grpc.EuropeanBanksStub(channel)
stub = currency_pb2_grpc.CurrencyStub(channel)

# SAVE
# request = credit_cards_pb2.CreditCardNotIdRequest(
#   cardNumber = '1231',
#   username = 'name',
#   cvc = '',
#   expiration = '100821',
#   documentIdentification = '12312322'
# ) 
# response = stub.save(request)

## UPDATE
# request_data = {
#   'id': '5f4ed32e1e5ff775fa5cad16',
#   'cardNumber': '98798798789',
#   'username': 'username',
#   'cvc': 'X',
#   'expiration': 'x',
#   'documentIdentification': '12312'
# }

# request = credit_cards_pb2.CreditCardRequest(**request_data)
# response = stub.update(request)

# GET
request_data = {
  'id': '5f61424597d4148b035718fa'
}

request = currency_pb2.CurrencyIdRequest(**request_data)
response = stub.get(request)

## GET ALL
# request = currency_pb2.CurrencyEmpty()
# response = stub.get_all(request)

## DELETE
# request_data = {
#   'id': '5f4ed32e1e5ff775fa5cad16'
# }
# request = credit_cards_pb2.CreditCardIdRequest(**request_data)
# response = stub.delete(request)


## SHOW RESULT - DO NOT COMMENT

print(response)
