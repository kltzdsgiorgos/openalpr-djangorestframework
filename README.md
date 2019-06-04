A plate recognition program built with Python 
that uses the OpenALPR library to recognize Greek licence plates and print to the screen if 
the licence plate is insured or stolen.

The idea behind this is that we would have a government public or private API
that we could access the licence plate for law enforcement reasons or other reasons.

The licence plates are stored in a website and can be accessed
by using the API.

We store the plates in a sqlite database and check their status every time
the alpr.recognize_ndarray(frame) returns a plate.

Work In progress:

1)  authentication to access the data for a get request to create or update the 
licence plates, right now this process is down manually

2)  secure the database in case we lose the device, we currently do no need this because
the data are anonymous but this would be useful in case we use real data

3) Use the data we can gather for analytics.