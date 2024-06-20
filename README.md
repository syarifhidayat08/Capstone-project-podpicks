## Podpicks Back-End
Backend application that provides an API for the Podcast Recommendation application in the form of an API for user authentication, podcast search based on genre and name for users as well as a bookmark feature. This application was built using Node.js and Hapi.js and uses various services from Google Cloud Platform (GCP) such as Firestore, Firebase, Cloud Storage and Cloud Run to support its functionality. This backend allows users to get podcast recommendations based on their preferences.

## Setup and Installation
1. Clone this repository
   ```
   git clone -b cc-backend1 https://github.com/syarifhidayat08/Capstone-project-podpicks
   ```
   
2. Install dependencies for Node.js (Hapi.js)
   ```
   npm install
   ```
   
3. Create an .env file to store firebase configuration data
   ```
   PORT=your_server_port
   HOST=your_server_host
   
   FIREBASE_API_KEY=your_api_key
   FIREBASE_AUTH_DOMAIN=your_auth_domain
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_STORAGE_BUCKET=your_storage_bucket
   FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
   FIREBASE_APP_ID=your_app_id
   FIREBASE_DATABASE_URL=your_database_url
   ```
   
4. Enter the service account (credential.json) and replace the service account path with the path of the credential file
   
5. Start the Node.js server
   ```
   npm run start:dev
   ```

## API Documentation
```
Base url: https://cc-backend2-d36ydfqv4q-et.a.run.app/
```

- General Search
  ```
  GET /podcasts
  ```
  ```
  GET /podcasts/genres
  ```
  ```
  GET /podcasts/genres/<id>
  ```
  ```
  GET /podcasts/genres/<genre>
  ```

- Authentication
  ```
  Body
  {
     “email” : “< email >”,
     “password” : “< password >”
  }
  ```

  ```
  POST /api/register           ->    register account
  ```
  ```
  POST /api/login              ->    login account
  ```
  ```
  POST /api/logout             ->    logout account
  ```
  ```
  POST /api/reset-password     ->    reset password account
  ```
  
- Bookmarks
  - Add bookmark

    ```
    POST /api/bookmarks
  
    Headers:
  
    | Key   | Content-type     | 
    |-------|------------------|
    | Value | application/json |

    Authorization:
    <bearer token from login>

    Body :
    {
        "podcastId" : "<podcast id>"
    }
    ```

  - Get bookmarks by id
    ```
    GET api/bookmarks/<idToken>
    
    Authorization:
    <bearer token from login>
    ```

  - Delete bookmarks
    ```
    DELETE api/bookmarks/<idToken>

    Authorization:
    <bearer token from login>

    Body :
    {
        "podcastId" : "<podcast id>"
    }
    ```
