from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Jurisdicionado, Responsavel,\
       Demanda, Parceiro, Vinculacao,\
       Voluntario, DadoProfissional, Atuacaopf, Vinculapf,\
       Juridico, RepresentanteLegal, Atuacaopj, Vinculapj,\
       Entrada, Saida

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anjosdados.db'
# POSTGRES = {
#     'user': 'postgres',
#     'password': 'secret',
#     'db': 'postgres',
#     'host': 'db',
#     'port': '5432',
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SECRET_KEY'] = 'mysecret'



db.init_app(app)
admin = Admin(app, name='Cadastro', template_mode='bootstrap3')

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/relatorio")
def relatorio():
    status = {}
    no_prazo = Demanda.query.filter_by(status_cumprimento=1)
    emrisco = Demanda.query.filter_by(status_cumprimento=2)
    foradoprazo = Demanda.query.filter_by(status_cumprimento=3)
    pendente = Demanda.query.filter_by(status_cumprimento=4)
    indisponivel = Demanda.query.filter_by(status_cumprimento=5)
    incompativel = Demanda.query.filter_by(status_cumprimento=6)
    status['no prazo'] = no_prazo.count()
    status['em risco'] = emrisco.count()
    status['fora do prazo'] = foradoprazo.count()
    status['pendente'] = pendente.count()
    status['recursos indisponivel'] = indisponivel.count()
    status['perfil incompativel'] = incompativel.count()
    # filter_by status
    #import pdb;pdb.set_trace()


    return render_template('relatorio.html', statuses=status, no_prazo=no_prazo, pendente=pendente,
    emrisco=emrisco, foradoprazo=foradoprazo, indisponivel=indisponivel, incompativel=incompativel)


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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')