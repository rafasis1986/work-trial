# Starter​ Project 
#​@ Data Quality Team

## RESUME


## DEPLOY

### Technical description

The project consists in one CLI application to get all ssr and PRID abortables.

## Settings

**Prerequisites**

-   [Python 2.7.10+](https://www.python.org/downloads/release/python-2713)
-   [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
-   [Docker 17.04.0+](https://docs.docker.com/engine/installation/)
-   [Docker-Compose 1.14.0+](https://docs.docker.com/compose/install/)

If you have your own database server pass over the docker instruccions, but remember that you need adjust the enviroment in your operative system with same variable names that you watch in the file ```env.prod``` 

```

export DB_HOST="127.0.0.1"
export DB_USER="root"
export DB_PASSWORD="root"
export DB_NAME="worktrial"
export DB_PORT=3307
export DAYS_EXPIRES=18

```

*You can change any settings by your prefer value*

To charge this values in your enviroment type the comand

```sh
$ source env.prod
```

Before to deploy your docker container you need copy all your csv files to the folder  ```data/initial```. Now you can deploy your dockerized database, even I added the [adminer](https://www.adminer.org/) image in the docker-compose script to use it in case that you don't have any mysql client in your host.

```sh
$ docker-compose up -d
```
When you need check the containers status use
```sh
docker-compose ps
```
Even you can use a lot of comands with your containers, if you want please read more about docker in the official page.

and finally to stop all the compose container use:

```sh
$ docker-compose stop
```

Finally to deploy the application we need previously install the python virtual enviroment I recomend use the *virtualenvwrapper* because you only need set some rules in your .bash_profile or .bashrc, to create and install all dependencies you use the next two sentences:

```sh
$ mkvirtualenv worktrial -p python

(worktrial) $ pip install -r requirements.txt
```

Right now your enviroment are ready to deploy the CLI application with the comand

```sh
(worktrial) $ python main.py
```

## Unit Test

To deploy the unittest I use the nose test pakage and to deploy the enviroment you need some steps like the previous stage and like it if you don't want install any dockerized database please skip these sentences.

``` sh
$ docker-compose -f test.yml up -d
```

The docker compose file to test enviroment is *test.yml* and by this reason we need specify with ```-f``` the script, and like the previous enviroment you can use the sames sentences with the only condition that you need add the -f argument.

Later you need set your enviroment variables, you can use the ```env.test``` file.

```sh
$ source env.test
```

Additionally you need use or crete the python enviroment, to finally deploy the test suite use the nex sentences.

```sh
$ workon worktrial

(worktrial) $ nosetests -v
```

The *-v* arg is to added verbosity to output test and if every is fine you can watch some like it.


```
test.test_get_samples_id ... ok
test.test_get_aborted_ssr_list ... ok
test.test_get_pending_ssr_list ... ok
test.test_abortable_ssr_with_results ... ok
test.test_get_exclude_samples ... ok
test.test_prid_abortables_without_legacy ... ok
test.test_prid_abortables_with_legacy ... ok

-------------------------------------------------------------
Ran 7 tests in 0.164s

OK

```
