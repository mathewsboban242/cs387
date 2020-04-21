from django.shortcuts import render

def func(request):
	# if request.user.is_authenticated:
	return render(None, 'blah.html')

def github_authenticated(request):
	if request.method == GET:
		auth_code = #extract code from request
		access_token = get_access_token(code) # step 2 in documentation.
		user_info = get_user_info(access_token) # step 3 in documentation
		return HtmlResponse("<html><body>" + str(user_info) + "</body></html>")
