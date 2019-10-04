import json
import requests
import simplejson as complexjson
import datetime
from pysolr import Solr

# import psycopg2


# templates = []
# templates.append(
#     '-0.037011910000000002, -0.00664601800000000006, 0.0107099010000000008, 0.0737079199999999962, -0.108862914000000005, 0.0267657250000000006, -0.0439099969999999992, -0.109475660000000002, -0.137991410000000009, 0.17642213000000001, 0.0212763119999999986, 0.0307382200000000001, 0.052940677999999998, -0.114703074000000002, 0.0812593000000000065, -0.0105438670000000002, 0.0951429200000000058, 0.0573748830000000015, 0.0927178599999999992, -0.0493947500000000012, -0.00608085469999999993, -0.179509210000000002, 0.162800240000000013, 0.034426074000000001, 0.00547843150000000036, -0.0245719549999999995, -0.0316947100000000009, 0.0714734640000000004, -0.196765410000000002, -0.108616229999999994, -0.0737815049999999972, -0.0366427699999999981, -0.0578547459999999986, 0.0237468719999999987, 0.144175999999999999, -0.0195041700000000012, 0.124564129999999995, 0.0973188360000000058, 0.144141230000000009, -0.0261765530000000017, 0.0579814800000000019, 0.120631896000000002, 0.0972114699999999943, 0.101020810000000003, -0.0674597549999999963, 0.0454500649999999978, 0.0824818239999999953, 0.0597614119999999999, -0.076563746000000002, 0.17525621999999999, 0.0501471399999999998, -0.0508460629999999969, 0.0700881099999999951, 0.0685324699999999981, 0.0981071399999999955, 0.182864059999999995, 0.0222169350000000002, -0.00444295630000000018, 0.00240321179999999999, -0.0302674960000000014, 0.156974140000000012, -0.0822841500000000003, -0.00753545800000000009, -0.0682959999999999956, 0.000541014829999999971, -0.121577439999999995, -0.16656783, -0.114877859999999998, -0.104956640000000004, -0.00197093900000000011, -0.0994669350000000063, 0.0425262669999999995, 0.0149399379999999998, -0.0481070580000000012, 0.0647929160000000059, -0.00169617800000000001, -0.0410210680000000008, 0.0506869439999999977, -0.0351111850000000031, -0.0552494379999999979, -0.00230485830000000001, -0.0786056150000000037, 0.0264332279999999996, 0.087983443999999994, 0.0332400100000000004, 0.0127717890000000004, 0.18933760999999999, 0.0268221389999999983, 0.00195694830000000012, -0.0119480000000000003, -0.168932529999999997, -0.0307370369999999983, 0.0122863050000000008, 0.0948812899999999931, 0.172073129999999991, -0.0661536100000000016, 0.0865394200000000058, -0.172083569999999991, -0.0699137799999999948, -0.0500211860000000022, 0.0767195450000000001, 0.0982428000000000051, -0.0511640299999999992, -0.068521953999999996, 0.0616075660000000025, -0.140695349999999997, -0.0292554099999999991, 0.0590939970000000023, 0.109489069999999994, -0.104790090000000002, 0.079011029999999996, -0.0181877429999999993, -0.0180418029999999986, 0.14554687999999999, -0.227822119999999989, -0.00185364220000000003, -0.0111450560000000004, 0.0478551129999999977, -0.0501227900000000004, 0.0155359620000000004, -0.0936181100000000044, -0.178739530000000008, 0.0621769839999999976, 0.0144565360000000007, -0.0898430649999999997, 0.0355385579999999979, 0.0924290640000000052, -0.0437677500000000011')

url_completa = 'http://localhost:8983/solr/teste/select?q=*:*'

solr_client = Solr('http://localhost:8983/solr/teste')


def get_function(dimension):
    return ','.join(['template_{0}_{1}_d'.format(dimension, i) for i in range(0, dimension)])


def get_document():
    return solr_client.search('*:*').docs[0]


def avaliar_solr(dimension):
    inicio_teste_global = datetime.datetime.now()
    print(inicio_teste_global)
    templates = solr_client.search('*:*')
    for template_teste in templates:
        fields = get_function(dimension)
        embedding = [str(template_teste['template_{0}_{1}_d'.format(dimension, i)]) for i in range(0, dimension)]
        funcao_distancia_euclidiana = 'sqedist('+ fields +',' + ','.join(embedding) + ')'
        payload = {"params": {
            "sort": funcao_distancia_euclidiana + ' asc ',
            "q": "*:*",
            "wt": "json",
            'rows': 4,
            "fl": "distancia:" + funcao_distancia_euclidiana + ',uuid'}
        }
        headers = {'Content-Type': 'application/json ; chartset=utf-8', 'Accept': 'application/json'}
        response = requests.post(url_completa, data=json.dumps(payload), headers=headers)
        # print('envio para extracao template  finalizado')
        response.encoding = 'utf-8'
        # print('iniciando extracao do json do response')
        print(response.text)
        resposta_decodificada = complexjson.loads(response.text, encoding='utf-8')
        tempo_requisicao = datetime.datetime.now()
        diferenca_tempo = tempo_requisicao - inicio_teste_global
        print(diferenca_tempo.total_seconds())
    final_tempo_global = datetime.datetime.now()
    print(final_tempo_global)
    print((final_tempo_global - inicio_teste_global).total_seconds())


avaliar_solr(8192)
