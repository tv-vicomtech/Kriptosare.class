## REST-API functions

<p> The Rest API always return a JSON following the tag.data.schema.json structure. The spected result will appeared in a field called custom_properties, following this structure:</p>

```json
custom_properties={
	error : int,
	message : string,
	result : {}
}
```

<p> where error is 0 or 1, if it is 1 the message return the found error, otherwise, if is 0 message return null value and result variable show the the retrived data</p>
### 1 Address Classification

FUNCTION NAME = search_address

GET REQUEST structure: `http://ip:port/search_address?key=xxx&currency=yyy`

POST REQUEST structure:

```json
input = {
  "uuid": "{uuid type string}",
  "version": number,
  "key_type":  "a",
  "key": "string, bitcoin address",
  "tag": "string",
  "contributor": "string",
  "tag_optional": {
    "currency": "3 char"
  }
}
```

<p> xxx/key = crytocurrency address<br>yyy/currency = BTC for Bitcoin</p>
<<<<<<< HEAD
=======

>>>>>>> 3d795f3a6304fdc95df2626cedc2f94769332b11
##########################################################

RETURN:

```json
result={
  "uuid": "{uuid type string}", 
  "version": number,
  "key_type": "a", 
  "key": "string, bitcoin address", 
  "tag": "string", 
  "contributor": "string",
  "tag_optional": {
    "currency": "BTC"
  },
  "custom_properties": {
    "error": 0|1, 
    "message": "string", 
    "result": {
      "exchange": float, 
      "gambling": float, 
      "market": float, 
      "miner": float,
      "mixer": float, 
      "service": float, 
      "user": "string"
    }
  } 
}

```

<p> key = cryptocurrency address requested<br>currency = BTC for Bitcoin<br>user = cluster name<br>exchange, gambling, market, pool, mixer, service = prediction class percentage <br>version = string version (current 1.0.0)</p>
### 2 List Classes

FUNCTION NAME = list_classes

GET REQUEST structure: `http://ip:port/list_classes?currency=xxx`

POST REQUEST structure:

```json
input={
  "uuid": "{uuid type string}",
  "version": number,
  "key_type":  "a",
  "key": "string, bitcoin address",
  "tag": "string",
  "contributor": "string",
  "tag_optional": {
      "currency": "3 char"
  }
}
```

<p>xxx/currency = BTC for Bitcoin</p> 
<<<<<<< HEAD
=======

>>>>>>> 3d795f3a6304fdc95df2626cedc2f94769332b11
#####################################################

RETURN:

```json
output = { 
  "uuid": "{uuid type string}",
  "version": number  
  "key_type": "a", 
  "key": "string, bitcoin address",
  "tag": "string",
  "contributor": "string",
  "tag_optional": {
    "currency": "BTC"
  },
  "custom_properties": {
    "error": 0|1, 
    "message": "", 
    "result": [
      {
        "abbreviation": "mxr", 
        "currency": "BTC", 
        "label": 5, 
        "name": "mixer"
      }, 
      {
        "abbreviation": "exc", 
        "currency": "BTC", 
        "label": 1, 
        "name": "exchange"
      }, 
      {
        "abbreviation": "gmb", 
        "currency": "BTC", 
        "label": 2, 
        "name": "gambling"
      }, 
      {
        "abbreviation": "mpo", 
        "currency": "BTC", 
        "label": 4, 
        "name": "miner"
      }, 
      {
        "abbreviation": "ser", 
        "currency": "BTC", 
        "label": 6, 
        "name": "service"
      }, 
      {
        "abbreviation": "mrk", 
        "currency": "BTC", 
        "label": 3, 
        "name": "market"
      }
    ]
  }
}
```

<p> currency = BTC for Bitcoin <br> label = the integer id referred to the class in our classification<br>name = name of the classes <br>abbreviation = abbreviation of the name of the classes (3 char)</p>name of the classes:
1. Exchange - exc
2. Gambling - gmb
3. Market - mrk
4. Miner - mpo
5. Mixer  - mxr
6. Service - ser

### 3 Class Confidence

FUNCTION NAME = class_checker

GET REQUEST structure: `http://ip:port/class_checker?key=xxx&currency=yyy&class=zzz&confidence=jj`

POST REQUEST structure:

```json
input = {
  "uuid": "{uuid type string}",
  "version": number,
  "key_type":  "a",
  "key": "string, bitcoin address",
  "tag": "string",
  "contributor": "string",
  "tag_optional": {
    "actor_type": "exchange | gambling | market | miner | mixer | service",
    "currency": "3 char"
  },
  "custom_properties":{
    "confidence": number
  }
}
```

<p>xxx/key = crytocurrency address<br>yyy/currency = BTC for Bitcoin <br> zzz/class = exchange | gambling | market | miner | mixer | service (for bitcoin) <br> jj/confidence = accuracy estimation percentage that the address belong to the chosen class </p>
<<<<<<< HEAD
=======

>>>>>>> 3d795f3a6304fdc95df2626cedc2f94769332b11
####################################################

RETURN:

```json
result={
  "uuid": "{uuid type string}", 
  "version": number,
  "key_type": "a",
  "key": "string, bitcoin address", 
  "tag": "string", 
  "contributor": "string", 
  "custom_properties": {
    "error": 0|1, 
    "message": "string", 
    "result": {
      "value": "True|False"
    }
  }  
}
```

value = Boolean that return if the condition of address/currency/class/confidence are verified or not!



### Quickly Examples
<<<<<<< HEAD

First call GET: `http://ip:port/search_address?key=17A16QmavnUfCW11DAApiJxp7ARnxN5pGX&currency=BTC`

Second call GET: `http://ip:port/list_classes?currency=BTC`

Third call GET: `http://ip:port/class_checker?key=17A16QmavnUfCW11DAApiJxp7ARnxN5pGX&currency=BTC&class=Exchange&confidence=99`






=======
>>>>>>> 3d795f3a6304fdc95df2626cedc2f94769332b11

First call GET: `http://ip:port/search_address?key=17A16QmavnUfCW11DAApiJxp7ARnxN5pGX&currency=BTC`

Second call GET: `http://ip:port/list_classes?currency=BTC`

<<<<<<< HEAD










 

=======
Third call GET: `http://ip:port/class_checker?key=17A16QmavnUfCW11DAApiJxp7ARnxN5pGX&currency=BTC&class=Exchange&confidence=99`
>>>>>>> 3d795f3a6304fdc95df2626cedc2f94769332b11
