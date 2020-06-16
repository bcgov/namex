# sbc-pay-py-client

#### Re-building the Swagger Client using Swagger Hub

These are the manual build steps for re-building the Swagger Client. We will eventually move to a solution that is more
automated, using the swagger-codegen project to generate our code instead of SwaggerHub.

##### Pre-requisites:

- You will need a SwaggerHub account. There is a free tier.
- You will need to fork and clone the Synonyms API Client project locally.
  
    https://github.com/bcgov/sbc-pay-py-client

##### Steps:

1. Modify/create new endpoint in sbc-pay.
2. Run sbc-pay from your local machine (localhost). 

    1. Stop the API first if it's already started.
    2. Click the link in the console output to the Swagger Docs for the API. 
    
    ```http://localhost:<your-port>```

3. Click on the link at the left-up corner under Synonyms API header pointing to the JSON spec for the API.
    
    http://localhost:<your-port>/api/v1/swagger.json
    
4. Open up SwaggerHub in your browser and select your API project.
    
    https://app.swaggerhub.com
   
    - If you haven't already created a new Project, create one for the API.

5. Update the API project.
   
    - Copy the content of swagger.json from Step 3 and copy it into the API editor (the big black text area).
    - Make sure the following three lines are at the TOP of the file:
    
    ```
    swagger: '2.0'
    host: sbc-pay.servicebc-ne-dev.svc:8080
    schemes: [http, https]
    ```
    
    - Remove any duplicate parameters.
    - Save the API project in SwaggerHub.
    
6. Export auto-generated code. Toward the top right of the project page, there is an Export menu. 
    1. Click Export, then choose Download API > Json Resolved. 
    2. Click Export, then choose Download Client SDK > Python.

7. Unzip the downloaded files ```swagger-client-generated, python-client-generated```.
8. Copy the following into the root of your Synonyms API Client project:
    
    1. From ```swagger-client-generated``` copy ```swagger.json ```
	2. From ```python-client-generated``` copy everything except:
	  
	  ```
	  .git (dir)
	  .gitignore
	  .swagger-codegen (dir)
	  .travis.yml
	  .swagger-codegen-ignore
	  ```
	  
9. In your Synonyms API Client project search and replace:  

    ```sbc-pay-servicebc-ne-dev.svc:8080``` with ```localhost:<your-port>```

10. Commit the changes and push.

#### Using the Swagger Client in Your Application

1. Just include the package in your requirements:

    ```git+https://github.com/bcgov/sbc-pay-py-client.git#egg=swagger_client```

2. Import the client like any other package:
    
    ```from swagger_client import SynonymsApi```
