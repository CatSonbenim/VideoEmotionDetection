import cv2
import os
import cognitive_face as CF


class Video:

    def __init__(self, path):
        self.video_path = path
        self.cr = []
        self.video = cv2.VideoCapture(self.video_path)
        self.frames_number = 0

    def frames(self):
        try:
            if not os.path.exists('frames'):
                os.makedirs('frames')
        except OSError:
            print('Error: Creating directory of data')

        current_frame = 0

        while True:

            ret, frame = self.video.read()

            name = '.\\frames\\frame' + str(current_frame) + '.jpg'
            self.cr.append(name + ' was created.')
            cv2.imwrite(name, frame)

            current_frame += 1
            self.frames_number += 1
            if not ret:
                self.frames_number -= 1
                break

        self.video.release()


class Analyzers:

    def __init__(self, video):

        if not isinstance(video, Video):
            raise ValueError('Not that type of video. There is a spacial class!')

        self.dir_path = os.path.abspath(os.curdir)
        self.frame_numbers = video.frames_number
        self.face_em = []

    def selecting_main(self, dictionary):
        bv = 0
        main_thing = ''

        values = list(dictionary.values())
        keys = list(dictionary.keys())
        for val in range(len(values)):
            if values[val] > bv:
                main_thing = keys[val]
                bv = values[val]

        return [main_thing, bv]


    def frame_analyzer(self, frame_path):

        all_faces = CF.face.detect(frame_path, attributes='emotion')

        if all_faces is []:
            return None

        self.face_em = []
        frame_emotions = []

        for face in all_faces:
            face_emotions = face['faceAttributes']['emotion']
            self.face_em.append(face_emotions)
            frame_emotions.append(self.selecting_main(face_emotions))

        main_emotion_dict = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'neutral': 0,
                             'sadness': 0,
                             'surprise': 0}
        for f in frame_emotions:
            main_emotion_dict[f[0]] += 1

        return self.selecting_main(main_emotion_dict), self.face_em
