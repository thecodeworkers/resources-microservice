from json import loads

def parserAllObject(model):
    parser = model.objects.all().to_json()
    parser = loads(parser)

    parser = map(lambda x:(x,x.__setitem__('_id', x['_id']['$oid']))[0], parser)
    return list(parser)
