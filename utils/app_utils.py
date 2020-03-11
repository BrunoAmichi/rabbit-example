#! /usr/bin/python python3
import uuid
import os
import argparse


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def has_letters(inputString):
    return any(char.isalpha() for char in inputString)


def init_log():
    global sessao
    global seq
    seq = 1
    sessao = str(uuid.uuid4())


def initialize_configs(params):
    '''
        Ideia e setar parametros de ambiente para o funcionamento correto do programa
    :param params: Parametros que deverao ser buscados no ambiente ou em argumentos de start do programa
                   Ordem Alias, Parametro, Help info
           exemplo: [('url','ELASTIC_URLS', 'Url do ambiente elasticsearch'), ('type','ELASTIC_TYPE' , 'Type para insercao no elasticsearch')]
    :return:
    '''

    global configs
    envs = {}
    parser = argparse.ArgumentParser()
    for param_alias, param, help in params:
        if param in os.environ:
            envs[param] = os.environ[param]
            parser.add_argument('-%s' % param_alias, '--%s' % param,
                                dest=param, required=False,
                                help=help)
        else:
            parser.add_argument('-%s' % param_alias, '--%s' % param,
                                    dest=param,required=True,
                                    help=help)
    args = parser.parse_args()

    parse_param = {k: v for k, v in args.__dict__.items() if v is not None}

    configs = {**envs, **parse_param}
    configs['tag'] = str(uuid.uuid4())
