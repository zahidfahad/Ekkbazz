******************************HOW TO RUN THIS PROJECT********************************

STEP-1 :

type this command on your machine: sudo docker compose up --build (assuming you will use linux)

STEP-2 :

there are three routes defined on the urls ->

    http://localhost/api/register-user/  <==> Fields (username,password)

    http://localhost/api/login/  <==> Fields (username,password)

    http://localhost/api/business/ <==> JWT authorized(set your Authorization Header type to Bearer and simply pass the token that you get from login)


