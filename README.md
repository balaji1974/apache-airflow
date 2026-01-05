
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

## Task Lifecycle - Architecture

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

4. Optimize the docker compose as given in the project directory 
to remove unnecessay dependencies

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


### Reference
```xml
https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT
https://airflow.apache.org/docs/apache-airflow/stable/index.html


```
