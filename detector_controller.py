import sys
import cognitive_face as CF
from PyQt5.QtWidgets import QApplication
from detector_view import MainWindow


def main():
    key = '53be708c65394e50afd4688fe12b468f'
    CF.Key.set(key)

    base_url = 'https://australiaeast.api.cognitive.microsoft.com/face/v1.0'
    CF.BaseUrl.set(base_url)

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
