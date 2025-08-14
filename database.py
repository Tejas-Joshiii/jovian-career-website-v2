# database.py handles DB operations 
import os
import ssl
from sqlalchemy import create_engine, text
from dotenv import load_dotenv # Importing load_dotenv to load environment variables from a .env file database ka password user etc load it secratly taaki koi aur na dekh paye
load_dotenv()  # Load .env file this is a function

# yeh path hai jaha par database.py file hai
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# The os.path.join() function in Python's os.path module is used to intelligently combine one or more path components into a single, valid path string. Its primary advantage is platform independence, as it automatically uses the correct path separator (e.g., / on Unix-like systems and `\` on Windows) based on the operating system where the code is executed.
# yeh join kardega path of app.py with ca.pem file ke sath phir taaki ssl connection establish kar sake
# yeh ek secure way hai to connect to the database
CA_PATH = os.path.join(BASE_DIR, "ca.pem") 

db_url = os.getenv("db_connection")  # Get the database connection string from environment variable
engine = create_engine( 
        db_url,
        connect_args={
        "ssl": {
            "ca": CA_PATH
        }
    }
)

def load_jobs_from_db():
    # This function can be used to load jobs from a database
    # For now, we will return the static JOBS list

    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
    #  print(result.all()) # uper wali query se output display karne ka tarika (result object hai usme data store hai query ka response ka ya consume kar rkha hai but hum isse dubara se use nahi kar sakte list empty ho jayegi) iterator hai
    # this print will give list of rows of results at once (means all the rows of the table or list of tuples)
    jobs = [] # list to store dictionaries
 # result is an iterator, so we can iterate over it to get each row
    for row in result.all():
        jobs.append(row._asdict())  # convert each row to a dictionary and append to the list ._asdict ke jagah dict(row) bhi use kar sakte hain leking yha mat karna kyunki row ek tuple hai aur tuple ko dict mei convert nahi kar sakteTypeError: cannot convert dictionary update sequence element #0 to a sequence
    return jobs  # return the list of dictionaries where each dictionary represents a row of the table with column names as keys and values as values

# with engine.connect() as conn:
#      result = conn.execute(text("select * from jobs"))
    #  print(result.all()) # uper wali query se output display karne ka tarika (result object hai usme data store hai query ka response ka ya consume kar rkha hai but hum isse dubara se use nahi kar sakte list empty ho jayegi) iterator hai
    # this print will give list of rows of results at once (means all the rows of the table or list of tuples)

def load_job_from_db(id): # yeh function alag hai uper wale se yeh job hai confuse ho gya tha mai
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
        {'val': id}  #  pass parameters as dict       using a parameterized query to prevent SQL injection attacks
        )         
    rows = result.all()  # this will give all the rows of the table as a list of tuples
    if len(rows) == 0: # agar koi row nahi hai to toh voh zero hi hoga ex :- agar 5 rows hai aur 10 select karte hai toh zero rows return karega
        return None
    else:
        return rows[0]._asdict()  # this will return the first row as a dictionary with column names as keys and values as values error ayegi tabhi yhi use kar rhe naa ki dict(rows[0]) kyunki rows ek tuple hai aur tuple ko dict mei convert nahi kar sakte

def add_application_to_db(job_id, data): # data here dictionary form info carry karta hai
    # This function can be used to add an application to the database    
    # Here you would typically insert the application data into the database
    # using an INSERT SQL statement
    # Example: conn.execute(text("INSERT INTO applications (job_id, name, email) VALUES (:job_id, :name, :email)"), {'job_id': job_id, 'name': application_data['full_name'], 'email': application_data['emailId']})
    with engine.connect() as conn:
        query = text("""INSERT INTO applications (job_id, full_name, email, linkedIn_URL, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedIn_URL, :education, :work_experience, :resume_url)""")
        conn.execute(query, 
                 {
                'job_id': job_id,
                'full_name': data['full_name'],
                'email': data['emailId'],
                'linkedIn_URL': data['linkedInURL'],
                'education': data['Edu'],            
                'work_experience': data['work'],     
                'resume_url': data['resume_url']
            }
        )
        conn.commit()  # commit the transaction to save the changes to the database


# result_dicts = [] # list to store dictionaries
# # result is an iterator, so we can iterate over it to get each row
# for row in result.all():
#     result_dicts.append(row._asdict())  # convert each row to a dictionary and append to the list ._asdict ke jagah dict(row) bhi use kar sakte hain

# print("result_dicts: ", result_dicts)  # this will print the list of dictionaries where each dictionary represents a row of the table with column names as keys and values as values



# print("type (result): ", type(result))
# result_all = result.all()  # result.all() will give all the rows of the table
# print("type (result_all): ", type(result_all))
# print("result_all: ", result_all)  # this will print all the rows of the table as a list of tuples
# first_result = result_all[0]  # this will give the first row(horizontal line) of the table
# print("type (first_result): ", type(first_result))
# first_result_dict = first_result._asdict()  # this will convert the first row to a dictionary or we can use dict(first_result) also
# print("type (first_result_dict): ", type(first_result_dict))
# print(first_result_dict)  # this will print the first row as a dictionary
# # this will print the first row as a dictionary with column names as keys and values as values
