#Basic rules for all clients
All clients take an API key and a response type at time of instantiation. 

###API key
You can acquire an API key from the [Giant Bomb](http://www.giantbomb.com/api/) site.

###Return types
Giant Bomb supports `JSON` and `XML` as return types. You can define these in the constructors using the 
convenience constants `pybomb.BaseClient.RESPONSE_FORMAT_JSON` and `pybomb.BaseClient.RESPONSE_FORMAT_XML`. 
The default return format is `JSON`

###Instantiation example
This is the same format for all the clients, but here's some examples using the `GamesClient`:
   
    import pybomb
    
    # Use default `JSON` return type
    api_key = 'your key'
    games_client = GamesClient(api_key)
    
    # Use `XML` return type
    games_client = GamesClient(api_key, pybomb.BaseClient.RESPONSE_FORMAT_XML)
