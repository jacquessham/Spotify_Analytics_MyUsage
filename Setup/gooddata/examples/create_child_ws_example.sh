curl -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -H "Content-Type: application/vnd.gooddata.api+json" \
  -H "Accept: application/vnd.gooddata.api+json" \
  -X POST \
  -d '
{
  "data": {
    "id": "spotify_streaming_history_jacquessham",
    "type": "workspace",
    "attributes": {
      "name": "Spotify Streaming History Analysis (jacquessham)"
    },
    "relationships": {
      "parent": {
        "data": {
          "id": "spotify_streaming_history_master",
          "type": "workspace"
        }
      }
    }
  }
}
  ' http://localhost:3000/api/v1/entities/workspaces

curl http://localhost:3000/api/v1/layout/workspaceDataFilters \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -H "Content-Type:application/json" \
  -X PUT -d @ws_example_filter.json