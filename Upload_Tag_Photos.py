import boto3

s3 = boto3.resource('s3')

images=[('test-1.jpg', 'Mr Test Person 1'),
        ('test-2.jpg', 'Mr Test Person 2')
       ]

for image in images:
  file = open(image[0],'rb')
  object = s3.Object('safe-haven-images','Rekognition-Images/'+ image[0])
  ret = object.put(Body=file, Metadata={'FullName':image[1]})
