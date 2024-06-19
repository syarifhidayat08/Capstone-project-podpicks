## Podpicks Flask Back-End
Flask backend application that provides an API for users to search for podcasts by name. This backend integrates with Machine Learning models by taking data from Google Cloud Firestore which stores podcast datasets.

## Setup and Installation
1. Clone this repository
   ```
   git clone -b backend-model https://github.com/syarifhidayat08/Capstone-project-podpicks
   ```
1. Create virtual environment (venv)
   ```
   python -m venv myenv
   ```
2. Activate the previously created venv
   ```
   myenv\Scripts\activate
   ```
3. Install the dependencies needed to run the flask backend in requirements.txt
   ```
   pip install -r requirements.txt
   ```
4. Enter the service account (credential.json) and replace the service account path with the path of the credential file

5. Start the Flask server
   ```
   python app.py
   ```

## API Documentation
```
Base url : https://backend-model-1-d36ydfqv4q-et.a.run.app
```
Get podcast recommendations by entering the desired query
```
GET /search?query=<query>

Params
| Key   | query     | 
|-------|-----------|
| Value | <query>   |
