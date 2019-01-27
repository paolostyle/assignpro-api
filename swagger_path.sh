#!/bin/bash

if [[ -z $OFFLINE_DEPLOY ]]; then
    sed -i "s/api.assignpro.ml/localhost:5000/" swagger.json;
    sed -i 's/https"/http"/' swagger.json;
fi
