# 与 Dgraph 交互的代码
import pydgraph

def connect_dgraph():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)
