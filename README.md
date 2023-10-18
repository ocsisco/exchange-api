# EXCHANGE API

**"Exchange api" is an api for currency exchange, it works in a similar way to the commercial apis available in the market**

How to use "Exchange api"?

Install the dependencies and run the uvicorn server in local with command "uvicorn main:app" and enjoy of the next endpoints:

``` [python]
/fetch-one
/fetch-multi
/fetch-all
/convert
/currencies
```



* /fetch-one:

If you GET: */fetch-one?From=USD&To=EUR*

the api return:

`	
Response body

{
  "From": "USD",
  "To": {
    "Coin": "EUR",
    "Value": 0.948
  }
}`


* /fetch-multi:

If you GET: */fetch-multi?From=EUR&To=USD%2CGBP*

the api return:

`
Response body

{
  "From": "EUR",
  "To": [
    {
      "Coin": "USD",
      "Value": 1.055
    },
    {
      "Coin": "GBP",
      "Value": 0.865
    }
  ]
}`

* /fetch-all:

If you GET: */fetch-all?From=USD*

the api return:

`
Response body

{
  "From": "USD",
  "To": [
    {
      "Coin": "USD",
      "Value": 1
    },
    {
      "Coin": "EUR",
      "Value": 0.948
    },
    {
      "Coin": "GBP",
      "Value": 0.82
    }
  ]
}`

* /convert

If you GET: */convert?From=GBP&To=USD&Amount=10*

the api return: 

`
Response body

{
  "From": "GBP",
  "Amount": 10,
  "To": {
    "Coin": "USD",
    "Value": 12.19
  }
}`

* /currencies

If you GET: */currencies*

the api return: 

`	
Response body

{
  "EUR": "Euro",
  "GBP": "British Pound Sterling",
  "USD": "United States Dollar"
}`


You can run with docker, you can will make a image from dockerimage an run this image with command "docker run --rm -it  -p 80:80/tcp your_image_name"