# **TWITTER CLONE PROJECT**  
! [license](https://img.shields.io/badge/license-MIT-green)
 This is a project cloing twitter functions.  


## Major requirements:  
| name | version | usage |
|------|------|------|
| Flask | 3.1.0 | Web framework (alternative to spring-boot-starter-web) |
| Flask-SQLAlchemy | 3.1.1 | ORM support (alternative to spring-boot-starter-data-jpa) |
| Flask-JWT-Extended | 4.4.0 | JWT handling (alternative to jjwt) |
| PyJWT | 2.6.0 | Another JWT library option |
| google-cloud-storage | 2.53.1 |  Google Cloud Storage client |
| mysql-connector-python | 8.0.33 | MySQL connector |
| pytest | 7.0.0 | Testing framework (alternative to junit + spring-boot-starter-test) |
| pytest-mock | 3.7.0 |  Mocking support for tests |
| SQLAlchemy | 2.0.40 | If you want plain SQLAlchemy without Flask integration |
| requests | 2.26.0 | For HTTP requests if needed |


## How to run 
1. Download the package and unfold it.  

2. Create the corresponding MYSQL database using `create_database.sql`, there are currently some very simple test data in database,  
if you want more, you can add by yourself.  

3. Set up Google Cloud Storage bucket for this project, download the JSON file and paste the path to `os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ` and also notice that to ensure `os.getenv("GCS_BUCKET")` has been set to the name of the project bucket. Additionally, remember to upload some pictures to GCS bucket and change
their URLs in `src/constants/default_name_contents.py` with yours


5. Finish Google oauth settings, also download the JSON file and replace the file path with your own in   
`with open("C:/****.apps.googleusercontent.com.json") as f:`

6. Now you can run with the command `py -m src.twitter_clone_app` in terminal.  

## Project structure
*_controller.py: Define the APIs for interaction
*_service.py: The real logic of controllers
*_repository.py: Connection to database, the operation of data
MODELNAME.py: The model itself
