# Create Data Souce in GoodData
curl http://localhost:3000/api/v1/entities/dataSources \
  -H "Content-Type: application/vnd.gooddata.api+json" \
  -H "Accept: application/vnd.gooddata.api+json" \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -X POST \
  -d '{
      "data": {
          "attributes": {
              "name": "Spotify Data Source",
              "url": "jdbc:postgresql://host.docker.internal:8731/spotify",
              "schema": "out__data",
              "username":"airflow",
              "password":"airflow",
              "type": "POSTGRESQL"
          },
          "id": "ps-gooddata-spotify",
          "type": "dataSource"
      }
  }'

# Scan and save the physical model in JSON
curl http://localhost:3000/api/v1/actions/dataSources/ps-gooddata-spotify/scan \
-H "Content-Type: application/json" \
-H "Accept: application/json" \
-H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
-X POST \
-d '{"separator": "__", "scanTables": true, "scanViews": false}' > pdm.json

# Upload the layout of the physical model to connect GoodData with Postgres
curl http://localhost:3000/api/v1/layout/dataSources/ps-gooddata-spotify/physicalModel \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -H "Content-Type: application/json" \
  -X PUT -d @pdm.json

# Delete pdm.json
rm pdm.json

# Refresh the data source
curl http://localhost:3000/api/v1/actions/dataSources/ps-gooddata-spotify/uploadNotification -X POST \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz"
