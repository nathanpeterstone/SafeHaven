# SafeHaven: Real-Time Reassurance. Re:invented. 
### Submission for AWS DeepLens Challenge (the “Hackathon”) #AWSDeepLensChallenge
### Devpost Entry - https://devpost.com/software/safehaven-d7rauk
### YouTube Demo Video - https://youtu.be/5DDRvRHZ1Qs


SafeHaven was designed to protect vulnerable people living alone, by enabling them to identify "Who Is At The Door" using an Alexa Skill. Unknown visitors trigger SMS or email alerts to relatives or carers, via an SNS subscription. 

DeepLens acts as a sentry on the doorstep, storing the faces of every visitor. When a visitor is "Rekognised", their name is stored in a DynamoDB table, ready to be retrieved by an Alexa Skill. 

AWS have democratised many complex computational elements (particularly in the realm of machine learning), making it possible for developers to build complex systems by configuration. 

SafeHaven is only possible because DeepLens allows us to deploy a light-weight, yet powerful Face-Detection neural network to a compact device. DeepLens minimises network traffic, so we don't need to stream high volumes of video data to the cloud.


## Files included in this repo

#### Overview

SafeHaven Architecture.pdf = detailed overview of our SafeHaven AWS implementation



#### Lambda Functions

deeplens-face-detection.zip = 

safe-haven-analyse-faces-function.zip = 

safe-haven-rekognition-image-upload.zip = 

safe-haven-who-is-at-the-door-function.zip = 



## Folder structure in the AWS S3 Bucket called “safe-haven-images” (also see Architecture PDF)

-- **"DeepLens"**: Output from deeplens – when a face is detected, the whole frame image is uploaded. A trigger on this bucket runs the lambda function “safe-haven-analyse-faces-function”

-- **"Rekognition-Images"**: Where Rekognition Collection images are uploaded by a user. The user has already tagged the image with meta data “x-amz-meta-fullname”, which holds the person’s name. A trigger on this folder goes to Rekognition, which adds the image to a Rekognition Collection; and returns a Unique ID, which is then uploaded (along with meta data) to a DynamoDB table.

-- **"Unknown-Images"**: If the lambda function “safe-haven-analyse-faces-function” cannot match the face returned from Rekognition, then that image is stored in “Unknown-Images” and a message is posted to an SNS topic, which is subscribed to by a SMS recipient.


