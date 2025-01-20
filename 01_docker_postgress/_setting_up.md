# Setting Up The Environment

**You need to:**
1. Get a GitHub Account and install VSCode, connecting both (*maybe obvious step*)
2. Install Brew (*I like having al my packages managed by brew, not a requirement, but can make it easier*)
3. Install Anaconda
4. Install Docker (via Brew or installer)
5. Follow the innital Docker videos (about 15 minutes to complete)
6. Install terraform (via Homebrew)

## Index
0. [Anaconda 🐍](#anaconda-🐍)
1. [Google Cloud Platform](#google-cloud-platform)
2. [Docker 🐟](#docker-🐟)
3. [TIPS 🔔](#tips-🔔)
   - [Intro to Docker Concepts](#intro-to-docker-concepts)
     1. [Image](#1-image)
     2. [Container](#2-container)
     3. [Registry](#3-registry)
   - [Simple Commands to Build Understanding](#simple-commands-to-build-understanding)
   - [To Save an Image](#to-save-an-image)
4. [USEFUL BASH Commands ⌨️](#useful-bash-commands-⌨️)
5. [USEFUL Docker 🐟](#useful-docker-🐟)
6. [Connect to POSTGRES with pgcli](#connect-to-postgres-with-pgcli)
7. [Convert Jupyter File to Python Script](#convert-jupyter-file-to-python-script)



## Anaconda 🐍


Since you’ve already installed Anaconda with Homebrew, follow these steps to set it up:
- Verify Anaconda Installation:
`conda --version`
If this works, Anaconda is installed properly. If not, ensure it is added to your system's PATH.

- Create a Python 3 Environment:
`conda create --name data_engineering python=3.10`
Replace data_engineering with your preferred environment name.

- Activate the Environment:
`conda activate data_engineering`


- Test Python Installation:
`python --version`
Ensure it outputs a Python 3 version.

If there is an issue with homebrew:

````
conda config --set auto_activate_base false
conda activate base
````


## Google Cloud Platform

1. Create a project in your Google Cloud Platform

2. Look for VM instances  
   You might need to enable it.  
   Since it's a new project, it will be empty.

## Docker 🐟

Docker is a tool that helps you package your application and everything it needs (like libraries, tools, and settings) into a container. A container ensures your application will run the same way, no matter where you run it.

## TIPS 🔔
- Don't use comments in the same line in the `dockerfile` or you will have issues in building / running your image.
- Extra spaces and missing backslash will give you issues when running commands on the shell. No spaces should exist around the `=` in key-value pairs.
- CTRL+D to end process in the shell.
- 🚨 **If you change anything in a dockerfile/yaml you need to build it again.**
- SHELL is how you interact with the command line. You can check which shell you are using by running `echo $SHELL`.
- **Docker compose** creates a network of images based on what you set on the file `.yaml`:  
  `docker compose up -d --build`
(*so if you're using docker compose you don't need to manually create the network like we did in the first videos*)
- A container should do only one thing (and do it well).

### Intro to Docker concepts

#### 1. Image
Think of an image as a recipe for a dish. It contains all the instructions and ingredients your app needs to run:
- The code for your app.
- Tools and libraries it depends on.
- The operating system (a lightweight version).

You create an image once, and it’s reusable.

#### 2. Container
A container is like the cooked dish made from the recipe. It’s the actual, running instance of your app.
- You can run many containers from the same image, just like you can make multiple dishes from one recipe.
- Each container is isolated, so one doesn’t mess with another.

#### 3. Registry
A registry is like a cookbook store where you keep and share your recipes (images).
- Docker Hub is the most popular registry, where people share ready-to-use images.
- You can pull images from a registry to your kitchen (computer) to use, or push your own recipes to share.

**How They Work Together**
- **Create an Image:** You write a recipe (called a Dockerfile) that describes your app and its setup. Docker builds this into an image.
- **Store in a Registry:** You save the image in a registry so it can be shared or used later.
- **Run a Container:** You take the image from the registry and use it to start a container (a running instance of your app).

### Simple Commands to Build Understanding

`docker run -it ubuntu bash`  
- ubuntu is the image.  
- bash is a parameter, your entry point (**everything that comes after the image is a parameter**).

`docker run -it python3:9`  
- Create and run an interactive container with Python 3.9.  
- **TIP: CTRL+D to end process.**

`docker run -it --entrypoint=bash python3.9`  
- To execute bash commands in Python Docker.  
- Image: Python.  
- Entrypoint: bash (you can run `pip install` directly if you start this container, for example).

#### **To Save an Image:**

**Option 01:** Create a dockerfile and specify the instructions such as in `../dockerfile`.

**Option 02:**  
- **Build the Image**:  
  `docker build -t test:pandas .`  
  Explanation: Here *test* is the name of the image, and after the *:* is the version (in this case *pandas*).  
- **Run the Image You Built**:  
  `docker run -it test:pandas`

🚨 **If you change anything in a dockerfile you need to build it again.**

## USEFUL BASH Commands ⌨️

- `pwd` shows current directory.
- `wget <link>` downloads a file.
- `less <file>` takes a look at the start of a text file.
- `head -h <number> <file>` shows the first <number> lines of a dataset.
- `wc -l <file>` counts how many rows in a file.

## USEFUL Docker 🐟

- `docker ps`: Shows what is running.
- `docker network create pq-network`: Creates a network to connect Postgres to.
- `docker stop pg_database`: Stops a container.
- `docker rm container`: Removes a container.
- `docker system prune -f`: Stops all running containers, removes unused networks, and frees allocated ports.
- `docker-compose down`: Kills Docker Compose.

## Connect to POSTGRES with pgcli

Run the command in the shell, and you will be able to interact with the database via the shell:

`pgcli -h localhost -p 5432 -u root -d ny_taxi -W`

*Explanation:*  
- `-h` for localhost.  
- `-p` for port.  
- `-d` for database.  
- `-W` to enforce a password.

🡠 **ORDER TO CHECK DB LOCALLY**
1. Run Postgres container (create if it does not exist).
2. Use the `pgcli` command line.
3. If you want to use pgAdmin, create a container/start it.

🡠 **TO FEED THE DATA TO THE DB**
- Run the file "script populate" line by line.
- Or create a script and then create a container using the script.

## Convert Jupyter File to Python Script

Go to the command line:  
`jupyter nbconvert --to=script <filename>`

