# SafeHaven: Real-Time Reassurance. Re:invented. 
### Submission for AWS DeepLens Challenge (the “Hackathon”) #AWSDeepLensChallenge
### Devpost Entry - https://devpost.com/software/safehaven-d7rauk
### YouTube Demo Video - https://youtu.be/5DDRvRHZ1Qs
### LinkedIn Nathan Stone - https://www.linkedin.com/in/na7hans7one/
### LinkedIn Peter McLean - https://www.linkedin.com/in/peter-mclean/


SafeHaven was designed to protect vulnerable people living alone, by enabling them to identify "Who Is At The Door" using an Alexa Skill. Unknown visitors trigger SMS or email alerts to relatives or carers, via an SNS subscription. 

DeepLens acts as a sentry on the doorstep, storing the faces of every visitor. When a visitor is "Rekognised", their name is stored in a DynamoDB table, ready to be retrieved by an Alexa Skill. 

AWS have democratised many complex computational elements (particularly in the realm of machine learning), making it possible for developers to build complex systems by configuration. 

SafeHaven is only possible because DeepLens allows us to deploy a light-weight, yet powerful Face-Detection neural network to a compact device. DeepLens minimises network traffic, so we don't need to stream high volumes of video data to the cloud.


## Important DeepLens Note

We have implemented the standard **deeplens-face-detection** model. As such, we have not included json model or parameter files in this repo. When creating your DeepLens project, please package the standard model with the **lambda function called "deeplens-face-detection", which _is_ included in this repo**.


## Files included in this repo

#### Overview

SafeHaven Architecture.pdf = detailed overview of our SafeHaven AWS implementation



#### Lambda Functions

deeplens-face-detection.zip

safe-haven-analyse-faces-function.zip

safe-haven-rekognition-image-upload.zip

safe-haven-who-is-at-the-door-function.zip



## Folder structure in the AWS S3 Bucket called “safe-haven-images” (also see Architecture PDF)

-- **"DeepLens"**: Output from deeplens – when a face is detected, the whole frame image is uploaded. A trigger on this bucket runs the lambda function “safe-haven-analyse-faces-function”

-- **"Rekognition-Images"**: Where Rekognition Collection images are uploaded by a user. The user has already tagged the image with meta data “x-amz-meta-fullname”, which holds the person’s name. A trigger on this folder goes to Rekognition, which adds the image to a Rekognition Collection; and returns a Unique ID, which is then uploaded (along with meta data) to a DynamoDB table.

-- **"Unknown-Images"**: If the lambda function “safe-haven-analyse-faces-function” cannot match the face returned from Rekognition, then that image is stored in “Unknown-Images” and a message is posted to an SNS topic, which is subscribed to by a SMS recipient.



## Prerequisites:
Ensure that your DeepLens device has been configured and registered within the AWS DeepLens console 

All of the elements below should be created in the US-EAST-1 (N. Virginia) region.


## IAM Roles
LambdaRekognitionRole – Attach a new policy called ‘LambdaPermissions’ – see LambdaPermissions.json – You will need to edit the policies to replace the account numbers with your own.

DoorLambdaAlexaSkillRole – Attach a new policy called ‘AlexaSkillPolicy’ – see AlexaSkillPolicy.json


## S3 Buckets
1)	Create a new S3 bucket where all your images will be stored
2)	Create the necessary folders within the S3 bucket as per the folder structure, defined above


## Rekognition
1)	Setup a new Rekognition Collection– see https://docs.aws.amazon.com/rekognition/latest/dg/create-collection-procedure.html


## DynamoDB Tables
1)	Create a new table to store the Rekognition collection IDs and people names – see see safe-haven-rekognition-collection.txt script script
2)	Create a new table to store the face detection history – see **safe-haven-facial-history.txt** script
3)	Create a new table to store the last person detected – see **safe-haven-last-person.txt** script


## SNS
1)	Create a new SNS topic called **NotifyMe**
2)	Create a subscription to this topic via either SMS or Email


## Alexa Skill

You will need to create a new Alexa skill, and get the Skill Id (as this is required within the lambda function configuration)

Alexa Skill setup is beyond the scope of this guide.


## Lambda Functions
1)	Create **‘deeplens-facial-detection’** lambda function, selecting **Python 2.7**.  The zip file included here should be uploaded. This function should run under the **AWSDeepLensLambdaRole**.

_N.B. This function may already have been created as part of the AWS DeepLens initial setup – if that is the case, upload the .zip file included here and publish a new version of the function_

---- a.	Edit the ‘greengrassHelloWorld.py’ script, change the bucket names in lines 54 & 56 to be the S3 bucket you setup previously

2)	Create **‘safe-haven-rekognition-image-upload’** lambda function, selecting **Python 2.7**. The zip file included here should be uploaded.  This function should run under the **LambdaRekognitionRole**.

---- a. Edit the **‘lambda_function.py’** script, change line 11 to be the DynamoDB table for the Rekognition Collection

---- b. Edit the **‘lambda_function.py’** script, change line 14 to be the Rekognition Collection name (as per the Rekognition setup)

---- c. Add a trigger from **S3**, using the bucket created earlier, the prefix **‘Rekognition-Images/’**, Event Type **ObjectCreated**, Suffix **jpg**


3)	Create **‘safe-haven-analyse-faces-function’** lambda function, selecting **Python 2.7**.  The zip file included here should be uploaded.  This function should run under the **LambdaRekognitionRole**.

---- a.	Edit the **‘lambda_function.py’** script, change line 13 to be the Rekognition Collection name (as per the Rekognition setup)

---- b.	Edit the **‘lambda_function.py’** script, change line 14 to be the DynamoDB table for the face detection history

---- c.	Edit the **‘lambda_function.py’** script, change line 15 to be the DynamoDB table for the last person detected

---- d.	Edit the **‘lambda_function.py’** script, change line 16 to be the SNS ARN

---- e.	Add the following Environment variables:

-------- i.	unknown_images_bucket            [This should be your S3 bucket name]

-------- ii.	unknown_images_folder           Unknown-Images


f.	Add a trigger from **S3**, using the bucket created earlier, the prefix **‘DeepLens/’**, Event Type **ObjectCreated**, Suffix **jpg**


4)	Create **‘safe-haven-who-is-at-the-door-function’** lambda function, selecting **Python 3.6**.  The zip file included here should be uploaded.  This function should run under the **DoorLambdaAlexaSkillRole**.

---- a.	Add the following Environment variables:

-------- i.	unique_id           [Any value you want as it is not used]

-------- ii.	greeting_msg    Welcome to Safe Haven.  Just ask me who is at the door.

-------- iii.	metrics_table    [DynamoDB table for the last person detected]

-------- iv.	intent_name     WhoIsAtTheDoor

-------- v.	slot_name          metric

-------- vi.	exit_msg             Thank you for using Safe Haven. Have a nice day!


---- b.	Add a trigger from Alexa Skills Kit, entering your Alexa Skill Id where necessary


