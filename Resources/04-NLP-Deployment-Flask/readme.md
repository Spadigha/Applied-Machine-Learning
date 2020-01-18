# Create and activate pythonvirtual environment

```
python3 -m virtualenv venv
source venv/bin/activate
```
To deactivate
```
deactivate
```

# Add `.gitignore` for clean version control

- Goto `gitignore.io` website and search for the stacks, programming lnguages, IDEs you will use. Here, `xcode`, `python`, `flask`
- Click on `create`
- copy the text in `gitignore.io` file and save it in main directory (or child directory). You can even restrict folders from being comitted / pushed to github by adding the path to the folder or file at the end of the file. *Note: The path must be mentioned relative to the location of `.gitignore` file. For example, i don't want to include `venv` virtual environment folder in my commits. As it is in the same directory as `.gitignore` file, at the eof, i will mention `venv` in new line.*

*There is `venv` in this repo because it was committed before `.gitignore` was added. Doesn'r matter as it won't be updated with every commit / push*

# Deployment

- For deployment we have to use CI CD Pipeline
- We will use `Flask`, `Docker` and `gitlab`
![github-vs-gitlab](./comparison.jpg)

**1. Docker Installation**

*Note: If you are using windows, install ubuntu in virtual box and install docker in it. Docker is built for linux; Quite complicated in windows.*

- It is a PaaS product uses `OS-level virtualisation` to deliver softare packages called `containers`
- Install it to your linux (virtual) or Mac OS (refer official website. Easy steps.)
- check if it is running or not using `sudo docker run hello-world` (Internet connection required). You should see `Hello from Docker!`

**2. Jenkins Installation**

Jenkins is an open source Continous Integration platform - Crutial tool in DevOps Lifeycle.

- Don't install on top of docker. Install in host OS itself
- Written in java, so yo will require `jdk` to run it (download oracle jdk latest version from official website ). For MacOS, download `.dmg` file and install `.pkg` file that appears when clicked on it. check installation using `java --version`
- Install Jenkins latest version: `brew install jenkins-lts`
- Start jenkins service: `brew services start jenkins-lts`
- Restart jenkins service: `brew restart start jenkins-lts`
- After starting the Jenkins service, browse to `http://localhost:8080`
    - Install recommended plugins so that jenkins runs smoothly
    - Enter username or password that can be remembered easily. Eg. `admin`; `admin`
    - Youn will land on jenkins page. We will configure it when we will write our flask code and deploy it
    - Stop Jenkins: `brew services stop jenkins-lts`
    
    **3. GitLab Inastallation**
    
    GitLab is for hosting our code and it will give all CI CD tools like intergrating it with docker, jenkins, or any deployment tool like kubernetes.
    
    - We are going to install `GitLab` on top of docker itself.
    - Run `docker images` to see availabe images
    - You can pull (download) any image you want from dockerhub using command `docker pull`. Just search it in hub.docker.com. (Use CE - Community Edition)
    
    ```
    docker pull gitlab/gitlab-ce
    ```

    - Run the `GitLab Image` using docker
    ```
    docker run -d -p 443:443 -p 80:80 -p 22:22 --name gitlab1 gitlab/gitlab-ce
    ```
    
        `-d` : Run in background
        
        `-p host-port:docker-image-port` : Port configuration. GitLab has `three ports` we need to open - `443`, `80` (UI runs here), `22` (For all 3 ports).
        
        `--name name-of-container name-of-image` : `Name-of-container` can be anything you want.
    
    - Check running containers:
    
    ```
    docker ps
    ```
    
    - Check history: List all containers (and the images it was based on) that were run previously
    
    ```
    docker ps -a
    ```
    
    - Stop the running container. You can find `<container-id>` from `docker ps` or `docker ps -a`
    
    ```
    docker stop <container-id>
    ```

    - Start a container. You can find `<container-id>` from `docker ps` or `docker ps -a`. If not found in both commands, run using pulled gitlab image usng `docker run -d -p . . . . `
    
    ```
    docker start <container-id>
    ```

    - See logs: `docker logs`
    
    - After running the container or starting the container, goto `localhost:80` (where UI is hosted.) It may show error `502, Taking too long to respond`, but eventually it loads when you reload it or all by itself. Set simple 8 characters password like `adminadmin` and then register.
    
    
# Jenkins with Flask - Introduction
 
 We will create a pipeline to monitor our build and if there is any problem, that pipeline will be broken. In this part, we will create our pipeline.
 
 Flask is a lightweight web development micro web service framework. 
    - Easy to make APIs
    - WSGI Connector: Helps us connect our applications with client.
    - Easy, Intutive and pythonic

**Simle Example**

- Install Flask using `pip` in `venv`
```
pip install flask
```

- Import and create object
```
    from flask import Flask # import class
    app = Flask(__name__) # create object. 
                          # We will pass `__name__` of the `main` method
                          # at the end of the code.
    
    # create route (API)
    @app.route('/')
    def index():
        return 'Hello Flask!'
    
    
    # main method
    if __name__ == '__main__':
        app.run(port = 8090, debug = True) # alter port if necessary
    
```

Run the python file to launch the webapp.


**As everything is set now, we can happily code and deploy!!**


# Sentiment Analysis

See `FlaskApp/twitter-data-preproceesing.ipynb` file

# Flask

- Create **two** folders in main directory of flask app: 

    - `static` folder - Contains `.css` files and images.
    - `template` folder - default dir where `.html` file templates will be searched from.

- **BASIC FLOW**

    - `analysis.ipynb`: Do your data analysis in jupyter notebook
    
    - `model.py`: Clean the code from .ipynb file and use here
        - Create `model` using this script
        - Save `model` (and `mode._vectorizer`) using Pickle
        - Test prediction on single "String" entry

    - Templates
        - `home.html`: needs to have a form 
        ```
        <form action="{{ url_for('predict')}}" method="POST">
        ```
        when clicked on submit button, the form will be redirected to `action` link i.e `predict` route.
        
        -  `result.html`: 
        ```
        {% if prediction == 1%}
	    <h2 style="color:red;">It's a Negative Comment</h2>
	    {% elif prediction == 0%}
	    <h2 style="color:blue;">It's Positive Comment</h2>
	    {% endif %}
        ```
        the value for `prediction` is supplied by flask `return render_template('result.html', prediction = my_pred)` in `predict` route
    
    - `app.py`: It has two routes and helper functions
        - `home` route: redirects to `home.html` from where, when clicked on `submit`, we are redirected to `predict` route which directs to `output.html`
        - `prediction` route: `my_pred` is predicted based on input form `message` and is sent to `output.html` through `prediction = my_pred`.

# App Ready. Deployment Starts

**Base Image**
It is the operating system on which we will run our `docker container`. It needs base image as well which is specified by `FROM` in Dockerfile. It is created with the help of `Dockerfile` which contains all the information how our deployed enviroment will look like inside `container` when used on top of *this* image.

**Container**
It is the environment in which our `app` will be running. It is based on docker image (which was used to create the container using `docker run ...` command)

*Note: The docker container will exit when it has nothing to do. If you want to enter into the container terminal, you have to write a script to make it wait.*

`wait.sh`:
```
while true; do sleep 1000; done
```
`Dockerfile`
```
.
.
.

CMD ["chmod", "+x", "wait.sh"]
CMD ["sh", "wait.sh"]
```
**Difference between RUN, CMD and ENTRYPOINT:**

- **RUN** : These commands are run only(once) when image is built from Dockerfile `docker build -t <image-name> .`.

- **CMD** : These commands are run everytime when docker container is run or restarted. You can do anything with it's help everytime containers starts or restarts. (like executing `wait.sh` script to enter container terminal)

- **ENTRYPOINT** :  
This syntax is used in Dockerfile to fire up flask app
```
ENTRYPOINT ["python"]
CMD ["app.py"]
```


## Procedure 

- We need a base image from docker hub on top of which we will create our own image. I am using `publysher/alpine-numpy:1.14.0-python3.6-alpine3.7`

- Create image based on `./Dockerfile`:

Goto your working directory and create `Dockerfile` in main folder
```
FROM publysher/alpine-numpy:1.14.0-python3.6-alpine3.7

# --------[ alpine-3.7 and python-3.6.5 dev tools installation ]-------- 
# multiple pip install lines to avoid 
# pkg dependancy issues
# scipy==1.0.0 for pickle loading issues
# for pickle issues, build .pkl file wih the same sklearn version
# you will be using to load it
# ALWAYS DO PIP INSTALLS IN IMAGE `RUN`
# NOT IN CONTAINERS
RUN apk --no-cache add lapack libstdc++\
    && apk --no-cache add --virtual .builddeps g++ gcc gfortran musl-dev lapack-dev\
    && pip install cython \
    && pip install scipy==1.0.0 \
    && pip install scikit-learn==0.21.3 \
    && pip install pandas flask nltk \
    && pip install pickle5 \
    && apk del .builddeps \
    && rm -rf /root/.cache

# ---------[ dev tools installation comlpete ]-------------------------

# creates `/app` folder inside container's root that will be
# used as our working dir inside the container
WORKDIR /app

# copies all our sourcecode from current dir (.) to
# the container.
COPY . /app

# try this. But will take time as it has to 
# build from spurce in alpine (unlike ubuntu). 
# There might aswell be
# version match issues. idk.
#RUN pip3 install -r requirements.txt

# opens up port 4000 to the world outside container
EXPOSE 4000

# build `model.pkl` with scipy and scikit-learn==0.21.3
# installed so that while loading it with pickle,
# there aren't any issues
RUN python model.py

# ----------------[ use as it is ]----------------------
# defined for running flask
# Use this only. Don't use `wait.sh` with this
# contents of ./wait.sh : `while true; do sleep 1000; done`
ENTRYPOINT ["python"]
CMD ["app.py"]
# ------------------------------------------------------

# Wait script which will help to get into container's 
# bash. Un comment it ONLY if flask is not running or
# docker is exiting. This makes container run so that we
# can get into it (As we cannot enter exited container's bash) 
#CMD ["chmod", "+x", "wait.sh"]
#CMD ["sh", "wait.sh"]



# =================[TERMINAL-COMMANDS]==============================
# 1. Create image:
#   docker build -t flask-nlp-basic-image:v1 .
# 2. Run container based on image: <outside-port>:<container port>
#   docker run -p 5000:4000 -d --name flask-test-container flask-nlp-basic-image:v1
# 3. make container wait so that we can enter it's terminal.
#   Use it only if container is exiting or Flask app NOT runing
#   CMD ["chmod", "+x", "wait.sh"]
#   CMD ["sh", "wait.sh"]
# 4. Enter into container:
#   docker exec -it <container-id> /bin/sh

```


# CI-CD Pipeline - Jenkins configuration

### **1. Push code to Gitlab & make Jenkins freestyle project.**

**Push code to Gitlab**

Gitlab provides all devops features. All enterprises are moving towards it. 

It is an enterprise level complete DevOps application where a developer can push his code and maintainer can make changes to the deployed app based on pushes from developers. CI-CD pipelines are available, you can even integrate Gitlab with Kubernetes. 


We will understand how end to end pipline works. End to end pipeline means getting the code, dockerizing it - build image and run container and then testing (We will do all this using **Jenkins** in gitlab)

i. Start both Jenkins(from system) and Gitlab(from docker) - *see above docs to know how to start and configure them.*

ii. Jenkins:

- You should see `Welcome to Jenkins!` after logging in

- Click on ⚙️ `Manage Jenkins`(on left side of windows) -> 🧩`Manage Plugins` -> (Click on) `Available` -> Search in the field on top right corner `Filter 🔍` : `gitlab` 

    - If you already have the `"GitLab Plugin"` and `"Generic Webhook Trigger Plugin"` installed, it won't be shown in the `Available` List, change to `Installed` list (Just beside `Available`.)

    - If you haven't installed it already, it should be visible in `Available` List... Select and Install `"GitLab Plugin"` and `"Generic Webhook Trigger Plugin"`
    *After installing Plugins, restart your Jenkins.*

iii. GitLab:

- It may take some time to open, wait and then login 

- Click on `Create a project`:
    ```
    Project name: my-nlp-model
    Visibility Level: public (can integrate easily with Jenkins without password)
    ```
    - You will be redirected to `Command line instructions` page. Stay still don't click on anything.

    - Before uploading your project folder (in your local file system), make sure it is not connected to any git repo by -

    In terminal, `cd` into your project foder
    ```
    # check git version
    >> git remote -v
    
    # if (fetch) and (push) urls exist, remove
    # it using
    >> sudo git remote rm origin

    # check again (This time there should be nothing)
    >> git remote -v
    ``` 

    - Link your project folder(in local system) to GitLab repo
    ```
    >> git init

    >> sudo git remote add origin http://0.0.0.0/rakesh4real/my-nlp-model 

    # check if linked or not.
    # (fetch) and (push) links must appear
    >> git remote -v
    ```
    *where, `http://0.0.0.0/rakesh4real/my-nlp-model` is from url field of your gitlab repo's `Command line instructions` page*

    - add, commit, push (with sudo)
    ```
    >> sudo git add .
    >> sudo git commit -m"initial commit"
    >> sudo git push origin master
    username: root
    password: adminadmin
    ```

    - refresh your `Command line instructions` page in GitLab tab to see changes.

- Steps to clone created repo and check how `Jenkins` is performing:
    
    - Goto, `Jenkins` browser UI and click on 📦`New Item` in left side.

    - Fill `Enter an item name :` feild with `simple build` and select `Freestyle project` available below.
    
    *`Freestyle project`(comes by default) is not meant for complex tasks and creating pipelines. Used to only build our particular software application*

    - Click `OK`

    - You will land into another page. 
    
    - Goto `General` -> `Source Code Management` -> (Select) `Git`-> (copy and paste repo url from url field of GitLab UI) `Repository URL`.
    (No need to fill any `Credentials` as this is a *public* repo)

    - (skip all and go to bottom of `General`) To `Build` -> `Add build step` -> `Execute shell` -> `Command:` (fill the following -)
    ```
    whoami
    ```

    - Click on `Save`. You will be redirected to main page

    - Again in left side, click 🕙`Build Now`. This will start build process which you can see in ☀️`Build History` displayed just below.

    - Click on ☀️`Build History` -> `#1` -> `Console Output`

    - You can see console output where project dir is fetched/cloned and our command `whoami` is run.

    - If you goto  ⬆️`Back to Project` -> 📁`Workspace`, you can see your cloned repo.

    - `Jenkins` is able to connect to our `Gitlab`!!

- Before making a pipleline, create `Jenkinsfile` which stores instructions that needs to be run.


### **2. Making `Jenkinsfile` and creating Jenkins Pipeline**

For creating Jenkins pipeline, we need to create `Jenkinsfile`.

- Goto your project directory and create `Jenkinsfile` in main dir:

./Jenkinsflie: (write something and push. We will edit from GitLab itself)
```
pipeline
```

In terminal:
```
>> git stauts
>> git add .
>> sudo git commit -m"Jenkins file added"
>> git push origin master

(Note: `origin master`)
```

- Now check from GitLab UI inside repo and you will find `Jenkinsfile`. Edit it from here.

    - For any given pipeline, there are different `stages`. Under `stages` we can declare n - number of stages

    - Inside stages, there are `steps`. In `steps` you can write any command or shell-script you want using `sh ' '`.

    ```
    pipeline {
        agent any
            stages {
                
                stage('Clone Repository') {
                    
                    /* Clone the repo of our workspace as `scm` means source-code-management*/
                    steps {
                        checkout scm
                    }
                }
                
                stage('Build Image') {
                    steps {
                        sh 'sudo docker build -t my-nlp-model:v1 .'
                    }
                }
                
                stage('Run Image Inside Container') {
                    steps {
                        sh 'sudo docker run -d --name nlp-model1 my-nlp-model:v1'
                    }
                }
                
                /* Last Stage - Test whatever you want */
                stage('Testing') {
                    steps {
                        echo 'Testing...'
                    }
                }
            }
    }
    ```

    - `Commit Changes` (update Jenkinsfile)

**Create Pipeline Using Jenknsfile:**

- Goto, `Jenkins` browser UI and click on 📦`New Item` in left side.

- Fill `Enter an item name :` feild with `My NLP Pipeline` and select `🚰 Pipeline` available below (Not Freestyle prject which is default).

- `OK`

- (Don't put anything except this: )`General` -> `Pipeline` -> Definition: `Pipeline script from scm` -> SCM: `Git` -> Repositories: Repository URL: `http://0.0.0.0/rakesh4real/my-nlp-model` -> (no need to put any credentials as *public* repo) -> (It will automatically check) Script Path: `Jenkinfile` (in the end) -> `Apply` -> `Save`

- You will be redirected to main page. Again in left side, click `🕙Build Now`. This will start build process which you can see in ☀️`Build History` displayed just below.

