import os
from kursovaya.detector_model import Video, Analyzers
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
import cognitive_face as CF
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_ui()

    def main_ui(self):
        self.ui = uic.loadUi('untitled.ui')
        self.ui.setStyleSheet('background-image: url(bg3.jpg); color: white;')
        self.dir_path = os.path.abspath(os.curdir)
        self.ui.framePB.setValue(0)
        self.ui.analyzerPB.setValue(0)
        self.ui.openButton.clicked.connect(self.showDialog)
        self.ui.progressL.moveCursor(QTextCursor.End)
        sb = self.ui.progressL.verticalScrollBar()
        sb.setValue(sb.maximum())

        self.ui.show()

    def showDialog(self):
        self.ui.progressL.clear()
        self.ui.progressL.insertPlainText('Program started.')
        self.ui.framePB.setValue(0)
        self.ui.analyzerPB.setValue(0)
        self.ui.res.setText('')
        while True:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.mp4')[0]
            if fname == '':
                self.ui.progressL.insertPlainText('\nYou must select a file!')
                return None
            else:
                break
        self.vid = Video(fname)
        self.vid.frames()
        self.framing()
        self.an = Analyzers(self.vid)
        try:
            res = self.analyzing()
            self.ui.res.setText(res[0] + '.')
            self.deleting()
        except CF.util.CognitiveFaceException:
            self.deleting()
            self.ui.progressL.insertPlainText(str('\nConecting to Face API Error!'))

    def framing(self):
        completed = 0
        i = 0
        while completed < 100:
            completed += 100 / self.vid.frames_number
            self.ui.framePB.setValue(completed)
            self.ui.progressL.moveCursor(QTextCursor.End)
            self.ui.progressL.insertPlainText(str('\n' + self.vid.cr[i]))
            i += 1

    def analyzing(self):

        all_vid_em = []
        completed = 0
        analyzed = 0

        for numb in range(self.vid.frames_number):
            frame_em, emotions = self.an.frame_analyzer(str(self.dir_path + '\\frames\\frame' + str(numb) + '.jpg'))
            if frame_em is None:
                continue
            all_vid_em.append(frame_em)
            completed += 100 / self.vid.frames_number
            self.ui.analyzerPB.setValue(completed)
            self.ui.progressL.insertPlainText(str('\nFrame number ' + str(analyzed) + ' was analyzed.'))
            for i in range(len(emotions)):
                self.ui.progressL.insertPlainText(str('\nFounded face emotion:\n' + str(emotions[0])))
            analyzed += 1

        main_emotion_dict = {'anger': 0, 'contempt': 0, 'disgust': 0, 'fear': 0, 'happiness': 0, 'neutral': 0,
                             'sadness': 0,
                             'surprise': 0}
        for frame in all_vid_em:
            main_emotion_dict[frame[0]] += 1

        return self.an.selecting_main(main_emotion_dict)

    def deleting(self):
        for i in range(self.vid.frames_number + 1):
            os.remove(str(os.path.abspath(os.curdir) + '\\frames\\frame' + str(i) + '.jpg'))
            self.ui.progressL.insertPlainText(str('\n' + os.path.abspath(os.curdir) + '\\frames\\frame' + str(i)
                                                  + '.jpg') + ' was removed.')

        try:
            os.rmdir(str(os.path.abspath(os.curdir) + '\\frames'))
        except OSError:
            self.ui.progressL.insertPlainText(str(self.ui.progressL.text() + '\nDirectory was not removed.'))
