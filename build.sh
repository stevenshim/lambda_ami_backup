#!/bin/bash

if [[ ! -z terraform/lambda_ami_backup/modules/code.zip ]]
then
    rm terraform/lambda_ami_backup/modules/code.zip
fi

zip code.zip -j src/*
mv code.zip terraform/lambda_ami_backup/modules/code.zip