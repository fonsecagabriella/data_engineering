# Setting Up The Environment

## Google Cloud Platform

1. Create a project in your Google Cloud Platform

2.  Look for VM instances 
You might need to enable it. 
Since it's a new project, it will be empty.

docker run -it ubuntu bash
    ubuntu is the image
    bash is a parameter (everything that comes after the image is a parameter)

docker run -it python3:9
    get python prompt
    to get out CTRL+D

to execute bash commands in python docker
    docker run -it --entrypoint=bash python3.9

to save an image:
    create a dockerfile and specify the commands there
    build
         docker build -t test:pandas .
        (here test is the name of the image, after : is the version)
    run
        docker run -it test:pandas
    
    -- if you change anything in a dockerfile need to build it again

## LET OP: TIPS ‼️
- don't use comments in the same line in the docker file or you will hace issues in building / running imagr
- Extra spaces and missing backslash will give you issues when running commands on the shell no spaces should exist around the = in key-value pairs

## USEFUL BASH commands ⌨️ 
pwd shows current directory
wget <link> download file
less <file> take a look at the start of a text file
head -h <number> <file>  shows first <number> lines of a dataset
wc -1 <file> counts how many rows in a file

## USEFUL Docker 🐟
docker ps: shows what is running
docker network create pq-network // creates a network to connect postgres to 
docker stop pg_database // stop container
docker rm container //  remove container
docker system prune -f // stop all running containr, removed unused networks, free allocated ports
docker-compose down // kills docker compose


## Connect to POSTGRES 
pgcli -h localhost -p 5432 -u root -d ny_taxi -W
-h for localhost -p for port, -d for database -W to enforce password



--> ORDER TO CHECK DB LOCALLY
Run postgre container (create if does not exist)
use the pgci command line
If want to use the pg-admin, create 

--> TO FEED THE DATA TO THE DB
You run the file "script populate" line by line

## Convert jupyter file to python script
Go to the command line:
jupyter nbconvert --to=script <filename>

## NOTE:
Docker compose creates a network of images based on what you set on file



