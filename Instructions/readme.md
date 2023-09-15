# Instructions for Causal Users

## Limitation
GoodData.CN community edition is not capable for usage from massive amount of users, we are only going to use one default users to surf the dashboards for multiple users. This application is not intended for production use.

## Log In
Once the application is setup, causal users may access the dashboard hosted by GoodData.CN at <i>http://localhost:3000</i> and it will bring you to a log in page. Log in with the default login password for the community edition, which can be found in GoodData's <a href="https://www.gooddata.com/developers/cloud-native/doc/2.4/deploy-and-install/community-edition/">documentation</a> page.

<img src=login_page.png>

## Landing to a Home Page
After you have logged in, you would come to the home page of GoodData.CN. You may click on the workspace with your Spotify username to enter the workspace (environment) where you can interact with. 

<img src=home_page.png>

<br>
In this workspace, the admin would distribute your dataset downloaded from Spotify. The dashboard would display the analytics you supplied while data from other users is not found in this workspace. In additional to the dashboards prepared by the admins, you may create additional visualizations and dashboards to this workspace. We will go over this feature in later section.
<br><br>
In a non-community edition GoodData.CN or GoodData Cloud, a user would not have access to other user's workspaces nor master workspace. Since this application is not design for production. <b>Causal users should not make interact with the master workspace</b> to avoid confusion. 

## Browse the Dashboards
Within the workspace, you may surf among different dashboards by clicking the desired dashboards on the left panel.

<img src=dashboard_example.png>

<br>
You may see a lock sign next to the dashboard name because those dashboards are owned by admin who are the only person has access to make changes to those dashboards in the master workspace. As a causal user in this workspace cannot edit those dashboard at all!
<br><br>
In the current version, a causal user has access to 4 dashboards including topics like <i>Overview</i>, <i>Songs</i>, <i>Artists</i>, and <i>Album</i>. There are filters set for those dashboards, you may change the filter value by clicking to the dropdown menu. 

## Creating Visualizations
If the visualizations are not sufficient for your analysis, you may create your own dashboard additional to what the admin prepared for you! To do so, you need to create your own visualizations and push those visualizations to a new dashboard. First, click on the <b>Analyze</b> button on the top panel that will bring you to the analytical designer.

<img src=dashboard_example.png>

<img src=ad.png>

It would bring you the page like above, this is where you can create your own visualizations. You can pick the metrics or attributes on the left panel and drag those to the selection box next to the panel, pick your chart type, name the visualization and save it.
<br><br>
You may create more than 1 visualization. After you have saved it, you may click <b>clear</b> button to start a new visualization. If you would like to retreive the previously saved visualization, you may click on the <b>Open</b> dropdown menu to load it.

## Pushing Visualizations to a New Dashboard
After you have created your visualizations, it is time to push it to a new dashboard. You should click on <b>Dashboards</b> on the top panel that will bring you back to dashboard mode. Then you may click on the <b>+</b> sign on the left panel that will bring you to the dashboard editor mode.

<img src=dashboard_editormode.png>

<br>
In here you may drag your newly created visualizations to the canvas in the center. You may also add any filter to this dashboard, simply drag <b>Attribute Value</b> on the left panel to the top canvas and select the desired attribute you want to utilize. The available attributes are provided by the admin and you may pick any attribute found in the list. In the editor mode, any filter value will become the default value of the filter. Once you are done, click <b>Save & Publish</b>!

## Happy Analytics
And this is all you need to know about how to use GoodData.CN! Happy analytics!

<br><br>
Note: We will update the instruction in the future update.


## Gallery
There are more screenshots in the [Gallery](/Gallery) folder.
