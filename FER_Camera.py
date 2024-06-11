
import cv2
import numpy as np
import os



face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  




size = 2
frames_count = 10 # validate the face to rechek the frames 10 times
thresss = 100 # thress hold value to validate the face
confirmation_count = 0
fn_haar = 'haarcascade_frontalface_default.xml'
fn_dir = 'att_faces'

#
# Traning code
#

# Part 1: Create fisherRecognizer
print('Training...')

fn_dir = "att_faces"

pred = []

faces_name = []

# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)

# Get the folders containing the training data
for (subdirs, dirs, files) in os.walk(fn_dir):

    # Loop through each folder named after the subject in the photos
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)

        # Loop through each photo in the folder
        for filename in os.listdir(subjectpath):

            # Skip non-image formates
            f_name, f_extension = os.path.splitext(filename)
            if(f_extension.lower() not in
                    ['.png','.jpg','.jpeg','.gif','.pgm']):
                print("Skipping "+filename+", wrong file type")
                continue
            path = subjectpath + '/' + filename
            lable = id

            # Add to training data
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(im_width, im_height) = (112, 92)

# Create a Numpy array from the two lists above
(images, lables) = [np.array(lis) for lis in [images, lables]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
#model = cv2.face.createFisherFaceRecognizer()
#model = cv2.face.FisherFaceRecognizer_create()
model = cv2.face.LBPHFaceRecognizer_create()
#model = cv2.face.LBPHFaceRecognizer_create()
#model = cv2.face.EigenFaceRecognizer_create()
model.train(images, lables)



import os

# function write_party_votes to text file 
def write_party_votes(parties):
    with open('party_votes.txt', 'w') as file:
        for party in parties:
            file.write(f"{party.name} : {party.vote}\n")


# class of party 
class Party():
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        self.vote = 0

    def cast_vote(self):
        self.vote += 1

    


parties = []

bjp = Party("BJP", "bjp.jpeg")
congress = Party("CONGRESS", "inc.png")
sp = Party("SP", "sp.jpg")
bsp = Party("BSP", "bsp.jpeg")
aap = Party("AAP", "aap.jpeg")

parties.append(bjp)
parties.append(congress)
parties.append(bsp)
parties.append(aap)
parties.append(sp)


class Voter():

    def __init__(self, name):
        self.name = name
        self.voted = False



voters = []



elon = Voter("Elon")
bill = Voter("Bill")
sachin = Voter("sachin")
saurabh = Voter("saurabh")
analp = Voter("analp")
anubha = Voter("anubha")

voters.append(elon)
voters.append(bill)
voters.append(sachin)
voters.append(saurabh)
voters.append(analp)
voters.append(anubha)





class VideoCamera:

    status = ["valid", "already_voted", "unauthorised"]

    def __init__(self):
        # open camera 0= default camera
        self.video = cv2.VideoCapture(0)
        self.urls = None
        self.emotion = None
        size = 2
        self.frames_count = 10
        self.thresss = 110
        self.confirmation_count = 0
        self.voter = "unauthorized"
    
    def __del__(self):
        self.video.release()

        
    # return status of the user after processing image  
    def get_status(self):
        print(self.voter)
        for voter in voters:
            if voter.name.upper() ==  self.voter.upper():
                if voter.voted:
                    return {"status": self.status[1], "name": voter.name}
                
                return  {"status": self.status[0], "name":  voter.name}
            
        return  {"status": self.status[2], "name": self.status[2]}
    
    # function to cast vote 
    def vote(self, party_name):
        for voter in voters:
            if voter.name.upper() ==  self.voter.upper():
                prty_indx = 0
                for party in parties:
                    if party.name == party_name:
                        parties[prty_indx].cast_vote()
                        voter.voted = True
                        write_party_votes(parties)
                        return True
                    prty_indx+=1
        
        return False
        
    #return all parties 
    def get_parties(self):
        return parties
    
    #return current frame of camera
    def get_frame(self):
        ret,test_img=self.video.read()# captures frame and returns boolean value and captured image  
          
        
        gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)  

        gray = gray_img
        # Resize to speed up detection (optinal, change size above)
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

         # Detect faces and loop through each one
        faces = face_haar_cascade.detectMultiScale(mini)
        for i in range(len(faces)):
            face_i = faces[i]

            # Coordinates of face after scaling back by `size`
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (im_width, im_height))

            # Try to recognize the face
            prediction = model.predict(face_resize)
            cv2.rectangle(test_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # [1]
            # Write the name of recognized face
            #cv2.putText(frame,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
            if prediction[1]< self.thresss:
                                         
                #print('%s - %.0f' % (names[prediction[0]],prediction[1]))
                #faces_name.append(names[prediction[0]])
                self.confirmation_count += 1
                if self.confirmation_count  > self.frames_count:
                    #print("Authorized")
                    self.voter = names[prediction[0]]
                    self.confirmation_count = self.frames_count
                    cv2.putText(test_img,'%s - %.0f' % ("Authorized "+names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                else:
                    cv2.putText(test_img,'%s - %.0f' % ("validating "+names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 255, 255))
                
            else:
                
                self.confirmation_count -= 1
                if self.confirmation_count < (-1*self.frames_count):
                    #print("Unauthorized")
                    self.voter = "unauthorized"
                    self.confirmation_count = -1*self.frames_count
                    cv2.putText(test_img,'unauthorized',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 0, 255))

                else:
                    cv2.putText(test_img,'trying to recognized',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0))



       

        resized_img = cv2.resize(test_img, (1000, 600))

        _, jpeg = cv2.imencode('.jpg', resized_img)

        return jpeg.tobytes()