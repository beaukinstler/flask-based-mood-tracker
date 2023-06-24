# Project Goals

1.  Implement a **2-tier architecture** that includes a **Postgres database** and the **web-based application** that interacts with the database.   
    
2.  Use Docker Compose to define and manage the tiers. 
    
3.  Be pushed to an online repository on GitHub.
    
4.  Be deployed to the cloud. 


### General Development Plan

1.  This week, you will begin the design of a web-based application that you will containerize as a multi-container application using Docker Compose. 
    
2.  In Week 2, you will apply what you learned in Week 1 to begin building your application and push it to an online repository. 
    
3.  In Week 3, you will continue building out your application in Docker Compose, and you will begin to add tests to it.   
    
4.  In Week 4, you will attempt to deploy your application to one of the Big Three Cloud Service Providers. Alternatively (or additionally), you will build a GitHub Actions workflow to automate building and testing your application.
    

# Questions and Answers

1.  What are the various features you would like your project to offer? 
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

2.  What are the API endpoints that you would need to set up for each feature? List them along with the respective HTTP verb, endpoint URL, and any special details (query parameters, request bodies, headers). 
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
				

3.  Provide a description of the database tables required for your application, including column names, data types, constraints, and foreign keys. Include your database name. You can optionally include an ER diagram. 

-   You are not required to start nor submit any code this week. However, when you do begin working on the code and containers, keep these tips in mind:

-   Set up a folder as the parent folder for your web application, and use this parent folder as the location for your docker-compose.yml file. 
-   Use a separate virtual environment for your project, and set it up in the same folder as the docker-compose.yml file. Activate it when testing locally. 
-   Test that your application works locally before you attempt to create a Docker image and containerize it. 
-   If you set up a Git repository, the Git repository should also be located in the same folder as the docker-compose.yml file. The virtual environment folder name should be added to the repository's .gitignore file so that it does not become added to the Git repository.