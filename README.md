## Orquestração com Airflow
Este projeto tem como objetivo colocar em prática conceitos iniciais de orquestração no Airflow a partir de uma base de dados Sqlite

## Detalheamento do Desafio
1- Criar uma task que lê os dados da tabela 'Order' do banco de dados disponível em data/Northwhind_small.sqlite. Essa task deve escrever um arquivo chamado "output_orders.csv".

2- Criar uma task que lê os dados da tabela "OrderDetail" do mesmo banco de dados e faz um JOIN com o arquivo "output_orders.csv" que você exportou na tarefa anterior. Essa task deve calcular qual a soma da quantidade vendida (Quantity) com destino (ShipCity) para o Rio de Janeiro. Você deve exportar essa contagem em arquivo "count.txt" que contenha somente esse valor em formato texto (use a função str() para converter número em texto). 

3- Adicionar uma variável no Airflow com a key "my_email" e no campo "value" adicione seu email.

4- Criar uma ordenação de execução das tasks que deve terminar com a task export_final_output.

5- Rodar o DAG sem erros e gerar o arquivo final_output.txt com apenas um texto codificado gerado automaticamente pela task export_final_output.

## Instruções

### 1. Clonando o repositório
O primeiro passo é clonar o repositório para um novo repositório no seu computador:
```
git clone git@github.com:angelicamacedo/desafioairflow.git
cd desafioairflow
```

### 2. Criando o ambiente de trabalho
Para instalar o Airflow, primeiro crie um virtualenv e depois rode o script install.sh. Esse script é um ctrl c ctrl v das instruções encontradas no site.

```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
bash install.sh
```
Se as coisas deram certo, no terminal vai aparecer a seguinte mensagem:
```
standalone | 
standalone | Airflow is ready
standalone | Login with username: admin  password: sWFbFYrnYFAfYgY3
standalone | Airflow Standalone is for development purposes only. Do not use this in production!
standalone |
```
airflow roda na porta 8080, então podemos acessar em http://localhost:8080

### 3. Limpando os dags de exemplo
Para tirar os dags de exemplo e começar um dag nosso, podemos apagar os arquivos airflow-data/data e airflow-data/admin-password.txt, e editar o arquivo airflow.cfg trocando:

```
load_examples = True
```
para 
```
load_examples = False
```
Feito isso, configure o ambiente para dizer onde vão ficar os arquivos de config do airflow, fazemos isso configurando a seguinte variável de ambiente:

```
export AIRFLOW_HOME=./airflow-data
```
Na sequência, rode o comando para resetar o db do airflow e fazer start do airflow local:

```
airflow db reset
airflow standalone
```

O Airflow procura por DAGs na em arquivos .py no diretório:

```
AIRFLOW_HOME/dags
```
Em nosso caso AIRFLOW_HOME é airflow-data, então criaremos uma pasta dags e copiaremos o arquivo northwind.py dentro de airflow-data. Dê um refresh no airflow e veja se o dag apareceu.









