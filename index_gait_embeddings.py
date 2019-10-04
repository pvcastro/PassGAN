import json
import requests
import simplejson as complexjson
import datetime
from pysolr import Solr
import numpy as np
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

solr_client = Solr('http://localhost:8983/solr/teste')

RS = 123


def get_cosine_similarity(embedding, embeddings):
    return [cosine_similarity(embedding, embedding_ref) for embedding_ref in embeddings]


def reduce_single_embedding(embedding, dimension):
    pca = PCA(n_components=dimension, random_state=RS)
    pca_result = pca.fit_transform(embedding)
    tsne = TSNE(n_components=dimension, random_state=RS).fit_transform(embedding)
    pca_50 = PCA(n_components=50, random_state=RS)
    pca_result_50 = pca_50.fit_transform(embedding)
    pca_tsne = TSNE(n_components=dimension, random_state=RS).fit_transform(pca_result_50)



def index_gait_embeddings(file_name, base_path = Path('/media/discoD/Mestrado/NoLeak/gait/')):
    file_path = base_path / file_name
    embedding = np.load(file_path, allow_pickle=True)[0][0]
    assert len(embedding) == 15872
    uuid = file_name.split('_')[0]
    print(uuid)
    solr_client.add([
        {
            'uuid': uuid,
            'template_8192': ','.join([str(value) for value in embedding[:8192]])
        }
    ])

index_gait_embeddings('5c4b9b22-843f-4db0-a60d-c1f8831c561f_09262019-200700.npy')
index_gait_embeddings('5338a22b-0e6f-44fc-a015-a80d5c296895_09262019-200700.npy')
index_gait_embeddings('08071d5b-9cb5-44c2-b880-ac46172704bd_09262019-200700.npy')
index_gait_embeddings('e639b627-c555-45fe-b0cf-c348c205410f_09262019-200700.npy')
solr_client.commit()
