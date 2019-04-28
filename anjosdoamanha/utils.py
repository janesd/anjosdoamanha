
from enum import Enum

class VinculacoesChoices(Enum):
    contratado = 'contratado'
    matriculado = 'matriculado'
    desligado = 'desligado'
    desistente = 'desistente'
    nao_encontrado = 'nao encontrado'
    atendido = 'atendimento'
    movito_do_desligamento = 'motivo do desligamento'
    termino_do_contrato = 'termino do contrato'
    iniciativa_do_estudante = 'iniciativa do estudante'
    iniciativa_da_instituicao = 'iniciativa da instituicao'
    reincidencia = 'reincidencia'
    evasao_familiar = 'evasao familiar'
    gravidez = 'gravidez'
