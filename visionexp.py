import io
import os
from PIL import Image, ImageDraw

# imports the google cloud vision client library
from google.cloud import  vision
from google.cloud.vision import types




print ('show something')


# initiates a client
client = vision.ImageAnnotatorClient()


# The name of the image file to annotate
path = os.path.join(
    os.path.dirname(__file__),
    'resources/text.png')




# Performs label detection on the image file



def create_image(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    return image

def detect_labels(image):
    """Detects labels in an image."""
    response = client.label_detection(image=image)
    labels = response.label_annotations


    print('Labels:')
    for label in labels:
        print (label)
        print(label.description)

def detect_text(image):
    """Detects labels in an image."""
    response = client.text_detection(image=image)




    texts = response.text_annotations


    for text in texts:
        print (text.confidence)
        print(text.score)
        print(text.description)
        print("-------")

def detect_faces(image):
    """Detects faces in an image."""
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    facecount =1
    for face in faces:

        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))



        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        # gathering vertices list to draw a polygon line around the face
        verticeslist = []
        for vertex in face.bounding_poly.vertices:
            point = (vertex.x,vertex.y)
            verticeslist.append(point)

        print (verticeslist)

        print('face bounds: {}'.format(','.join(vertices)))

        imagecan = Image.open(path)
        print(imagecan.size)
        width, height = imagecan.size
        draw = ImageDraw.Draw(imagecan)
        draw.polygon(verticeslist, outline='white')
        # save the image with a facecount
        imagecan.save('editface'+str(facecount)+'.jpg')

        facecount += 1


image=create_image(path)

# print ("running face detection")
# detect_faces(image)
# print ("running label detection")
# detect_labels(image)
print ("running text detection")
detect_text(image)