#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import webapp2
from google.appengine.api import rdbms



JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

_INSTANCE_NAME="prinya-th-2013:prinya-db"

class MainHandler(webapp2.RequestHandler):
	def get(self):

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor = conn.cursor()
		cursor.execute('SELECT course_id,course_code,course_name,credit_lecture,credit_lab,credit_learning,status,regiscourse_id FROM course natural join regiscourse')

		conn2=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor2 = conn2.cursor()
		cursor2.execute('SELECT sum(capacity),sum(enroll),regiscourse_id FROM section group by regiscourse_id')

		# conn3=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
  #   		cursor3 = conn3.cursor()
		# cursor3.execute('SELECT course_id,status FROM regiscourse')

		templates = {

			'course' : cursor.fetchall(),
			'enroll' : cursor2.fetchall(),
			# 'status' : cursor3.fetchall(),

			}

		template = JINJA_ENVIRONMENT.get_template('course.html')
		self.response.write(template.render(templates))


		
	

class Toggle(webapp2.RequestHandler):
	def get(self):

		value=self.request.get('course_id');
		value=int(value)
		
				

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor = conn.cursor()
    		sql1="SELECT status FROM regiscourse WHERE course_id= '%d'"%value
    		cursor.execute(sql1);
    		result=cursor.fetchall()

    		for row in result:
			if row[0]==1:
				sql2="UPDATE regiscourse set status=0 where course_id='%d'"%value

				cursor.execute(sql2);
				

			else:
				sql3="UPDATE regiscourse set status=1 where course_id='%d'"%value
				cursor.execute(sql3);

				
		conn.commit()
		conn.close()
		self.redirect("/")


class search(webapp2.RequestHandler):
  	def get(self):

  		course_code=self.request.get('keyword');
  		year=self.request.get('year');
  		
  		semester=self.request.get('semester');
  		check_code=0
  		check_fac=0
  		check_dep=0
  		check_year=0
  		check_sem=0
  		allcheck=0
  		key_year=""
  		key_sem=""
  		code=""

  		if year=="":
  			check_year=0
  		else:
  			check_year=1
  			key_year="year="+year

  		if semester=="":
  			check_sem=0
  		else:
  			check_sem=1
  			key_sem="semester="+semester

  		if course_code == "":
  			check_code=0

  		else:
  			check_code=1
  			code="course_code like '%"+course_code+"%' "




  		data_faculity_id=self.request.get('faculity');
  		data_faculity_id=str(data_faculity_id)
  		data_faculity=""
		if data_faculity_id=="1":
			data_faculity = "faculity='Engineering'";
		elif data_faculity_id=="2":
			data_faculity = "faculity='Information Technology'";
		elif data_faculity_id=="3":
			data_faculity = "faculity='Business Administration'";
		elif data_faculity_id=="4":
			data_faculity = "faculity='Language'";

		if data_faculity_id =="":
			check_fac=0
		else:
			check_fac=1
  		
  		
	
		data_department=self.request.get('department');
		data_department=str(data_department)
		data_department_full=""

		if data_department=="1":
			data_department_full="department='Information Technology'"
		elif data_department=="2":
			data_department_full="department='Multimedia Technology'"
		elif data_department=="3":
			data_department_full="department='Business Information Technology'"
		elif data_department=="4":
			data_department_full="department='Accountancy'"
		elif data_department=="5":
			data_department_full="department='Industrial Management'"
		elif data_department=="6":
			data_department_full="department='International Business Management'"
		elif data_department=="7":
			data_department_full="department='Japanese Businees Administration'"
		elif data_department=="8":
			data_department_full="department='Computer Engineering'"
		elif data_department=="9":
			data_department_full="department='Production Engineering'"
		elif data_department=="10":
			data_department_full="department='Automotive Engineering'"
		elif data_department=="11":
			data_department_full="department='Electrical Engineering'"
		elif data_department=="12":
			data_department_full="department='Industrial Engineering'"
		elif data_department=="13":
			data_department_full="department='Language'"

		if data_department=="":
			check_dep=0
		else:
			check_dep=1

		

		where_code=" "
		a=" and "

		

		if check_code == 1:
			if check_code == 1:
				where_code+=code
			if check_year == 1:
				where_code+=a
				where_code+=key_year
			if check_sem == 1:
				where_code+=a
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_year == 1:
			if check_year == 1:
				where_code+=key_year
			if check_sem == 1:
				where_code+=a
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_sem == 1:
			if check_sem == 1:
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_fac == 1:
			if check_fac == 1:
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_dep==1:
			if check_dep==1:
				where_code+=data_department_full
		else:
			where_code="course_id = 0"



		# self.response.write(where_code)


                
      	
	

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor = conn.cursor()
    		sql="SELECT course_id,course_code,course_name,credit_lecture,credit_lab,credit_learning,status,regiscourse_id FROM course natural join regiscourse where %s "%(where_code)
                # sql="SELECT course_id,course_code,course_name,credit_lecture,credit_lab,credit_learning,status,regiscourse_id FROM course natural join regiscourse where course_code like '%s'"%(percent)
		cursor.execute(sql)
		conn.commit()
		

		conn2=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor2 = conn2.cursor()
		cursor2.execute('SELECT sum(capacity),sum(enroll),regiscourse_id FROM section group by regiscourse_id')
		conn2.commit()


		
	

		templates = {

			'course' : cursor.fetchall(),
			'enroll' : cursor2.fetchall(),
			

			}

		template = JINJA_ENVIRONMENT.get_template('course.html')
		self.response.write(template.render(templates))

		conn.close()
		conn2.close()


  	
    		

		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/toggle',Toggle),
    ('/search',search),
], debug=True)
