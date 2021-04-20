# AI Workflow Capstone - Setup

The project runtime consists of a Python Flask Application and associated modules that are deployed to a Docker container. The following steps provide instructions to setup, deploy and test the runtime.


## Step 1 - Clone / Download Repository

Clone and/or download the repository on to your preferred directory on your local machine. The commands in the subsequent steps are executed from this directory.

## Step 2 - Basic Unit Tests

Execute the following to start the Flask app
```
python app.py
```
and then open http://localhost:5000/ in your browser to check if the application is running.

Execute the following to test the model
```
python model.py
```

## Step 3 - Build the docker container

Execute the following commands to create the image
```
docker build --pull --rm -f "Dockerfile" -t aiworkflowcapstonesanujit:latest "."
```

Verify if the image was created successfully
```
docker image ls
```

Run the image in a container
```
docker run -p 5000:5000 aiworkflowcapstonesanujit
```

and then open http://localhost:5000/ in your browser to check if the application is running.

## Step 4 - Run the unit tests

Run the API unit tests
```
python test_api.py
```

Run the model unit tests
```
python test_model.py
```

Run the logger unit tests
```
python test_logger.py
```

Run all the unit tests at once
```
python test_all.py
```
