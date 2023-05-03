from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow import DAG
import sqlite3
import os
import base64
import pandas as pd

# Definindo diretório e nome dos arquivos a serem lidos/gerados
path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, '../data/Northwind_small.sqlite')
output_orders = os.path.join(path, '../data/output_orders.csv')
count_result = os.path.join(path, '../data/count.txt')
final_output = os.path.join(path, '../data/final_output.txt')


def extract_orders():
    '''
        Função que lê os dados da tabela Order e cria um arquivo chamado output_orders.csv
    '''

    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect(db)
    
    # Lê os dados da tabela 'Order' usando o pandas
    df = pd.read_sql_query("SELECT * from 'Order'", conn)

    # Escreve o arquivo CSV
    df.to_csv(output_orders, index=False)


def count_quantity_to_rio():
    '''
        Função que lê os dados da tabela OrderDetail e faz um join com o arquivo output_orders.csv. 
        Então calcula a soma da quantidade vendida (Quantity) com destino (ShipCity) para o Rio de Janeiro
        e exporta essa contagem em um arquivo count.txt
    '''

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


def add_my_email():
    ''' 
        Adiciona uma variável no Airflow com a key my_email e adiciona um e-mail no campo value
    '''
    Variable.set("my_email", "angelica.macedo@indicium.tech")


def export_final():
    '''
        função que gera um texto codificado gerado automaticamente pela task export_final_output
    '''

    # Texto a ser codificado em base64
    text = "Texto Airflow codificado em base64"

    # Codifica o texto em base64
    encoded_text = base64.b64encode(text.encode()).decode()

    # Salva o texto codificado em um arquivo
    with open(final_output, 'w') as f:
        f.write(encoded_text)


# Esses argumentos serão passados para cada operador

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

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

# Ordenação de execução das Tasks
task1 >> task2 >> export_final_output