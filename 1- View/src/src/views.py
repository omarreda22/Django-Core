from django.http import HttpResponse, HttpResponseRedirect


# def home(request):
# 	print(dir(request))
# 	return HttpResponse("<h1>Hello Omar</h1>")


def home(request):
	response = HttpResponse(content_type="application/json")
	# default content_type
	response = HttpResponse(content_type="text/html")
	response.content = '<h1>Hello Omar</h1>'
	response.write('<h1>Hello Omar write1</h1>')
	response.write('<h1>Hello Omar write2</h1>')
	response.write('<h1>Hello Omar write3</h1>')
	return response

def redirect_somewhere(request):
	return HttpResponseRedirect("some/where")