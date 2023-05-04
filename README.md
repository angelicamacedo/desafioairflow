## Orquestração com Airflow
Este projeto tem como objetivo colocar em prática conceitos iniciais de orquestração no Airflow a partir de uma base de dados Sqlite.

## Detalhamento do Desafio
1- Criar uma task que lê os dados da tabela ***'Order'*** do banco de dados disponível em ***data/Northwhind_small.sqlite***. Essa task deve escrever um arquivo chamado ***"output_orders.csv"***.

2- Criar uma task que lê os dados da tabela ***"OrderDetail"*** do mesmo banco de dados e faz um JOIN com o arquivo ***"output_orders.csv"*** que você exportou na tarefa anterior. Essa task deve calcular qual a soma da quantidade vendida ***(Quantity)*** com destino ***(ShipCity)*** para o ***Rio de Janeiro***. Você deve exportar essa contagem em arquivo ***"count.txt"*** que contenha somente esse valor em formato texto (use a função ***str()*** para converter número em texto). 

3- Adicionar uma variável no Airflow com a key ***"my_email"*** e no campo ***"value"*** adicione seu email.

4- Criar uma ordenação de execução das tasks que deve terminar com a task ***export_final_output***.

5- Rodar o DAG sem erros e gerar o arquivo ***final_output.txt*** com apenas um texto codificado gerado automaticamente pela task ***export_final_output***.

## Instruções

Nota: Os comandos utilizados são para ambiente Linux.

### 1. Clonando o repositório
O primeiro passo é clonar o repositório para um novo repositório no seu computador:

```sh
git clone git@github.com:angelicamacedo/desafioairflow.git
cd desafioairflow
```

### 2. Criando o ambiente de trabalho
Para instalar o Airflow, caso ainda não tenha, primeiro crie um virtualenv e depois rode o script install.sh. Esse script é uma cópia das instruções encontradas no site. Caso tenha o Airflow instalado, o arquivo ***requirements.txt*** precisa ser executado no ambiente onde o Airflow está instalado.

```sh
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
bash install.sh
```
Se as coisas derem certo, no terminal irá aparecer a seguinte mensagem:

```sh
standalone | 
standalone | Airflow is ready
standalone | Login with username: admin  password: sWFbFYrnYFAfYgY3
standalone | Airflow Standalone is for development purposes only. Do not use this in production!
standalone |
```
O Airflow roda na porta 8080, então podemos acessar em http://localhost:8080

### 3. Limpando os dags de exemplo
Para tirar os dags de exemplo e começar um DAG nosso, podemos editar o arquivo ***airflow.cfg*** localizado no diretório **~/airflow** trocando:

```sh
load_examples = True
```
para 
```sh
load_examples = False
```
Feito isso, termine a execução do Airflow pressionando ***CTRL + C*** no terminal.  

O Airflow procura por DAGs em arquivos ```.py``` no diretório ***~/airflow/dags***. Então, criaremos uma pasta chamada ***dags***, copiaremos o arquivo ```northwind.py``` e o colocaremos dentro de ***~/airflow/dags***. 

Copie também a pasta ***data*** para ***~/airflow***

A estrutura do diretório deve ficar assim:

```
├── airflow
│   ├── airflow.cfg
│   ├── airflow.db
│   ├── airflow-webserver.pid
│   ├── dags
│   ├── logs
│   ├── data
│   ├── standalone_admin_password.txt
│   └── webserver_config.py
```

Na sequência, rode o comando para resetar o db do Airflow e fazer start do Airflow local:

```sh
airflow db reset
airflow standalone
```

Dê um refresh no Airflow e veja se o DAG apareceu. Após a execução, se tudo deu certo, você terá três novos arquivos no diretório ***~/airflow/data***, sendo eles:***output_orders.csv***, ***count.txt*** e ***final_output.txt***. Além disso, no menu ***Admin -> Variables***deverá aparecer uma variável com a key "my_email" e um e-mail no campo "val". Para mais informações, veja a pasta ***imagens***.


No tópico a seguir, há o detalhamento de criação do DAG.


## Explicando a solução para o desafio 

1 - Importação dos módulos necessários para a execução do projeto
```py
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow import DAG
import sqlite3
import os
import base64
import pandas as pd
```
2 - Definindo o diretório e nome dos arquivos a serem lidos/gerados

```py
path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, '../data/Northwind_small.sqlite')
output_orders = os.path.join(path, '../data/output_orders.csv')
count_result = os.path.join(path, '../data/count.txt')
final_output = os.path.join(path, '../data/final_output.txt')
```
3 - Criando a função que lê os dados da tabela ***Order*** e cria um arquivo chamado ***output_orders.csv***

```py
def extract_orders():
    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect(db)
    
    # Lê os dados da tabela 'Order' usando o pandas
    df = pd.read_sql_query("SELECT * from 'Order'", conn)
    
    # Escreve o arquivo CSV
    df.to_csv(output_orders, index=False)
```

4 - Criando função que lê os dados da tabela ***OrderDetail*** e faz um join com o arquivo ***output_orders.csv***. Então calcula a soma da quantidade vendida ***(Quantity)*** com destino ***(ShipCity)*** para o ***Rio de Janeiro*** e exporta essa contagem em um arquivo ***count.txt***

```py
def count_quantity_to_rio():
    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect(db)

    # Lê os dados da tabela 'OrderDetail' usando o pandas
    df_detail = pd.read_sql_query("SELECT * from OrderDetail", conn)

    # Lê os dados do arquivo CSV 'output_orders.csv' usando o pandas
    df_orders = pd.read_csv(output_orders)

    # Faz um JOIN entre as tabelas 'OrderDetail' e 'Order' usando a coluna 'OrderId'
    df_join = pd.merge(df_detail, df_orders, left_on='OrderId', right_on='Id')

    # Filtra as linhas onde o destino é o Rio de Janeiro
    df_rio = df_join[df_join['ShipCity'] == 'Rio de Janeiro']

    # Calcula a soma da quantidade vendida para o Rio de Janeiro
    count = df_rio['Quantity'].sum()

    # Escreve o valor da contagem em um arquivo de texto
    with open(count_result, 'w') as f:
        f.write(str(count))

    # Fecha a conexão com o banco de dados
    conn.close()
```

5 - Adicionando uma variável no Airflow com a key ***my_email*** e adiciona um e-mail no campo value

```py
def add_my_email():
    Variable.set("my_email", "angelica.macedo@indicium.tech")
```

6 - Função que gera um texto codificado gerado automaticamente pela task ***export_final_output***

```py
def export_final():
    # Texto a ser codificado em base64
    text = "Texto Airflow codificado em base64"

    # Codifica o texto em base64
    encoded_text = base64.b64encode(text.encode()).decode()

    # Salva o texto codificado em um arquivo
    with open(final_output, 'w') as f:
        f.write(encoded_text)
```
#### Os argumentos abaixo serão passados para cada operador

```py
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
```

#### Criando o DAG:

```py
dag = DAG('task_order_execution',
          default_args=default_args,
          schedule_interval=None
)

task1 = PythonOperator(
    task_id='task1',
    python_callable=extract_orders,
    dag=dag
)

task2 = PythonOperator(
    task_id='task2',
    python_callable=count_quantity_to_rio,
    dag=dag
)

task3 = PythonOperator(
    task_id="task3",
    python_callable=add_my_email,
    dag=dag
)

export_final_output = PythonOperator(
    task_id='export_final_output',
    python_callable=export_final,
    dag=dag
)
```

#### Ordenação de execução das Tasks

```py
task1 >> task2 >> export_final_output
```






