### How to sam accelerate work with lambda layers

If you are a developer, you know testing is very important for application development. But integration testing in cloud is really a concern. As deployment time plays a vital role in development, many of us try to do mock test before deploy it into cloud. There are some frameworks for doing that. But in that case integration testing is not possible. If you are a SAM user, you can speed up your development with SAM accelerate. In this blog post, you will see an example of lambda layers and its implementation in sam accelerate.  



<img width="1115" alt="image_1" src="https://user-images.githubusercontent.com/63281366/223938791-5ae4d30e-4379-4edb-9658-985635ec186e.png">


### Prerequisite
- First you have to install aws sam cli into your machine. 
- Then configure aws cli.

**If you don't have CLI installed and configured into your local machine please follow prerequisite steps from this** [link](https://medium.com/@farzanajuthi08/how-to-make-an-application-using-serverless-application-model-sam-and-python-937415d38a44)

### Local Development

- After installation done, you have to pull the code from git repository [(HTTPS link)](https://github.com/farzana-juthi/sam-accelerate-example.git)
- Then go to project directory by using following command:
  ```
    cd <your folder name>
    example: cd sam-accelerate-example
  ```
- Then you will see following structure:

  <img width="356" alt="structure" src="https://user-images.githubusercontent.com/63281366/223938999-547fe158-d62e-4247-b513-2b6db2787ccd.png">

### Lambda Layers code details

- In **template.yaml** file, you will get following code for creating lambda layers:
  
  <img width="407" alt="lambda_layers_temp" src="https://user-images.githubusercontent.com/63281366/223939092-8e3f3b0a-a5d1-4fcb-bf3d-540e5127f721.png">

  >In this image,
  >    - **Type:** This is used to make resource you want to create. *AWS::Serverless::LayerVersion* means it will create lambda layer.
  >    - **Properties:**
  >       - **LayerName:** This is for layer name you want to give. Here you can give any name. In this demo it is *global-utils* .
  >        - **ContentUri:** This will be your code location. In this demo it is **lambda_layers/global_utils/**
  >        - **CompatibleRuntimes:**
  >             - **python3.9**  Here you have to give your choosen language. In this demo, I used python. There are specific folder structure for lambda layers according to language. See this [link](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) for other languages.
  >    - **Metadata:**
  >         - **BuildMethod: makefile** If you want to create custom layer you can do it easily through SAM. In this make file you have to give commands to run your configuration or settings. See this [link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/building-layers.html) for documentation.
- If you need share some libraries through layers, you can add those into **requirements.txt** file in layer's python folder like following image:
  
  <img width="404" alt="layer_requirement" src="https://user-images.githubusercontent.com/63281366/223939301-266dadd4-b65d-457a-b76b-ad5388b15fb3.png">

- In **make** file within global_utils folder, you have to give path to **$(ARTIFACTS_DIR)/python**, otherwise libraries in requirements.txt file will not found into **.aws-sam** folder and when calling through layers it will not work. So this line is very important.
  ```
  build-GlobalUtils:
      echo "Global layers build started"
      pip install --default-timeout=100 -r ./python/requirements.txt -t $(ARTIFACTS_DIR)/python
      echo "Global layers build completed"
      cp -r ./python $(ARTIFACTS_DIR)/
  ```
- If you want to pass some code through layers, you can also do that. In *global_utils.py* file you can see example of it.
  
  <img width="456" alt="global_utils_file" src="https://user-images.githubusercontent.com/63281366/223939384-9115f131-9f4c-4ce5-b278-9c6381d2a530.png"> 

  > Here three libraries (json, os, boto3) and also dynamo client, resource and table name are passed through this layer. For table name, you have to pass it through function's *Environment* parameter. You will see it in a while.
- Now this layer has to be attached with lambda function where it will be used. In this post you will see global_utils layer is passed to *HelloWorldFunction* . In case of sharing resources with *!Ref* key, you have to use logical id of that resource. Here logical id for layer is *GlobalUtils* and for dynamodb table it is *TestTable* .
  
  <img width="297" alt="hello_world_function" src="https://user-images.githubusercontent.com/63281366/223939547-f00c0c7c-2ed5-47b8-af78-d95ad852bbb7.png">


### How to run sam sync
- You have to run following command into your terminal
  ```
    sam sync --watch --stack-name <give your stack name>
    example: sam sync --watch --stack-name sam-accelerate-example
  ```
- After running this command, you will see like following image:
  
  <img width="613" alt="terminal_yes_no_option" src="https://user-images.githubusercontent.com/63281366/223939627-0de999bf-b8e3-4346-8995-5f9795ffa8a3.png">
- Now you have to press **Enter** .
- Now open your aws console from browser, you will see your stack is created into cloud like following image. 

  <img width="903" alt="cloudformation_resource" src="https://user-images.githubusercontent.com/63281366/223939676-75d77a61-76fd-46c5-b850-57bdfd9b7e35.png">

- After sync, you will see an API link in your device terminal like following image:

  <img width="736" alt="API" src="https://user-images.githubusercontent.com/63281366/223940899-de43da15-25ee-4884-85c1-e164537668e7.png">
  
- After clicking on this API, you will see the table name what is passed through layer.

  <img width="762" alt="output" src="https://user-images.githubusercontent.com/63281366/223940975-dc276e98-f942-4514-9941-6fea47575fe7.png">

If you change anything in layers or anything into your template file, you will see that change into cloud. So you can test your application with real aws resources. If you have any question please let me know in comment.

