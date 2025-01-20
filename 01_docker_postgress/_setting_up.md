# Setting Up The Environment

## Google Cloud Platform

1. Create a project in your Google Cloud Platform

2.  Look for VM instances
You might need to enable it.
Since it's a new project, it will be empty.


## Docker 🐟

## TIPS 🔔
- Don't use comments in the same line in the `dockerfile` or you will have issues in building / running your image
- Extra spaces and missing backslash will give you issues when running commands on the shell no spaces should exist around the = in key-value pairs
- CTRL+D to end process in the shell
- 🚨 **If you change anything in a dockerfile you need to build it again**
- SHELL is how you interact with command line. You can check which shell you are using run `echo $SHELL`

### Simple commands to build understanding
`docker run -it ubuntu bash`
    - ubuntu is the image
    - bash is a parameter, your entryoint (**everything that comes after the image is a parameter**)

`docker run -it python3:9`
    - create and run a interactive container with python 3.9
    - **TIP: CTRL+D to end process**


`docker run -it --entrypoint=bash python3.9`
    *to execute bash commands in python docker*
    - image: python
    - entrypoint: bash (you can run `pip install` directly if you start this container, foc example)

#### **To save an image:**

**Option 01:** create a dockerfile and specify the instructions such as in `../dockerfile` 

**Option 02:**
    - **Build the image**
         `docker build -t test:pandas .`
        Eplanation: Here *test* is the name of the image, after the *:* is the version (in this case *pandas*))
    - **Run the image you built**
        `docker run -it test:pandas`

🚨 **If you change anything in a dockerfile you need to build it again**

## USEFUL BASH commands ⌨️ 
`pwd` shows current directory
`wget <link>` download file
`less <file>` take a look at the start of a text file
`head -h <number> <file>`  shows first <number> lines of a dataset
`wc -1 <file>` counts how many rows in a file

## USEFUL Docker 🐟
`docker ps:` shows what is running
`docker network create pq-network` // creates a network to connect postgres to 
`docker stop pg_database` // stop container
`docker rm container` //  remove container
`docker system prune -f` // stop all running containr, removed unused networks, free allocated ports
`docker-compose down` // kills docker compose


## Connect to POSTGRES with pgcli
Run the command in the shell and you will be able to interact with the database via the shell.

`pgcli -h localhost -p 5432 -u root -d ny_taxi -W`

*Explanation:*
    -h for localhost 
    -p for port, 
    -d for database 
    -W to enforce password



--> ORDER TO CHECK DB LOCALLY
Run postgre container (create if does not exist)
use the pgci command line
If want to use the pg-admin, create 

--> TO FEED THE DATA TO THE DB
You run the file "script populate" line by line

## Convert jupyter file to python script
Go to the command line:
`jupyter nbconvert --to=script <filename>`

## NOTE:
Docker compose creates a network of images based on what you set on file



