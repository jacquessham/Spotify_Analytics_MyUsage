# Find the payloads for creating children workspaces
lst_files=($(ls payloads))
SUB='child_ws_'

# Create each individual child workspace
for STR in "${lst_files[@]}"
do
	if [[ "$STR" == *"$SUB"* ]]; 
		then 
		curl http://localhost:3000/api/v1/entities/workspaces \
		-H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
		-H "Content-Type: application/vnd.gooddata.api+json" \
		-H "Accept: application/vnd.gooddata.api+json" \
		-X POST \
		-d @payloads/"$STR" 
	fi
done

# Set up a Data filter
curl http://localhost:3000/api/v1/layout/workspaceDataFilters \
  -H "Authorization: Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz" \
  -H "Content-Type:application/json" \
  -X PUT -d @payloads/ws_filter.json