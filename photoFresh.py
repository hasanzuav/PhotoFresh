import boto3



BUCKET = "aamazon-rekognition"
KEY = "test.jpg"
# Code to upload test.jpg file to bucket
s3 = boto3.resource('s3')
s3.Object(BUCKET, 'test.jpg').put(Body=open('test.jpg', 'rb'))

def detect_labels(bucket, key, max_labels=10, min_confidence=10, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )
    return response['Labels']

FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")

def detect_faces(bucket, key, attributes=['ALL'], region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        Attributes=attributes,
    )
    return response['FaceDetails']



FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")

def detect_faces(bucket, key, attributes=['ALL'], region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        Attributes=attributes,
    )
    return response['FaceDetails']



for label in detect_labels(BUCKET, KEY):
    print "{Name} - {Confidence}%".format(**label)


for face in detect_faces(BUCKET, KEY):
    print "Face ({Confidence}%)".format(**face)
    # emotions
    for emotion in face['Emotions']:
        print "  {Type} : {Confidence}%".format(**emotion)
    # quality
    for quality, value in face['Quality'].iteritems():
        print "  {quality} : {value}".format(quality=quality, value=value)
    # facial features
    for feature, data in face.iteritems():
        if feature not in FEATURES_BLACKLIST:
            print "  {feature}({data[Value]}) : {data[Confidence]}%".format(feature=feature, data=data)