# SafeHaven: Real-Time Reassurance. Re:invented. 
# Submission for AWS DeepLens Challenge (the “Hackathon”) #AWSDeepLensChallenge

SafeHaven was designed to protect vulnerable people living alone, by enabling them to identify "Who Is At The Door" using an Alexa Skill. Unknown visitors trigger SMS or email alerts to relatives or carers, via an SNS subscription. 

DeepLens acts as a sentry on the doorstep, storing the faces of every visitor. When a visitor is "Rekognised", their name is stored in a DynamoDB table, ready to be retrieved by an Alexa Skill. 

AWS have democratised many complex computational elements (particularly in the realm of machine learning), making it possible for developers to build complex systems by configuration. 

SafeHaven is only possible because DeepLens allows us to deploy a light-weight, yet powerful Face-Detection neural network to a compact device. DeepLens minimises network traffic, so we don't need to stream high volumes of video data to the cloud.
