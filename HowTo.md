******************************HOW TO RUN THIS PROJECT********************************

STEP-1 :

type this command on your machine: sudo docker compose up --build (assuming you will use linux)

STEP-2 :

there are three routes defined on the urls ->

    http://localhost/api/register-user/  <==> Fields (username,password)

    http://localhost/api/login/  <==> Fields (username,password)

    http://localhost/api/business/ <==> JWT authorized(set your Authorization Header type to Bearer and simply pass the token that you get from login)

       *This api has two methods defined:

                **GET method: returns the list of business, you have to pass lat and lng of a place to the query_params from where system will return        responses within 2000km
                
                **POST method: 
                    **fields:
                            business_name = models.CharField()
                            place_name = models.CharField(
                            latitude = models.DecimalField()
                            longitude = models.DecimalField()


