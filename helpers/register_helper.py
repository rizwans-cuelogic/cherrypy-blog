

def check_empty_data(username,email,password,confirm_password):
	
	if username == '' or email == '' or password == '' or confirm_password == '':
		return False

	return True

def check_password_length(password):
	
	if len(password)<6:
		return False

	return True 

def check_password_match(password,password1):
	
	if password != password1:
		return False
	
	return True