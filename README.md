# smile-base

# Installation
  - `conda env create -f PySmileBase.yml`


### 5. Install GraphDB
#### 5.1 GraphDB Installation
- [GraphDB](https://www.ontotext.com/products/graphdb/) can be installed for your distribution.
- Make sure it's running port `7200`, e.g. [http://localhost:7200](http://localhost:7200).
- Make sure you have GraphDB running on [http://localhost:7200](http://localhost:7200).

#### 5.2 GraphDB Repository Creation
- For testing, make sure the username and password are set to `admin`
- Create a new test repository. Go to [http://localhost:7200](http://localhost:7200)
  - Create new repository:
    - Name the repository (Repository ID) as `smile`
    - Set context index to True *(checked).
    - Set query timeout to 45 second.
    - Set the `Throw exception on query timeout` checkmark to True (checked)
    - Click on create repository.
  - Make sure the repository rin in "Running" state.
- [See instruction below for troubleshooting](#user-content-graphdb-and-docker-configuration)


#### 5.3 GraphDB Configuration
A few notes on configurting SMILE to connect to the database.
- The main SMILE Flask application can be configured in the [config/local_config.yml](config/local_config.yml) file.
- Knowledge source that are running in a Docker instance must use the "Docker" version of the config file: [config/local_config_test.yml](config/local_config_test.yml).



# Run SMILE

## Start Flask
In another terminal, run the following:
#### Set Conda Environment
- `conda activate PySmileBase`


# Troubleshooting
#### GraphDB Configuration
If you get the following error, you need ot increase teh memory used by Java for running GraphDB, see below:
```
Query evaluation error: Insufficient free Heap Memory xxxMb for group by and distinct, threshold:xxxMb, reached 0Mb (HTTP status 500)
```


- Increase memory for Java:
  - Update the GraphdDB application cfg file
  - Usualy it is here: `/Applications/GraphDB Desktop.app/Contents/app/GraphDB Desktop.cfg`
  - Add or update the following lines to have `20G` memory:
    ```
    [JavaOptions]
    ...
    java-options=-Xms20G
    java-options=-Xmx20G
    ...
    ```