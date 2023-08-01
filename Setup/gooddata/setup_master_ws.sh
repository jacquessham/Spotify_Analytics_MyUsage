# Upload master workspace layout
curl http://localhost:3000/api/v1/layout/workspaces/spotify_streaming_history_master \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -X PUT \
  -d @spotify_streaming_history_master_layout.json