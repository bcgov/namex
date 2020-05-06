# Using the Synonyms API Client

Visit the project page for the [Synonyms API Client](https://github.com/bcgov/namex-synonyms-api-py-client).

To use the Synonyms API Client in your application just include the package in your requirements:

```git+https://github.com/bcgov/namex-synonyms-api-py-client.git#egg=swagger_client```

Then import the client like any other package:
    
```from swagger_client import SynonymsApi```

### Re-building the Swagger Client

These are the build steps for re-generating the Swagger Client. 

#### Pre-requisites:

1. You need to have [Docker](https://docs.docker.com/get-docker/) installed locally and running.
2. You need to have the solr-synonyms-api project running. If you're here, you probably already do.
3. You need to have forked the [Synonyms API Client](https://github.com/bcgov/namex-synonyms-api-py-client) project, if you want to push the client to a remote git repository.
 
#### When to Generate the API Client
You MUST update the API client if you modify / create an endpoint in solr-synonyms-api.

#### Generating an Updated API Client

1. Run solr-synonyms-api from your local machine (localhost). 

   - Stop the API first if it's already started.
   - Open the link in the console output to the Swagger Docs for the Synonyms API. 
    
     ```http://localhost:<your-port>```
     
2. Copy the link at the left-up corner of the Swagger Docs. It will look something like:
    
   ```http://localhost:<your-port>/api/v1/swagger.json```
    
3. Open up a new terminal window. From the root ```/client``` folder run `bash ./generate-client.sh`.

   This will utility will generate an updated API client. Usage is simple, just follow the prompts:
    
   1. Enter the URL for the OpenApi spec from [Step 2] or press enter to use the default: 
      ```http://localhost:<your-ENV-port>/api/v1/swagger.json```
      
   2. You will be prompted to push the client to a remote repository. 
      Enter ```no```, if you want to follow the manual update steps. Enter ```yes``` if you want to push the new client to a git repository.
      
   3. If you entered```yes``` you will prompted to enter a git repository URL eg. 
      ```https://github.com/<org-name>/namex-synonyms-api-py-client```
      
   4. You will finally be prompted for the name of the branch you would like to commit to. 
      The default is ```test-codegen```.
   
   And that's it!
   
Note: you can configure the default git repository URL to use by adding the following line to your .env:
      
```
# No trailing slashes!
export SYNONYMS_API_CLIENT_REPO_URL="https://github.com/<your-fork>/namex-synonyms-api-py-client"
```
      
#### [optional] Manual Update Steps

- Copy the files from the ```/client/dist``` folder into the root of your Synonyms API Client project.

- Commit the changes and push.


#### Modifying the Templates

- Documentation for swagger-codegen [Mustache template variables](https://github.com/swagger-api/swagger-codegen/wiki/Mustache-Template-Variables)