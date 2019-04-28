from anjosdoamanha import app
from anjosdoamanha.models import db
from anjosdoamanha.models import ( Demanda, Jurisdicionado, Responsavel,
                                   Parceiro, Vinculacao, Voluntario, DadoProfissional,
                                   Atuacaopf, Vinculapf, Juridico, RepresentanteLegal, 
                                   Vinculapj, Atuacaopj, Entrada, Saida
                                 )
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import render_template
from anjosdoamanha.utils import VinculacoesChoices

admin = Admin(app, name='Cadastro', template_mode='bootstrap3')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/relatorio_capacitacao")
def relatorio_capacitacao():

    # verificando os diferentes tipos de status existentes no arquivo Demanda
    tipo_de_status = []
    for value in Demanda.query.group_by(Demanda.status_cumprimento):
        tipo_de_status.append(value.status_cumprimento)

    
    # qtde_por_status: chave = tipo de status,
    #                  valor = qtde de registros com status igual ao da chave
    qtde_por_status = {}
    colecoes_por_status = {}
    #TODO enum
    for n in tipo_de_status:
        provisorio = Demanda.query.filter_by(pasta=2, status_cumprimento = '%s' %(n))
        if n == '1':
            nome_status = "no_prazo"
        elif n == '2':
            nome_status = "em_risco"
        elif n == '3':
            nome_status = "fora_do_prazo"
        elif n == '4':
            nome_status = "pendente"
        elif n == '5':
            nome_status = "recurso_indisponivel"
        elif n == '6':
            nome_status = "perfil_incompativel"
        else:
            nome_status = "nao_definido"
        qtde_por_status[nome_status] = provisorio.count()
        colecoes_por_status[nome_status] = provisorio

    vinculacoes_statuses = list(VinculacoesChoices)
    vinculacoes_by_status = {}
    for status in vinculacoes_statuses:
        vinculacoes_by_status[status.value] = Vinculacao.query.filter_by(status=status.value).all()

    return render_template('relatorio.html', 
                            titulo_pasta='Profissionalização/Capacitação', 
                            statuses=qtde_por_status, 
                            colecoes=colecoes_por_status,
                            vinculacoes=vinculacoes_by_status)

@app.route("/relatorio_saude")
def relatorio_saude():
    # verificando os diferentes tipos de status existentes no arquivo Demanda
    tipo_de_status = []
    for value in Demanda.query.group_by(Demanda.status_cumprimento):
        tipo_de_status.append(value.status_cumprimento)

    # qtde_por_status: chave = tipo de status,
    #                  valor = qtde de registros com status igual ao da chave
    qtde_por_status = {}
    colecoes_por_status = {}
    for n in tipo_de_status:
        provisorio = Demanda.query.filter_by(pasta=1, status_cumprimento='%s' % (n))
        if n == '1':
            nome_status = "no_prazo"
        elif n == '2':
            nome_status = "em_risco"
        elif n == '3':
            nome_status = "fora_do_prazo"
        elif n == '4':
            nome_status = "pendente"
        elif n == '5':
            nome_status = "recurso_indisponivel"
        elif n == '6':
            nome_status = "perfil_incompativel"
        else:
            nome_status = "nao_definido"
        qtde_por_status[nome_status] = provisorio.count()
        colecoes_por_status[nome_status] = provisorio

    # filter_by status


    return render_template('relatorio.html',titulo_pasta='Saúde', statuses=qtde_por_status, colecoes=colecoes_por_status)



class JurisdicionadoView(ModelView):
    column_searchable_list = ['nome']
    column_list = ['id', 'nome', 'data_nasc','cpf','RG']
    column_labels = dict(data_nasc='Data de Nascimento', cpf='CPF', RG='Doc.de Identidade')
    form_columns = ['nome' , 'genero', 'data_nasc', 'idade', 'RG' , 'orgao_exp' , 'cpf' , 'genitor' ,
                    'cpf_genitor', 'genitora', 'cpf_genitora', 'fone_jurisdicionado'  , 'email_jurisdicionado' , 'endereco',
                    'bairro', 'cep', 'escolaridade', 'turno', 'instituicao_educacional' , 'fone_instituicao', 'desempenho_escolar',
                    'observacoes' , 'tutor_id']
    form_choices = { 'turno': [ ('0', 'A informar'), ('1', 'Matutino'), ('2', 'Vespertino'), ('3', 'Noturno'),('4','Integral')] ,\
                     'genero': [('1', 'Feminino'), ('2', 'Masculino')], \
                     'desempenho_escolar': [('0','a informar'),('1','Nivelado'),('2','Defasado')], \
                     'escolaridade': [('0', 'a informar'), ('1', 'Alfabetização'), ('2', '1º ano EF'), ('3', '2º ano EF'), ('4', '3º ano EF'), ('5', '4º ano EF'), ('6', '5º ano EF'), ('7', '6º ano EF'), ('8', '7º ano EF'), ('9', '8º ano EF') , ('10', '9º ano EF'), ('11', '1º ano EM'), ('12', '2º ano EM') , ('13', '3º ano EM'), ('14', 'EJA-EF'), ('15', 'EJA-EM') , ('16', 'Ensino Superior')]} 
   
    edit_template = 'edit_user.html'
    create_template = 'create_user.html'

class DemandaView(ModelView):
    column_list = ['vinculo_id', 'pasta', 'subpasta', 'nr_processo', 'prazo_cumprimento_meses',
                   'origem','unid_solicitante_id','tecnico_resp','data_solicitacao', 'descricao_solicitacao',
                   'data_cumprimento', 'status_cumprimento', 'qual_curso', 'sugestao_da_instituicao', 'servidor_resp']
    column_labels = dict(vinculo_id='Beneficiário', subpasta='Opção')
                    
    form_columns = ['vinculo_id', 'pasta','subpasta','nr_processo', 'prazo_cumprimento_meses',
                   'origem','unid_solicitante_id','tecnico_resp','data_solicitacao', 'descricao_solicitacao',
                   'data_cumprimento', 'status_cumprimento', 'qual_curso', 'sugestao_da_instituicao', 'servidor_resp']
    
    form_choices = { 'origem': [ ('1', 'Determinação Judicial'), ('2', 'Requerimento Sessões Técnicas'), ('3', 'Requerimento Instituição de Acolhimento') , ('4', 'Requerimento Unidade de Medidas Sócio Educativa') , ('5', 'Outros')],
                     'status_cumprimento': [ ('1', 'No prazo'), ('2', 'Em risco'), ('3', 'Fora do prazo'), ('4', 'Pendente'), ('5', 'Recursos Indisponíveis'), ('6', 'Perfil Incompatível')]  ,
                     'pasta': [('0','a definir'),('1','Saúde'),('2','Profissionalização/Capacitação'),('3','Acompanhamento Pedagócico'),('4','Lazer/Cultura e Esporte'),('5','Doação')],
                     'subpasta': [('0','Menor Aprendiz'),('1','Estágio Nível Médio'),('2','Outros')]}

    edit_template = 'edit_user.html'
    create_template = 'create_user.html'

admin.add_view(JurisdicionadoView(Jurisdicionado, db.session, category="Jurisdicionado"))
admin.add_view(ModelView(Responsavel, db.session, category="Jurisdicionado"))
admin.add_view(DemandaView(Demanda, db.session, category="Jurisdicionado"))
admin.add_view(ModelView(Parceiro, db.session, category="Jurisdicionado"))
admin.add_view(ModelView(Vinculacao, db.session, category="Jurisdicionado"))

admin.add_view(ModelView(Voluntario, db.session, category="Pessoa Fisica"))
admin.add_view(ModelView(DadoProfissional, db.session, category="Pessoa Fisica"))
admin.add_view(ModelView(Atuacaopf, db.session, category="Pessoa Fisica"))
admin.add_view(ModelView(Vinculapf, db.session, category="Pessoa Fisica"))

admin.add_view(ModelView(Juridico, db.session, category="Pessoa Juridica"))
admin.add_view(ModelView(RepresentanteLegal, db.session, category="Pessoa Juridica"))
admin.add_view(ModelView(Atuacaopj, db.session, category="Pessoa Juridica"))
admin.add_view(ModelView(Vinculapj, db.session, category="Pessoa Juridica"))

admin.add_view(ModelView(Entrada, db.session, category="Doacao"))
admin.add_view(ModelView(Saida, db.session, category="Doacao"))