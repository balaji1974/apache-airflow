
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
### dag_with_bash_operator.py
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
### dag_with_python_operator.py
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

4. All dags are created under the dags folder.
Under this folder create a file called dag_with_python_operator.py
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


6. Refresh the page containing our DAGs and see its execution by running it
Look into the log to see the values

Note: Max size of xcom=48M and must not be used to share large number of values

```

## Create DAG with taskflow API
### dag_with_taskflow_api.py
```xml 
A TaskFlow API is a modern way to build data workflows (DAGs) using Python functions 
and decorators (like @task) to define tasks, making code cleaner, more readable, and 
reducing boilerplate by automatically handling data passing (XComs) and task 
dependencies, essentially turning Python functions into manageable, connected steps 
in a workflow. It simplifies creating Extract, Transform, Load (ETL) pipelines by 
letting you pass return values from one function as arguments to the next, with 
Airflow managing the underlying data movement. 

1. All dags are created under the dags folder.
Under this folder create a file called dag_with_taskflow_api.py
with the following content:
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'Balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_v2', 
     default_args=default_args, 
     start_date=datetime(2021, 10, 26), 
     schedule='@daily')
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Balaji',
            'last_name': 'Thiagarajan'
        }

    @task()
    def get_age():
        return 45

    @task()
    def greet(first_name, last_name, age):
        print(f"Hello World! My name is {first_name} {last_name} "
              f"and I am {age} years old!")
    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], 
          last_name=name_dict['last_name'],
          age=age)

greet_dag = hello_world_etl()


2. Refresh the page containing our DAGs and see its execution by running it
Look into the log to see the values


```

## Create DAG with Catchup and Backfill
### dag_with_catchup_and_backfill.py
```xml 
Catchup: This is an automatic feature of the Airflow scheduler (enabled by default) 
that runs all the missed DAG runs between the start_date defined in the DAG and the 
current date/time when the DAG is unpaused or deployed.
catchup=False: If historical runs are not needed (e.g., if the DAG is processing 
the most current data regardless of interval), the catchup parameter can be set to 
False in the DAG definition. This tells the scheduler to only run the DAG for the 
latest interval. 

Backfill: This is a manual, on-demand process, usually initiated via the command-line 
interface (CLI) or API, that runs the DAG for a specific, user-defined historical 
date range, regardless of the DAG's catchup parameter setting. 
Specific Intervals: Unlike catchup, which runs all missed runs from the start_date, 
backfill allows you to pick a specific interval in the past 
(e.g., just last week's data).

1. Catchup (Note: catchup=True)
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


default_args = {
    'owner': 'balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_catchup_backfill_v01',
    default_args=default_args,
    start_date=datetime(2025, 12, 31),
    schedule='@daily',
    catchup=True
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple bash command!'
    )


2. Refresh the page containing our DAGs and see its execution by running it
Look into the log to see the values

3. Backfill: 
docker ps
docker exec -it <container-id> bash
airflow backfill create --dag-id dag_with_catchup_backfill_v01 --from-date 2025-12-31 --to-date 2026-01-10

```

## Create DAG with cron expression
### dag_with_cron_expression.py
```xml 
A cron expression is a string of characters defining a schedule for automated tasks, 
specifying when commands or scripts should run, typically using five or six fields 
for seconds, minutes, hours, day of month, month, and day of week, with special 
characters like * (any value) and / (interval) to set repeating patterns 
(e.g., 0 0 * * * runs daily at midnight) 

Ref the below link for easy cron creation:
https://crontab.guru/

1. Create the DAG
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


default_args = {
    'owner': 'balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id="dag_with_cron_expression_v04",
    start_date=datetime(2026, 1, 5),
    schedule='0 3 * * Tue-Fri'
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command="echo dag with cron expression!"
    )
    task1

2. Refresh the page containing our DAGs and see its execution by running it
Look into the log to see the values

```

## DAG connection to database
### dag_with_sql_operator.py
```xml 
1. Expose the Postgres Database by adding the ports to the existing Postgres
service in our docker-compose.yaml
services:
  postgres:
    ports:
      - "5432:5432"

2. Build the postgres container
docker compose up -d --no-deps --build postgres

3. Check the connection using PgAdmin by creating a new connection
Register -> Server 
Name: airflow

Connection (tab)
HostName: localhost
Port: 5432
Maintainance DB: airflow
UserName: airflow
Password: airflow

Save and Test the connection 

4. Once connected right click on the database
Create New Database: test

5. Create a DAG Connection from our airflow console page
Admin -> Connection
Connection ID: postgres_localhost
Connection Type: postgres
Host: postgres (our service name in docker or host.docker.internal or localhost if exposed outside)
Login: airflow
Password: airflow
Port: 5432
Database: test
Save

6. Create our sql operations DAG
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    'owner': 'balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='dag_with_sql_operator_v1',
    default_args=default_args,
    start_date=datetime(2025, 12, 31),
    schedule='0 0 * * *'
) as dag:
    task1 = SQLExecuteQueryOperator(
        task_id='create_table',
        conn_id='postgres_localhost',
        sql="""
            create table if not exists dag_runs (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )

    task2 = SQLExecuteQueryOperator(
        task_id='insert_into_table',
        conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )

    task3 = SQLExecuteQueryOperator(
        task_id='delete_data_from_table',
        conn_id='postgres_localhost',
        sql="""
            delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        """
    )
    task1 >> task3 >> task2


7. Run the DAG from the console by enabling it and check 
if it has run successfully.

8. Check the test database to see if the table is created 
and a record has been inserted 

```

## Installing additional Python packages
```xml 
Extending vs Customization 
The distinction between extending and customization in the context of Python packages 
revolves around whether you are adding functionality externally or modifying the 
internal workings. 

Extending
---------
Extending is the standard, best-practice approach. 

Methodology: 
This involves building new code that imports and leverages existing packages, 
adding features, or creating new modules that work alongside the original.

Best Practices:
Use virtual environments: Isolate dependencies for different projects.
Create a separate package: Build a new, dependent package that uses the original package as 
a dependency.
Utilize inheritance/wrapper functions: Create new classes or functions that wrap or inherit 
from the original package's components to add features.

Benefit: The original package remains untouched, allowing for seamless updates without breaking 
your added functionality. 

Example:
1. Create a requirements.txt file in the project root folder and add your dependencies:
scikit-learn==1.8.2
matplotlib==3.10.8

2. Create a Dockerfile and add the following:
FROM apache/airflow:3.1.5
COPY requirement.txt /requirements.txt 

RUN pip install --user --upgrade pip 
RUN pip install --no-cache-dir --user -r /requirements.txt

Save it

3. Build the image
docker build . --tag extending-airflow:latest

4. Change the image to the newly built one inside the docker-compose.yaml
x-airflow-common:
  &airflow-common
  image: ${AIRFLOW_IMAGE_NAME:-extending-airflow:latest}

Save it

5. Now you can create a new DAG file that can use the imports that were added

6. Rebuild the airflow dag processor and scheduler services using this new image
docker-compose up -d --no-deps --build airflow-scheduler airflow-dag-processor

7. Refresh the page and run the task


Customization
-------------
Customization, in this context, refers to directly modifying a third-party package's source code. 
This practice is strongly discouraged. 

Methodology: 
Manually editing files in the site-packages directory or maintaining a private fork with local changes.

Drawbacks:
Difficult updates: Updating the original package (via pip install --upgrade) will likely overwrite 
your custom changes.
Version conflicts: Your customized version might become incompatible with other dependent packages.
Deployment issues: Sharing your project becomes complex, as others would also need your exact custom 
modifications. 

Example:
1. Clone the official airflow image
git clone https://github.com/apache/airflow.git

2. Open it in VSCode
Inside the docker-context-files folder
create a requirements.txt file
scikit-learn==1.8.2
matplotlib==3.10.8

3. Build the image
docker build . --build-arg AIRFLOW_VERSION='3.1.5' --tag customizing_airflow:latest

4. Change the image to the newly built one inside the docker-compose.yaml
x-airflow-common:
  &airflow-common
  image: ${AIRFLOW_IMAGE_NAME:-customizing_airflow:latest}

5. Now you can create a new DAG file that can use the imports that were added

6. Rebuild the airflow dag processor and scheduler services using this new image
docker-compose up -d --no-deps --build airflow-scheduler airflow-dag-processor

7. Refresh the page and run the task


In summary, extend the functionality by building on top of existing packages and 
using virtual environments, and avoid customization of installed packages whenever 
possible. If internal modifications are unavoidable, use the "editable" install mode 
(pip install -e path/to/SomePackage) to work on the source code in a development 
directory under version control

Use extend in 99% of time and choose customization only if extending is not possible and 
you care about image size optimization. 

```

## Airflow AWS S3 sensor 
### sensor-s3.py
```xml 
Sensor is a special type of operator which waits for something to occur 
It is event based and used when the exact time is not know for tigger 

Minio
MinIO is a high-performance, open-source object storage server that's fully compatible 
with the Amazon S3 API, designed for modern cloud-native applications, AI/ML, analytics, 
and data-intensive workloads. 



```

### Reference
```xml
https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT
https://airflow.apache.org/docs/apache-airflow/stable/index.html
https://coder2j.com/airflow-tutorial/airflow-task-life-cycle-and-airflow-architecture/
```
