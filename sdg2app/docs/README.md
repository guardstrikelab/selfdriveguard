# Installation

## Setup from source

Prerequisites:
- Python3.8


Enter project root folder:
```
cd sdg2app
```

Install python dependencies:
```
pip install -r requirements.txt
```

> Use command below if the original connection is slow:
>```
>pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
>```

Setup configurations in src/sdgApp/conf.ini.

Run:
```
python src/sdgApp/main.py 
```
The service will be hosted at [0.0.0.0:8000](0.0.0.0:8000) by default. Open [127.0.0.1:8000/docs](127.0.0.1:8000/docs) to check the API document page.

## Setup by docker-compose

Prerequisites(only tested threw below environment):
- docker==20.10.7
- docker-compose==1.27.4


Update images:
```
docker-compose rm -f
docker-compose pull
```
Setup configurations (environment variables) in docker-compose.yml.

Run:
```
docker-compose up -d
```
The service will be hosted at [0.0.0.0:8000](0.0.0.0:8000) by default. Open [127.0.0.1:8000/docs](127.0.0.1:8000/docs) to check the API document page.

Stop:
```
docker-compose stop
```

Additional, if you want to build your own docker image, run:
```
docker build -t myimage .
```

# Usage

sdgApp is responsible for defining user interface and routing the command from the user. The actual execution unit is other related microservices such as sdgEngine. If you want to test or run all the functionalities through the whole platform, Please correctly setup all other services and run the demo down below.

## Integrated api document

Now that the service is running at [0.0.0.0:8000](0.0.0.0:8000), you can open [127.0.0.1:8000/docs](127.0.0.1:8000/docs) to try our API.

First, go to `auth` section and click `/auth/register`, click "Try it out" and fill in the request body. 
Click "Execute", then this account will be registered.

Then scroll up to the top of the page and click the "Authorize" button decorating with a small lock which is unlocked.
Fill in the email and password(ignore other fileds), and click "Authorize". Now you are logged in and you are free to try all the apis.

Find `users` section then execute the `/users/me` api to get your rootfolder id. After that, you can create scenarios within the folder, create tasks based on some scenarios and create jobs based on some tasks.

## Jupyter notebook
You can try out our apis using a jupyter notebook.

Install jupyter notebook:
```
pip install jupyter
```
> Use command below if the original connection is slow:
>```
>pip install jupyter -i https://pypi.tuna.tsinghua.>edu.cn/simple
>```

Enter demo folder:
```
cd demo
```

Run:
```
jupyter notebook
```

In the notebook homepage, open "SDG2.0 Demo.ipynb".
More details are presented within the notebook.

# Develop

Run test before commit. Run formatter before commit. Write good code for you and me.

## Unit test

Make sure pytest has been installed, if not , install it:
```
pip install pytest
```

In the project root folder, run:
```
pytest tests/unit
```

Make sure all cases are passed before you commit code.

## Formatter

We obey the PEP8 standard.

Make sure yapf has been installed, if not , install it:
```
pip install yapf
```

In the project root folder, run:
```
yapf -i -r --style pep8 .
```

> -i means it will make changes to files
>
> -r means it will run recursively over directories
>
> More usage see: [Google YAPF](https://github.com/google/yapf#usage)

Run formatter before you commit code.