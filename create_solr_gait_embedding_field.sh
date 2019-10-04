#!/usr/bin/env bash

export SOLR_HOME=/media/discoD/solr-8.2.0

./${SOLR_HOME}/bin/solr create -c gait

curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"gait_embedding_value","type":"gait_embedding_1024","stored":true }}' http://localhost:8983/solr/gait/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field-type":{"name":"embedding_1024","class":"solr.PointType","dimension":"1024","subFieldSuffix":"_d"}}' http://localhost:8983/solr/gait/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"gait_embedding_value","type":"gait_embedding_512","stored":true }}' http://localhost:8983/solr/gait/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field-type":{"name":"embedding_512","class":"solr.PointType","dimension":"512","subFieldSuffix":"_d"}}' http://localhost:8983/solr/gait/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"gait_embedding_value","type":"gait_embedding_128","stored":true }}' http://localhost:8983/solr/gait/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field-type":{"name":"embedding_128","class":"solr.PointType","dimension":"128","subFieldSuffix":"_d"}}' http://localhost:8983/solr/gait/schema
