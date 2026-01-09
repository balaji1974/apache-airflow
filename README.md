
# Apache Airflow

## What is Airflow & Core Concepts

```xml 

It is a workflow management platform and used for managing complex workflows

Workflow is a sequence of tasks
Workflow is defined as DAGs (Directed Acyclic Graph)
Task is a unit of work within a DAG and is represented as a node in the DAG
Task is written in python
Operators determine what actually is done by a task 
(Eg. BashOperator, PythonOperator, CustomizedOperator)
Each task is an implementation of an operato.

Operators determines what is going to be done
while a task determines the specific values for that operator 
DAG is a collection of all the task that we want to run 
organized in a way that represents their relationships and dependencies 

Execution Date: Is the logical date and time in which the DAG run and 
its task instances are running 
Task Instance: It is a run of a task at a specific point of time (execution date)
DAG run: Is the initiation of a DAG containing task instances that run
for a specific execution date

DAG - consist of nodes (connected by edges) and edges (sharp one way direction)

```

## Task Lifecycle 

```xml 
Task Stages - Early Phase
-------------------------

no_status: The task is not yet ready for execution, as its dependencies 
are not yet met.

scheduled: The scheduler has determined that the task's dependencies are 
fulfilled and it should run.

queued: The task has been assigned to an executor and is waiting for an 
available worker to pick it up.

running: A worker is actively executing the task.

Task Stages - Execution Phase
-----------------------------
success: The task completed successfully without any errors. 

upstream_failed: The task was not run because one or more of its 
preceding tasks failed.

up_for_reschedule: The task, typically a sensor, is waiting and 
will be tried again at a later interval without being marked as a failure.

skipped: The task was intentionally bypassed, often due to a branching condition 
or a specific trigger rule.

deferred: The task has been paused (e.g., in an asynchronous operation) 
and handed off to a trigger, waiting for an external event to resume.

removed: The task is no longer present in the DAG definition since the run began. 

Task Stages - Failure Stage
---------------------------

failed: The task encountered an error during execution and 
did not complete successfully.

up_for_retry: The task failed but is configured to retry and 
will be rescheduled for execution.

shutdown: The task was interrupted or aborted due to a system shutdown 
or manual intervention.

```
![TaskStages](https://github.com/balaji1974/apache-airflow/blob/main/airlfow-task-retry-and-reschedule.png?raw=true)


## Architecture
```xml 

The following are the main components of the fundamental architecture of Apache Airflow

Data Engineer:
Responsible for building and monitoring ETL processes.
Configures Airflow settings, such as the executor type and database choice.
Manages DAGs through the Airflow UI.

Web Server, Scheduler, and Worker:
The web server supports the Airflow UI, visible to data engineers.
The scheduler manages DAG visibility and influences task status.
Workers execute tasks picked from the queue.

Database and Executor:
Connected components for persisting DAG updates and information retrieval.
Various database engines like MySQL or PostgreSQL can be chosen.

```
![Architecture](https://github.com/balaji1974/apache-airflow/blob/main/airflow-basic-architecture-graph.png?raw=true)


## Install Airflow

```xml 

Note: Was not working with python 3.13.0 and had to downgrade it to python 3.11.9
1. Create a folder called apache-airflow and open it in visual studio.

2. Open this folder in terminal 

3. Check python version
python3 --version  

4. Create a python environment
python3 -m venv py_env

5. Activate the environment
source py_env/bin/activate

6. Install airflow
pip install apache-airflow[EXTRAS]==AIRFLOW_VERSION --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-AIRFLOW_VERSION/constraints-PYTHON_VERSION.txt"
Eg. for version 3.1.5
pip install "apache-airflow[celery]==3.1.5" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.5/constraints-3.10.txt"

7. Make my current directory as airflow home directory 
export AIRFLOW_HOME=/<your-project-directory>/apache-airflow

8. Create Airflow database connection
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////<your-project-directory>/airflow.db

9. Check if database can be reached
airflow db check

10. Initialize the DB
airflow db migrate

11. Start the airflow server:
airflow standalone

12. Once the server is started a password file is randomly generated 
and stored in the project root directory as simple_auth_manager_passwords.json.generated
Open it and copy the password

13. Login to the server:
http://localhost:8080/
User name: admin
Password: <randomly generated password stored in simple_auth_manager_passwords.json.generated>

14. You will now enter the landing page of Airflow
Login
Go to Dags
Click on one of dags
Select one of the displayed dags
Select Treeview

15. Finally stop server and run
deactivate
```

## Install Airflow on Docker

```xml 
1. Download and install docker 
Follow official document at 
https://docs.docker.com/desktop/

2. Check if docker running
docker --version
docker-compose --version

3. Fetch Official Docker compose file for airflow:
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.5/docker-compose.yaml'
In our folder we have this file as docker-compose-original.yaml.

4. Optimize the docker compose as given in the project directory 
to remove unnecessay dependencies
In our folder we have this file as docker-compose-optimized.yaml. 
Please rename it to docker-compose.yaml and use it. 

5. Create directory and give access to docker-compose
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

6. Initilize the database
docker compose up airflow-init

7. Run the container in background
docker compose up -d

8. Go to airflow
http://localhost:8080
User name: airflow
Password: airflow

9. You will now enter the landing page of Airflow
Login
Go to Dags
Click on one of dags
Select one of the displayed dags
Select Treeview

Select example_bash_operator
Start it by toggling the button next to it 
and see it run successfully 

```

## Remove all existing examples from Airflow
```xml 
1. Remove the existing volume:
docker compose down -v

2. In the docker-compose.yaml file change the below variable 
from true to false and save it. 
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

3. Initilize Airflow
docker compose up airflow-init

4. Launch Airflow
docker compose up -d

8. Go to airflow
http://localhost:8080
User name: airflow
Password: airflow

9. You will now enter the landing page of Airflow
Login
Go to DAGs
All example DAGs will now be missing or removed

```

## Create our first DAG - With BashOperator
```xml 
All dags are created under the dags folder.
1. Under this folder create a file called dag_with_bash_operator.py
with the following content.

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


default_args = {
    'owner': 'balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


with DAG(
    dag_id='dag_with_bash_operator_v1',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2026, 1, 4, 2),
    schedule='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is the first task!"
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo hey, I am task2 and will be running after task1!"
    )

    task3 = BashOperator(
        task_id='thrid_task',
        bash_command="echo hey, I am task3 and will be running after task1 at the same time as task2!"
    )

    # Task dependency method 1
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    # Task dependency method 2
    # task1 >> task2
    # task1 >> task3

    # Task dependency method 3
    task1 >> [task2, task3]

2. Refresh the page containing our DAGs and see its execution 

3. You can make changes to the DAG and create a different version 
in the code by changing the version id: 
dag_id='our_first_dag_v2'

4. You can give the dependency of tasks in multiple ways:
# Task dependency method 1
task1.set_downstream(task2)
task1.set_downstream(task3)

# Task dependency method 2
task1 >> task2
task1 >> task3

# Task dependency method 3
task1 >> [task2, task3]


```

## Create DAG - With PythonOperator
```xml 
We want to create a python operator with 2 python packages 
skikit-learn
matplotlib

In order to make sure that these 2 packages exit within our python
environment do the following before running the docker container

1. Create a Dockerfile with the following contents:
ARG AIRFLOW_IMAGE_NAME=apache/airflow:3.1.5
FROM ${AIRFLOW_IMAGE_NAME}

USER airflow
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir matplotlib

2. Add the following in the docker-compose.yaml file 
airflow-scheduler:
    build: .
    image: my-airflow:custom

airflow-dag-processor:
    build: .

Leave the other sections and lines within the sections as is. 

3. Build the docker container
docker compose down
# just to make sure the same image does not exist
docker image rm my-airflow:custom 2>/dev/null || true
docker compose build --no-cache 
docker compose up -d 

4. Under this folder create a file called dag_with_python_operator.py
with the following content.
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


default_args = {
    'owner': 'balaji',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(name, age):
    print(f"Name is {name} and age is {age} ")

def get_sklearn():
    import sklearn
    print(f"sklearn with version: {sklearn.__version__} ")


def get_matplotlib():
    import matplotlib
    print(f"matplotlib with version: {matplotlib.__version__}")

def set_name():
    return "Balaji"

def get_name(ti):
    name = ti.xcom_pull(task_ids='set_name')
    print(f"Hello my name is {name}")

def set_multiple_values(ti):
    ti.xcom_push('first_name', "Balaji")
    ti.xcom_push('last_name', "Thiagarajan") 

def get_multiple_values(ti):
    first_name = ti.xcom_pull(task_ids='set_multiple_values', key='first_name')
    last_name = ti.xcom_pull(task_ids='set_multiple_values', key='last_name')
    print(f"Full name is {first_name} {last_name}") 

with DAG(
    default_args=default_args,
    dag_id="dag_with_python_operator_v8",
    start_date=datetime(2026, 1, 5),
    schedule='@daily'
) as dag:
    
    # Calling simple function and passing parameters to it using op_kwargs
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name': 'Balaji', 'age': 30} 
    )
    
    # Calling python function which uses sklearn package
    task2 = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn
    )
    
    # Calling python function which uses matplotlib package
    task3 = PythonOperator(
        task_id='get_matplotlib',
        python_callable=get_matplotlib
    )
    
    # Calling python function which returns a value
    # This value can be seen under Browse -> XComs
    task4 = PythonOperator(
        task_id='set_name',
        python_callable=set_name
    )

    # Reading the value from XComs (from another task)
    task5 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    # Calling python function which returns multiple value
    # This value can be seen under Browse -> XComs
    task6 = PythonOperator(
        task_id='set_multiple_values',
        python_callable=set_multiple_values
    )

    # Reading multiple values using XComs
    task7 = PythonOperator(
        task_id='get_multiple_values',
        python_callable=get_multiple_values
    )   
    
    task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7


5. This example contains the following
a. greet task -> with static variables
b. get_sklearn task -> calling sklearn python library
c. get_matplotlib task -> calling matplotlib python library
d. set_name task -> setting a variable using xcoms
e. get_name task -> getting the varibale set using xcoms
f. set_multiple_values task -> setting multiple variables using xcoms 
g. get_multiple_values task -> getting multiple variable set using xcoms 


5. Refresh the page containing our DAGs and see its execution by running it
Look into the log to see the values

Note: Max size of xcom=48M and must not be used to share large number of values

```


### Reference
```xml
https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT
https://airflow.apache.org/docs/apache-airflow/stable/index.html
https://coder2j.com/airflow-tutorial/airflow-task-life-cycle-and-airflow-architecture/
```
