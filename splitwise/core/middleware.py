

def UserMiddleware(self):
    def wrapper(request):
        print("middlware")
        # response = self.get_response(request)
        # response = "middleware"
        # return response
        # return self

    return wrapper
