#!/usr/bin/env bash

declare -a passwords=("admin" "12345678" "senha123" "senha" "29111982" "gQ7rj6" "Hl7gi4vrSB" "2pvx2H[k@Q:kD^}")

for password in "${passwords[@]}"
do

    python password_evaluation.py flask-evaluation --password ${password} --ngrams 3

done