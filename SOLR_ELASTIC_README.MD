PUT gait
{
  "mappings": {
    "properties": {
      "gait_embedding_1024": {
        "type": "dense_vector",
        "dims": 1024
      },
      "gait_embedding_512": {
        "type": "dense_vector",
        "dims": 512
      },
      "gait_embedding_128": {
        "type": "dense_vector",
        "dims": 128
      },
      "uuid" : {
        "type" : "keyword"
      }
    }
  }
}

PUT gait/_doc/1
{
  "gait_embedding_1024": [0.5, 10, 6],
  "uuid" : "uuid_value"
}

PUT gait/_doc/2
{
  "gait_embedding_1024": [-0.5, 10, 10],
  "uuid" : "uuid_value"
}

GET gait/_search
{
  "query": {
    "script_score": {
      "query" : {
        "bool" : {
          "filter" : {
            "term" : {
              "uuid" : "uuid_value" 
            }
          }
        }
      },
      "script": {
        "source": "cosineSimilarity(params.query_vector, doc['gait_embedding_1024']) + 1.0", 
        "params": {
          "query_vector": [4, 3.4, -0.2]  
        }
      }
    }
  }
}

GET gait/_search
{
  "query": {
    "script_score": {
      "query" : {
        "bool" : {
          "filter" : {
            "term" : {
              "uuid" : "uuid_value"
            }
          }
        }
      },
      "script": {
        "source": """
          double value = dotProduct(params.query_vector, doc['gait_embedding_1024']);
          return sigmoid(1, Math.E, -value); 
        """,
        "params": {
          "query_vector": [4, 3.4, -0.2]
        }
      }
    }
  }
}