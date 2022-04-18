# 

# Web-Scrap-Assignment

### Script Description

As per assignment, the solution consists of:
- **Dockerfile** : Responsible for building environment for code run.
    - Built from Ubuntu 20
    - Install python 3.8 along with other required modules.
- **Requirements.txt** : Consists of required python modules along with their specific versions for deterministic builds.

- **fetch.py** : Consists of the following:
    - A cli interface that supports download/metadata operations.
    - The --operation download flag followed by a list of absolute urls fetches the webpages and stores them inside "fetch" directory.
    - The --operation metadata flag followd by a list of absolute urls gets the specified metadata for the urls

### Script Output Screenshots

Docker Image Build:

<img width="1745" alt="Screenshot 2022-04-18 at 6 19 47 PM" src="https://user-images.githubusercontent.com/17096303/163814544-b5836765-8de3-4cdc-add4-5d818ccea936.png">
<img width="1237" alt="Screenshot 2022-04-18 at 6 20 08 PM" src="https://user-images.githubusercontent.com/17096303/163814582-9ac4493a-04fb-42b7-93e7-d9c09a834044.png">

Fetch WebPages:<br>
<img width="850" alt="Screenshot 2022-04-18 at 6 25 04 PM" src="https://user-images.githubusercontent.com/17096303/163814638-045a320c-9695-42ff-ac34-3b11aee322cc.png">

Get Metadata for the WebPages:
<img width="913" alt="Screenshot 2022-04-18 at 6 25 39 PM" src="https://user-images.githubusercontent.com/17096303/163814645-6ccc1407-b489-42cd-9abf-e35789c509e4.png">

Error Handling:

<img width="714" alt="Screenshot 2022-04-18 at 7 13 46 PM" src="https://user-images.githubusercontent.com/17096303/163817108-2dc8696d-7821-4c34-9649-6264e098a1ab.png">
<img width="638" alt="Screenshot 2022-04-18 at 7 14 26 PM" src="https://user-images.githubusercontent.com/17096303/163817118-bdb39868-ee5b-480c-9dc5-7e02065e7078.png">
<img width="814" alt="Screenshot 2022-04-18 at 7 22 45 PM" src="https://user-images.githubusercontent.com/17096303/163818158-44f1b646-d0f9-4dc2-9791-68324ff5b6a0.png">

### What could have been done with more time

- Any code is incomplete without unit tests (which are misssing here, because of time constraint)
- Use of some database for data persistence. For the sake of assignment (and keeping it simple), using a storing in a json on secondary storage. The disadvantage with json is that as the data increases, it has to read and written as a whole everytime, where using csv will increase search time.
- Better code design following SOLID principles and design patterns.
- Use of cache for metadata fetch using 80/20 rule in case of heavy read. 
- Proper logging in log files instead of dumping info on stdout.
- Better validations and error handling.
