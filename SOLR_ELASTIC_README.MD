GET _search
{
  "query": {
    "match_all": {}
  }
}

PUT my_index
{
  "mappings": {
    "properties": {
      "my_dense_vector": {
        "type": "dense_vector",
        "dims": 3
      },
      "my_sparse_vector" : {
        "type" : "sparse_vector"
      },
      "status" : {
        "type" : "keyword"
      }
    }
  }
}

PUT my_index/_doc/1
{
  "my_dense_vector": [0.5, 10, 6],
  "my_sparse_vector": {"2": 1.5, "15" : 2, "50": -1.1, "4545": 1.1},
  "status" : "published"
}

PUT my_index/_doc/2
{
  "my_dense_vector": [-0.5, 10, 10],
  "my_sparse_vector": {"2": 2.5, "10" : 1.3, "55": -2.3, "113": 1.6},
  "status" : "published"
}

GET my_index/_search
{
  "query": {
    "script_score": {
      "query" : {
        "bool" : {
          "filter" : {
            "term" : {
              "status" : "published" 
            }
          }
        }
      },
      "script": {
        "source": "cosineSimilarity(params.query_vector, doc['my_dense_vector']) + 1.0", 
        "params": {
          "query_vector": [4, 3.4, -0.2]  
        }
      }
    }
  }
}

GET my_index/_search
{
  "query": {
    "script_score": {
      "query" : {
        "bool" : {
          "filter" : {
            "term" : {
              "status" : "published"
            }
          }
        }
      },
      "script": {
        "source": "cosineSimilaritySparse(params.query_vector, doc['my_sparse_vector']) + 1.0",
        "params": {
          "query_vector": {"2": 0.5, "10" : 111.3, "50": -1.3, "113": 14.8, "4545": 156.0}
        }
      }
    }
  }
}

GET my_index/_search
{
  "query": {
    "script_score": {
      "query" : {
        "bool" : {
          "filter" : {
            "term" : {
              "status" : "published"
            }
          }
        }
      },
      "script": {
        "source": """
          double value = dotProduct(params.query_vector, doc['my_dense_vector']);
          return sigmoid(1, Math.E, -value); 
        """,
        "params": {
          "query_vector": [4, 3.4, -0.2]
        }
      }
    }
  }
}