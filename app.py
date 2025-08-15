from flask import Flask, render_template, url_for, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db  # Importing functions to load jobs from the database
#image ko load karne ke liye templates se url_for ko import karna padega
# Create a Flask web application instance ya variable jisme flask application load hogi ye deployment ke vakt gunicorn app:app :- app.py:name of variable
app = Flask(__name__)



# data kisi aur jagah hota database mei hamne yha par dynamically data ko render kiya hai



# Define a route for the route URL ("/")
@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()  # Load jobs from the database using the function imported from database.py
    # return render_template(Home.html)
    return render_template("Home.html", jobs=jobs, company_name='Jovian')

    # some website allows access to dynamic data using API
    # Json is simply JavaScript objects


@app.route("/api/jobs")  # is function ko register karna padega at route(Second route or URL) & JOBs information ko lenge aur convert karenge into JSON String :- jsonify(helper function) ko import(or call) karna isko
def list_jobs():
    jobs = load_jobs_from_db()
    # load_jobs_from_db() function will return a list of dictionaries where each dictionary represents a
    return jsonify(jobs)  #jsonify takes any object and converts into a json object

@app.route("/job/<id>")  # is function ko register karna padega at route(Second route or URL) & JOBs information ko lenge aur convert karenge into JSON String :- jsonify(helper function) ko import(or call) karna isko
def show_job(id):
    job = load_job_from_db(id)
    # return jsonify(job)  #jsonify takes any object and converts into a json object but hame isse HTML jobpage mei render karna hai job hame id url me de job ki information ache se dikhe
    if not job:  # agar job nahi mila toh 404 error return karna hai
        return "Job not found", 404 # agar yeh if chal gya toh niche wala code nahi chalega
    return render_template("jobpage.html", job=job)  # job is a dictionary with all the information about the job iske madad se data ko jobpage.html mei render karenge

@app.route("/api/job/<id>")  # is function ko register karna padega at route(Second route or URL) & JOBs information ko lenge aur convert karenge into JSON String :- jsonify(helper function) ko import(or call) karna isko (is function isko api ke through access karna hai)
def show_job_json(id):
    job = load_job_from_db(id)
    return jsonify(job)

# method POST ka use karte hai jab hame server ko kuch data bhejna hota hai jaise form data jab user form submit karta hai toh hame server ko data bhejna hota hai
@app.route("/job/<id>/apply", methods=['POST'])  # is function ko register karna padega at route(Second route or URL) & JOBs information ko lenge aur convert karenge into JSON String :- jsonify(helper function) ko import(or call) karna isko
# "/job/<id>/apply" also expects a post method becoz we have used post method in the form in jobpage.html so it expects some data to be posted by the browser and not send a url which becomes bulky and slow we add more things in form
# when we send form data to apply route all the information in the url got read into the variable data and then converted into JSON format
def apply_to_job(id):
    # data = request.args  # it contains information from the URL when u post the data if post method is used then it no longer in request.args  is present in request.form  request.args is a dictionary-like object that contains the query parameters from the URL
    # request.form data is posted to this URL and nothing in the URL it was sent by the browser along with the request to this URL Now that data was accessed using request.form 
    data = request.form
    # store this in database or send an email or dispplay an acknowledgement page
    # return jsonify(data)  # return the data as a JSON response, this is just for testing purpose, in real application we will save this data to database or send an email
    job = load_job_from_db(id)  # load the job from the database using the id
    add_application_to_db(id, data)  # add the application to the database using the function imported from database.py
    return render_template("application_submitted.html", application=data, job=job)  # this will render the application_submitted.html template and pass the data(dictionary) to it

# when people say rest API or Json API or API endpoint this is what they mean that your server is returning some information not just as HTML(HTML version of that information) but the same information is also accessible in the form of Json in the form where it's just the data and then u can do whatever u want with the data

# Run the application if this script is executed directly
# programatically extraction data of thousand user then u can simply invoke this Json endpoint or Json route and get all data structured in the form of Json and maybe create a CSV out of it and Analyze it
# information database se bhi aa saki yha par JOBS se aa rha hai
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    print("I am inside if")
print(__name__)
print("check kar hre hai")
# requirement.txt file mei ham jo library isme import karenge vo dalaenge kyunki render.com ko pata nahi hai ki isko install karne ki jarurat hai
# gunicorn ek production server hai for python when python says its for devlopment server not for production use isko use karke ham flask application ko production mei laate hai
# pip ek package manager hai for python it is used to install liberaries in Python & u are just telling pip look into the requirements.txt file in each line there will be name of the liberary and plz install that liberary for me
