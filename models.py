from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from pycpfcnpj import cpfcnpj
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import object_session

db = SQLAlchemy()

class Jurisdicionado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), unique=True, nullable=False)
    genero = db.Column(db.String(10))
    data_nasc = db.Column(db.String(10))
    idade = db.Column(db.Integer)
    RG = db.Column(db.String(20))
    orgao_exp = db.Column(db.String(30))
    cpf = db.Column(db.String(14))
    genitor = db.Column(db.String(200))
    cpf_genitor = db.Column(db.String(14))
    genitora = db.Column(db.String(200))
    cpf_genitora = db.Column(db.String(14))
    fone_jurisdicionado = db.Column(db.String(30))
    email_jurisdicionado = db.Column(db.String(30))
    endereco = db.Column(db.String(300))
    bairro = db.Column(db.String(30))
    cep = db.Column(db.String(10))
    escolaridade = db.Column(db.String(10))
    turno = db.Column(db.String(10))
    instituicao_educacional = db.Column(db.String(200))
    fone_instituicao = db.Column(db.String(30))
    desempenho_escolar = db.Column(db.String(10))
    observacoes = db.Column(db.String(300))
    tutor_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'))
    demandas = db.relationship('Demanda', backref='vinculo')
    def __repr__(self):
        return '%r' % self.nome


class Responsavel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    responsavel_legal = db.Column(db.String(200), unique=True, nullable=False)
    cpf_responsavel_legal = db.Column(db.String(14))
    email_responsavel_legal = db.Column(db.String(30))
    grau_parentesco_id = db.Column(db.Integer)
    endereco_residencial = db.Column(db.String(200))
    bairro = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    fone_representante_legal = db.Column(db.String(30))
    celular_representante_legal = db.Column(db.String(30))
    email_representante_legal = db.Column(db.String(30))
    ind_contexto_familiar = db.Column(db.String(10))
    tutorados = db.relationship('Jurisdicionado', backref='tutor')
    def __repr__(self):
        return '%r' % self.responsavel_legal

class Demanda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vinculo_id = db.Column(db.Integer, db.ForeignKey('jurisdicionado.id'))
    nr_processo = db.Column(db.String(50))
    origem = db.Column(db.String(10))
    unid_solicitante_id = db.Column(db.Integer, db.ForeignKey('unidade_solicitante.id'))
    tecnico_resp = db.Column(db.String(100))
    data_solicitacao = db.Column(db.String(20))
    descricao_solicitacao = db.Column(db.String(300))
    prazo_cumprimento_meses = db.Column(db.Integer)
    data_cumprimento = db.Column(db.String(20))
    status_cumprimento = db.Column(db.String(10))
    pasta = db.Column(db.String(10))
    subpasta = db.Column(db.String(10))
    qual_curso = db.Column(db.String(100))
    sugestao_da_instituicao = db.Column(db.String(200))
    servidor_resp = db.Column(db.String(100))
    def __repr__(self):
        return '%r' % self.vinculo_id


class Unidade_solicitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100),  nullable=False)
    unidades = db.relationship('Demanda', backref='unid_solicitante')
    def __repr__(self):
        return '%r' % self.nome


class Parceiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200),  nullable=False)
    tipo_oferta = db.Column(db.String(20),  nullable=False)
    descricao_oferta = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20))
    data_ini = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))
  #  demandas = db.relationship('Demanda', secondary='vinculacao')

    def __repr__(self):
        return '<Parceiro %r>' % self.nome


class Vinculacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    demanda_id = db.Column(db.Integer, db.ForeignKey('demanda.id'))
    parceiro_id = db.Column(db.Integer, db.ForeignKey('parceiro.id'))
    demanda = db.relationship(Demanda, backref=backref('vinculacao', cascade='all, delete-orphan'))
    parceiro = db.relationship(Parceiro, backref=backref('vinculacao', cascade='all, delete-orphan'))
    status = db.Column(db.String(20))
    data_ini = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))


# ------- Voluntário Pessoa Física ----------
class Voluntario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), unique=True, nullable=False)
    genero = db.Column(db.String(10))
    nome_mae = db.Column(db.String(200))
    data_nasc = db.Column(db.String(10))
    RG = db.Column(db.String(20))
    orgao_exp = db.Column(db.String(30))
    CPF = db.Column(db.String(14))
    end_residencial = db.Column(db.String(200))
    complemento_residencial = db.Column(db.String(200))
    bairro_residencial = db.Column(db.String(50))
    cep_residencial = db.Column(db.String(10))
    fone = db.Column(db.String(30))
    celular = db.Column(db.String(30))
    email = db.Column(db.String(30))
    como_soube_rssa = db.Column(db.String(30))
    motivacao = db.Column(db.String(30))
    expectativa = db.Column(db.String(300))
    dadosprofissionais = db.relationship('DadoProfissional', backref='dado')
    atuacoes = db.relationship('Atuacaopf', backref='acoes')
    vinculacoes = db.relationship('Vinculapf', backref='atendimento')

    def __repr__(self):
        return '<voluntario %r>' % self.nome


class DadoProfissional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dado_id = db.Column(db.Integer, db.ForeignKey('voluntario.id'))
    formacao = db.Column(db.String(150))
    escolaridade = db.Column(db.String(50))
    atuacao_em_anos = db.Column(db.Integer)
    outros_cursos = db.Column(db.String(200))
    registro_profissional = db.Column(db.String(50))
    cargo_servidor = db.Column(db.String(50))
    ocupacao_atual = db.Column(db.String(50))
    end_comercial = db.Column(db.String(200))
    complemento_comercial = db.Column(db.String(200))
    bairro_comercial = db.Column(db.String(50))
    cep_comercial = db.Column(db.String(10))
    status = db.Column(db.String(20))
    data_ini = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))


class Atuacaopf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acoes_id = db.Column(db.Integer, db.ForeignKey('voluntario.id'))
    data_inscricao = db.Column(db.String(20))
    data_entrevista = db.Column(db.String(20))
    tratativas = db.Column(db.String(400))
    data_adesao = db.Column(db.String(20))
    atividade = db.Column(db.String(30))
    especialidade = db.Column(db.String(30))
    experiencia_anterior = db.Column(db.String(10))
    quais_experiencias = db.Column(db.String(200))
    disponibilidade = db.Column(db.String(30))
    deslocamentos_possiveis = db.Column(db.String(200))


class Vinculapf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atendimento_id = db.Column(db.Integer, db.ForeignKey('voluntario.id'))
    beneficiario = db.Column(db.String(200))
    detalhamento = db.Column(db.String(200))
    status = db.Column(db.String(20))
    data_ini = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))


# --------------- Pessoa Jurídica -----



class Juridico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150))
    nome_fantasia = db.Column(db.String(200), unique=True, nullable=False)
    CNPJ = db.Column(db.String(20))
    end_comercial = db.Column(db.String(200))
    complemento_comercial = db.Column(db.String(200))
    bairro_comercial = db.Column(db.String(50))
    cep_comercial = db.Column(db.String(10))
    fone1 = db.Column(db.String(30))
    fone2 = db.Column(db.String(30))
    fone3 = db.Column(db.String(30))
    genero = db.Column(db.String(10))
    email = db.Column(db.String(30))
    como_soube_rssa = db.Column(db.String(30))
    motivacao = db.Column(db.String(30))
    expectativa = db.Column(db.String(300))
    representantes = db.relationship('RepresentanteLegal', backref='contato')
    atuacoes = db.relationship('Atuacaopj', backref='acoes')
    vinculacoes = db.relationship('Vinculapj', backref='atendimento')

    def __repr__(self):
        return '<voluntario %r>' % self.nome


class RepresentanteLegal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contato_id = db.Column(db.Integer, db.ForeignKey('juridico.id'))
    nome = db.Column(db.String(200), unique=True, nullable=False)
    cargo = db.Column(db.String(60))
    RG = db.Column(db.String(20))
    orgao_exp = db.Column(db.String(30))
    CPF = db.Column(db.String(14))
    celular = db.Column(db.String(30))
    email = db.Column(db.String(30))
    status = db.Column(db.String(20))
    data_ini = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))


class Atuacaopj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acoes_id = db.Column(db.Integer, db.ForeignKey('juridico.id'))
    data_inscricao = db.Column(db.String(20))
    data_entrevista = db.Column(db.String(20))
    tratativas = db.Column(db.String(400))
    data_adesao = db.Column(db.String(20))
    atividade = db.Column(db.String(30))
    especialidade = db.Column(db.String(30))
    experiencia_anterior = db.Column(db.String(10))
    quais_experiencias = db.Column(db.String(200))
    disponibilidade = db.Column(db.String(30))
    deslocamentos_possiveis = db.Column(db.String(200))


class Vinculapj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atendimento_id = db.Column(db.Integer, db.ForeignKey('juridico.id'))
    beneficiario = db.Column(db.String(200))
    detalhamento = db.Column(db.String(200))
    status = db.Column(db.String(20))
    data_ini = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))



# ------ Doação --------------
class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_entrada = db.Column(db.String(10))
    descricao  = db.Column(db.String(150))
    tipo = db.Column(db.String(150))
    campanha = db.Column(db.String(200))
    origem = db.Column(db.String(20))
    quantidade_recebida = db.Column(db.String(200))
    unidade = db.Column(db.String(200))
    nome_doador = db.Column(db.String(150))
    email= db.Column(db.String(30))
    celular = db.Column(db.String(30))
    entregas = db.relationship('Saida', backref='entrega')

class Saida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_saida = db.Column(db.String(20))
    entrega_id = db.Column(db.Integer, db.ForeignKey('entrada.id'))
    destino = db.Column(db.String(200), unique=True, nullable=False)
    beneficiario = db.Column(db.String(60))
    processo_nr = db.Column(db.String(20))
    categoria = db.Column(db.String(30))
    quantidade_doada = db.Column(db.String(14))


def validate_cpf(target, value, oldvalue, initiator):
    # cpf = value
    assert cpfcnpj.validate(value), 'CPF Invalido!'
    return value


event.listen(Jurisdicionado.cpf, 'set', validate_cpf, retval=True)
