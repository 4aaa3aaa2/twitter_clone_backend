۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩bismillah۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩

(1) IN DEFINING A CLASS

Class class_name(extend_from_class):
    property1 = ...
    property2 = ...

    def __Init__(self, var1,var2 ...):
        self.proprty1 = var1
        ...
    
    def to_dict(self):
        return {
            property1 : var1,
            property2 : var2,
            ...
        }
    
    def __repr__(self):
        return f"sentence {peoperty1}, {property2}..."

to_dict enables the class to be turned to JSON form, that can be 
read by jsonify().

__repr__ is used for debug and printing.

۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩bismillah۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩

(2) INSIDE A MODULE (for example, user)

user.py : the user model, define the datastructure and the fileds.

user_repository.py : data access layer, that connects to database
and implement the operation like find, add, delete

user_service.py : bussiness logic layer, that implements the operations
and functions that this module can do inside the whole app or before/
after access to database.

user_controller.py :  convert JSON requsts to objects and return responses,
acting like API, and ususally the logic is implemented in user_service.py.

۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩bismillah۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩

(3) THE FUNCTION OF @staticemethod

usually in a class:
Class ClassName():
    def func():
        ...

if there is no @staticemethod before def func, each time when using the 
func it is needed to do as ClassName().func()

if @staticemethod is added, it can just be ClassName.func()

۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩bismillah۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩

(4) USING db.session 

in the repository file, if the function operations to database is written as
db.session......., then in other files when calling this function, we can not 
pass db.session as the variety like func(db.session, var1, var2...) 

۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩bismillah۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩

(5) DIFFERENT get() TYPES OF request

METHOD                     SOURCE            USE CASE            RETURN
request.args.get()        URL query str     get parameters      str, None
request.form.get()        POST body         text in forms       str, None
request.files.get()       POST body         uploaded files      Filestorage, None


REQUEST TYPE	DATA LOCATION	    FLASK METHOD TO USE
GET	            URL query string	request.args.get()
POST (form)	    Body (form fields)	request.form.get()
POST (JSON)	    Body (JSON)	        request.get_json()
POST (files)	Body (multipart)	request.files.get()

۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩bismillah۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩۩