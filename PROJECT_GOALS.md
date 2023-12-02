# Project Goals

1.  Implement a **2-tier architecture** that includes a **Postgres database** and the **web-based application** that interacts with the database.   
    
2.  Use Docker Compose to define and manage the tiers. 
    
3.  Be pushed to an online repository on GitHub.
    
4.  Be deployed to the cloud. 


### General Development Plan

1.  A web-based application that is containerized as a multi-container application using Docker Compose. 
    
2.  Store in an online repository. 
    
3.  Add tests to the application.   
    
4.  Deploy your application to one of the Big Three Cloud Service Providers. Alternatively (or additionally), you will build a GitHub Actions workflow to automate building and testing your application.
    

# Features


1. User accounts for tracking mood over time
2. Push button Smile or Sad to show mood at the time.
3. Optional Note
	1. Notes encrypted, until in the client.
4. Data that aggregates all users to to show collective mood trends
5. Display some detail of data from media or social media sources
	1. Ideas for this
		1. display a mood graph. Show trending topics in the timeframe around the mood chnages.
	2. Media sources
		1. NY Times
		2. Bloomberg?
		3. Twitter
		4. Google Searches
		5. Bing Searches

# API endpoints

1. Capture Mood (POST)
	1. Endpoints
		1. /user/<user_id>/sad
		2. /user/<user_id>/happy
	2. Logic
		1. Lookup the user in the db.
		2. Check the last mood capture
		3. If recent (check some default amount of time  FUTURE: give each account a setting) only allow updating the mood. 
			1. Respond with 40X and redirect to a Edit page that uses the PATCH
		4. Else:
			1. Log the mood and time in the database
2. Mood lists
	1. Endpoints
		1. /moods
			- GET: List all moods
			- POST: create a mood. body needs json. [{"description":"happy"}]
			- PATCH/PUT: update the description of the moods

		2. /moods/{descirption}
			- GET: Get total by date of moods based on description
				

# database tables required

