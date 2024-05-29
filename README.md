
# OpenWeatherMap ETL

This is a simple ETL built using Python and an Azure SQL Database in order to practice basic knowledge for Data Engineers and Python Developers, by retrieving temperature data from the OpenWeatherMap [Current Weather API](https://openweathermap.org/current) for a given city.

This project was built during my internship at Globant.


## Features

- Recognition of the city that you want to extract the data from, using the OpenWeatherMap [Geocoding API](https://openweathermap.org/api/geocoding-api).
- Temperature data extraction from OpenWeatherMap [Current Weather API](https://openweathermap.org/current).
- Simple data transformation in order to convert the Kelvin degrees to Celsius degrees. **(More transformations are coming soon!)**
- Data loading to an [Azure SQL Database](https://azure.microsoft.com/es-es/products/azure-sql/database/) instance, always checking that the loaded data is new in order to avoid duplicated registers.
- Logging for all the events of the ETL Pipeline, creating a log file for each of the script executions


## Requirements

You need to have installed the latest version of [Docker and Docker Compose](https://docs.docker.com/engine/install/) in order to run this project.

You'll also need an Azure SQL Database with a table with the next schema:

```sql
CREATE TABLE [dbo].[weather] (
    [uuid]         UNIQUEIDENTIFIER NOT NULL,
    [datetime]     DATETIME         NOT NULL,
    [consulted_at] DATETIME         NOT NULL,
    [temp]         REAL             NOT NULL,
    [temp_min]     REAL             NOT NULL,
    [temp_max]     REAL             NOT NULL,
    [feels_like]   REAL             NOT NULL,
    CONSTRAINT [PK_weather] PRIMARY KEY CLUSTERED ([uuid] ASC)
);
```


## Deployment

To deploy this project, follow the next steps:

First, you must setup the env variables by creating a `.env` file from the `.env.example` file and set the values as follows:
- `ZIP_CODE` is the zip code of the country of the city you want to retrieve the data from. (You can search it [here](https://worldpostalcode.com/))
-  `COUNTRY_CODE` is the [ISO 3166 Alpha-2 code](https://www.iso.org/obp/ui/#search) of the country of the city
- `API_BASE_URL` is the common URL for all the requests, having the default value of `https://api.openweathermap.org`. **Don't change it unless OpenWeatherMap changes the URLs for their APIs, what's unlikely to happen.**
- `API_KEY` is the key that OpenWeatherMap provides when you create an account on their website. You can get your API key [here](https://home.openweathermap.org/api_keys)
- `PIPELINE_EXECUTION_INTERVAL_IN_MINUTES` defines the interval in which the ETL will be executing. By default is set in five minutes but you can customize it as you want.
- `AZURE_ODBC_CONNECTION_STRING` is the connection string used to connect to the Azure SQL Database, you can find more information [here](https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-content-reference-guide?view=azuresql#get-adonet-connection-information-optional---sql-database-only)
- `AZURE_TABLE_NAME` is the name of the table in Azure SQL Database where you want to store the transformed data.

Then, you can run the docker container by using the next command:
```bash
  docker compose up
```

