#! /usr/bin/python python3
import logging
import utils.app_utils as app_utl
import flask
import uuid
import json
from json import JSONDecodeError
import copy


logger = logging.getLogger(__name__)


def get_seq():
    seq = flask.g.get('seq', None)
    if not seq:
        flask.g.seq = 1
        return 1
    else:
        flask.g.seq += 1
        return flask.g.seq


def get_sessao():
    sessao = flask.g.get('sessao', None)
    if not sessao:
        flask.g.sessao = str(uuid.uuid4())
        return flask.g.sessao
    else:
        return flask.g.sessao


def trata_string(mensagem):
    msg = mensagem
    if type(msg) is str:
        try:
            msg = json.loads(msg).copy()
        except JSONDecodeError as err:
            msg = str(err)
    return msg


def trata_dict(key, dictionary):
    for k, v in dictionary.items():
        if k.startswith(key):
            dictionary[k] = '*********************'
        elif isinstance(v, dict):
            trata_dict(key, v)
    return dictionary


def default_logging(mensagem, level='INFO'):
    msg = mensagem
    msg = trata_string(msg)
    if isinstance(msg, dict):
        msg = copy.deepcopy(msg)
        msg = trata_dict('foto', msg)
    if level is 'INFO':
        logger.info('sessao=%s seq=%s mensagem=%s' % (app_utl.sessao, app_utl.seq, msg))
    if level is 'ERROR':
        logger.error('sessao=%s seq=%s mensagem=%s' % (app_utl.sessao, app_utl.seq, msg))
    app_utl.seq += 1


def default_status_logging(mensagem):
    logger.info('sessao=%s seq=%s mensagem=%s' % (get_sessao(), get_seq(), mensagem))
