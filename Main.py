from flask import Flask, render_template, request, jsonify, Response, make_response, redirect
from signUP import *
from signIN import *
import os
#import logging

import os
import cv2
import random
import shutil
from Training import * 
from Company_data import *
import logging


# for user login page check https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

app = Flask(__name__)


def condition_validation(company,category,name):            
    logger.info("Validating inputs")                # validating where input taken are empty
    if company == '':
        errorStr = 'Please select any company'
        status_code = 422
    else:
        if category == '':
            errorStr = 'Please select any category'
            status_code = 422
        else:
            if name == '':
                errorStr = 'Please enter Name/ID of Person'
                status_code = 422
            else:
                errorStr = 'all ok'
                status_code = 200
    return errorStr,status_code


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/signup/', methods=['POST'])
def signUp():
    args = request.get_json()
    company = args.get('company') 
    password = args.get('password')
    res, st_code = condition_validation(company,password,'xyz')
    
    status,code = signup().mydata(company,password)
    return make_response(jsonify(status),code)


@app.route('/signin/', methods=['POST'])
def signIn():
    args = request.get_json()
    company = args.get('company') 
    password = args.get('password')
    res, st_code = condition_validation(company,password,'xyz')
    print("SSS")
    status,code = signin().mydata(company,password)
    if code == 200:
        print("Login success")
        #return make_response(jsonify(status),code)    # working
        return make_response(redirect('/index2.html/'),code)	# this is working and Jsonify format in redirect giving error
        #return make_response(jsonify(redirect('/index2.html/'),code))    # not working

    else:
        return make_response(jsonify(status),code)
        return make_response(redirect('/login.html/'),code)



def generate_List(path):
    list1 = []
    if os.path.exists(path):
        files = os.listdir(path)
        list1.append(files)
        print("List : ",list1)
        list_status = 'List formed!!!'
        logger.info(list_status)
        response = {"expected_result":list1}
        return make_response(jsonify(response),200)
    else:
        list_status = 'Invalid input!!!'
        logger.error(list_status)
        response = {"expected_result":list_status}
        return make_response(jsonify(response),400) 



@app.route('/get_company_list/', methods=['GET'])		
def company_list():		                          # function to remove category of given company
    logger.info("################")                
    logger.info("Task : Getting Company name list")
    response = generate_List('images/')
    return response


@app.route('/add_company/', methods=['POST'])		# function to add company
def add_company_name():						# function name should be different in every new app.route
    logger.info("################")                
    logger.info("Task : Adding Company name")
    args = request.get_json()
    company = args.get('company')           # getting JSON values from index.html
    
    res, st_code = condition_validation(company,'xyz','xyz')

    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        if not os.path.exists('images'):
            logger.warning("images folder was not existed... just created")
            os.makedirs('images')
        if not os.path.exists('images/'+company.lower()):
            os.makedirs('images/'+company.lower())
            cmpny_status = "Company " + company.lower() + " Added"
            logger.info(cmpny_status)
            response = {"expected_result":cmpny_status}
            return make_response(jsonify(response),200)
        else:
            found = "Company is already exist"
            logger.warning(found)
            response = {"expected_result":found}
            return make_response(jsonify(response),200)


@app.route('/remove_company/', methods=['POST'])		  # url just used to confirm which button got clicked 
def rem_company_name():			                  # function to remove company folder	
    logger.info("################")                		
    logger.info("Task : Removing Company name")
    args = request.get_json()
    company = args.get('company')              
    res, st_code = condition_validation(company,'xyz','xyz')

    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        if os.path.exists('images/'+company.lower()):
            shutil.rmtree('images/'+company.lower())
            Remove_status = company.lower() + ' Content Removed Successfully!!!'
            logger.info(Remove_status)
            response = {"expected_result":Remove_status}
            return make_response(jsonify(response),200)
        else:
            remove_status = 'Company d not exist!!!'
            logger.error(remove_status)
            response = {"expected_result":remove_status}
            return make_response(jsonify(response),400)				
    


@app.route('/get_category_list/', methods=['GET'])		
def category_list():		                          # function to remove category of given company
    logger.info("################")                
    logger.info("Task : Getting Category name list")
    args = request.get_json()
    company = args.get('company')           
    res, st_code = condition_validation(company,'xyz','xyz')
    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        response = generate_List('images/'+company.lower())
        return response


@app.route('/add_catgory/', methods=['POST'])		
def add_ctgry_name():		                          # function to add category of given company
    logger.info("################")                
    logger.info("Task : Adding Category name")
    args = request.get_json()
    company = args.get('company') 
    category = args.get('category')
    res, st_code = condition_validation(company,category,'xyz')

    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        if not os.path.exists('images/'+company.lower()):
            cmpny_status = 'Company folder not exist!!!'
            print(cmpny_status)
            logger.error(cmpny_status)
            response = {"expected_result":cmpny_status}
            return make_response(jsonify(response),400)
        if not os.path.exists('images/'+company.lower()+'/'+category.lower()):
            os.makedirs('images/'+company.lower()+'/'+category.lower())
            ctgry_status = "category " + category.lower() + " Added"
            logger.info(ctgry_status)
            response = {"expected_result":ctgry_status}
            return make_response(jsonify(response),200)
        else:
            found = "Category is already exist"
            logger.warning(found)
            response = {"expected_result":found}
            return make_response(jsonify(response),200)


@app.route('/remove_catgory/', methods=['POST'])		
def rem_ctgry_name():		                          # function to remove category of given company
    logger.info("################")                
    logger.info("Task : Removing Category name")
    args = request.get_json()
    company = args.get('company')           
    category = args.get('category')
    res, st_code = condition_validation(company,category,'xyz')

    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        if os.path.exists('images/'+company.lower()+'/'+category.lower()):
            shutil.rmtree('images/'+company.lower()+'/'+category.lower())
            Remove_status = category.lower() + ' Content Removed Successfully!!!'
            logger.info(Remove_status)
            response = {"expected_result":Remove_status}
            return make_response(jsonify(response),200)
        else:
            remove_status = 'Invalid input!!!'
            logger.error(remove_status)
            response = {"expected_result":remove_status}
            return make_response(jsonify(response),400)
   

  
@app.route('/get_person_list/', methods=['GET'])		
def person_list():		                          # function to remove category of given company
    logger.info("################")                
    logger.info("Task : Getting Person name list")
    args = request.get_json()
    company = args.get('company')           
    category = args.get('category')
    res, st_code = condition_validation(company,category,'xyz')
    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        response = generate_List('images/'+company.lower()+'/'+category.lower())
        return response


@app.route('/person_exist/', methods=['POST'])	# this is to check whether person dir exist or not
def check_existence():						
    logger.info("################")                
    logger.info("Task : Checking Person name existence")
    args = request.get_json()
    print(args)
    name = args.get('name')
    category = args.get('category')		
    company = args.get('company')              
    print("#################")
    print(name)
    print(category)
    print(company)
    print("#################")

    res, st_code = condition_validation(company,category,name)
    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else: 
        logger.info("Validation over : " + res)

        if not os.path.exists('images/'+company.lower()+'/'+category.lower()+'/'+name.lower()):
            errorStr = 'Name ' + name + ' is ' + 'not Exist'
            logger.error(errorStr)		       
            response = {"error":errorStr}
            return make_response(jsonify(response),400)
        else:
            found = 'Name ' + name + ' is already exist'
            logger.info(found)
            response = {"expected_result":found}
            return make_response(jsonify(response),200)


@app.route('/person_add_photo/', methods=['POST'])		
def add_photos():                                          # this will click and store pics of person in respective directory 
    logger.info("################")                
    logger.info("Task : Clicking pictures")
    args = request.get_json()
    print(args)
    name = args.get('name')
    category = args.get('category')		
    company = args.get('company')    
    print("#################")
    print(name)
    print(category)
    print(company)
    print("#################")

    res, st_code = condition_validation(company,category,name)
    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else: 
        logger.info("Validation over : " + res)

        if not os.path.exists('images/'+company.lower()+'/'+category.lower()):
            cmpny_status = 'Invalid Input!!!'
            logger.error(cmpny_status)
            response = {"expected_result":cmpny_status}
            return make_response(jsonify(response),400)
        if not os.path.exists('images/'+company.lower()+'/'+category.lower()+'/'+name.lower()):
            logger.warning(name.lower() + " folder was not existed... just created")
            os.makedirs('images/'+company.lower()+'/'+category.lower()+'/'+name.lower())
            
        try:
            #video_capture = cv2.VideoCapture("rtsp://admin:q12345678@192.168.7.9:554/Streaming/Channels/101 RTSP/1.0")	
               
            video_capture = cv2.VideoCapture(0)
            x = random.randint(1000,9999)
            ret, frame = video_capture.read()
            print("x value = : ",x)
            #print(frame)
            cv2.imwrite('images/'+company.lower()+'/'+category.lower()+'/'+name.lower() +'/'+ "pctur_%d.jpg" % x, frame) 
            print("Pic uploaded")
            upload_pic = 'Pic successfully uploaded'
            logger.info(upload_pic)
            response = {"expected_result":upload_pic}
            return make_response(jsonify(response),200)
        except:
            click_status = 'error while clicking pictures'
            logger.error(click_status)
            response = {"expected_result":click_status}
            return make_response(jsonify(response),400)


@app.route('/remove_person_info/', methods=['POST'])		# this will Delete directory of a person
def remove_details():
    logger.info("################")                
    logger.info("Task : Removing Person name existence")
    args = request.get_json()
    name = args.get('name')
    category = args.get('category')		
    company = args.get('company')    
    print("#################")
    print(name)
    print(category)
    print(company)
    print("#################")

    res, st_code = condition_validation(company,category,name)
    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else: 
        logger.info("Validation over : " + res)
        if os.path.exists('images/'+company.lower()+'/'+category.lower()+'/'+name.lower()):
            shutil.rmtree('images/'+company.lower()+'/'+category.lower()+'/'+name.lower())
            Remove_status = name + ' Content Removed Successfully!!!'
            logger.info(Remove_status)
            response = {"expected_result":Remove_status}
            return make_response(jsonify(response),200)
        else:
            remove_status = 'Person not exist!!!'
            logger.error(remove_status)
            response = {"expected_result":remove_status}
            return make_response(jsonify(response),200)



@app.route('/train_model/', methods=['POST'])		
def training():                                  # this will start training of any particular category of any company
    logger.info("################")                
    logger.info("Task : Training ")
    args = request.get_json()
    print(args)
    category = args.get('category')		
    company = args.get('company')    
    
    res, st_code = condition_validation(company,category,'xyz')
    if not st_code ==200:
        logger.error("Validation error : " + res)
        response = {"error":res}
        return make_response(jsonify(response),st_code)
    else:    
        logger.info("Validation over : " + res)
        if not os.path.exists('images/'+company.lower()+'/'+category.lower()):
            training_status = 'Path not found!!!'
            logger.error("Validation error : " + training_status)
            response = {"expected_result":training_status}
            return make_response(jsonify(response),400)
        else:
            print("Training starts...")
            try:
                classifier, list1 = Training().train("images/"+company.lower()+'/'+category.lower(), model_save_path="trained_knn_model.clf", n_neighbors=2)
                training_status = 'Training completed!!!!!!'
                print(training_status)
                logger.info(training_status)

                if len(list1) != 0:
                    response = {"expected_result":list1}
                    return make_response(jsonify(response),200)
                else:
                    return make_response(jsonify(response),200)
            except:
                training_status = 'Training Failed!!!'
                print(training_status)
                response = {"expected_result":training_status}
                return make_response(jsonify(response),400)



@app.route('/download_company_data/', methods=['POST'])		
def company_data():                            # this will start create excel file or directory structure of any compamy
    logger.info("################")                
    logger.info("Task : Excel creation")
    args = request.get_json()
    print(args)
    company = args.get('company')    

    if company == '':
        errorStr = 'Please select any company'
        logger.error(errorStr)
        response = {"error":errorStr}
        return make_response(jsonify(response),400)
    else:
        print("#################")
        if os.path.exists('images/'+company.lower()):
            excel_status = Company_data().excell('images/',company.lower())
            response = {"expected_result":excel_status}
            logger.info(response)
            return make_response(jsonify(response),200)
        else:
            remove_status = 'No such company exist!!!'
            logger.error(remove_status)
            response = {"expected_result":remove_status}
            return make_response(jsonify(response),400)



@app.route('/prediction/', methods=['GET'])		
def prediction():                            # this will start create excel file or directory structure of any compamy
    args = request.get_json()
    print(args)
    person_name = args.get('name')    
   
    if person_name == 'unknown':
        print('unknown')
        response = {"R":0}
    else:
        print(person_name)
        response = {"R":1}
    return make_response(jsonify(response),400)



if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host = '127.0.0.1',port=5000)
    #app.run(host = '192.168.5.131',port=5000)
    app.run(host = '192.168.5.131',port=5000,debug=True,threaded=True)
#    app.secret_key = 'mysecret''Training completed!!!'







