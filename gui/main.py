import logging
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
app = QtWidgets.QApplication(sys.argv)
log_html_format =  \
        "<span style=\" font-size:10pt; font-weight:400; color:{};\" ><pre>{}<\pre></span>"


class QLogger(QObject, logging.Handler):
    new_record = QtCore.pyqtSignal(object)
   
    def __init__(self, parent):
        super().__init__()
        self.is_error = False

    def emit(self, record):
        msg = self.format(record)
        match record.levelno:
            case logging.DEBUG:
                msg = log_html_format.format('gray', msg)
            case logging.INFO:
                msg = log_html_format.format('black', msg)
            case logging.WARNING:
                msg = log_html_format.format('orange', msg)
            case logging.ERROR:
                msg = log_html_format.format('red', msg)
            case logging.CRITICAL:
                msg = log_html_format.format('violet', msg)

        self.new_record.emit(msg)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Logging window')

        self.log_widget = QtWidgets.QPlainTextEdit(self)
        self.log_widget.setReadOnly(True)

        self._log_view = QtWidgets.QWidget(self)

        self.set_logging()
       
        vertical_layout =  QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.log_widget)

        self._log_view.setLayout(vertical_layout)

        log.debug('Debug')
        log.info('Info')
        log.warning('Warning')
        log.error('Error')
        log.critical('Critical')

        self.setCentralWidget(self.log_widget)

    def set_logging(self):
        log_format = '''%(asctime)s %(name)s %(levelname)s: %(message)s'''
        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")

        self.logger = QLogger(self)
        self.logger.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(self.logger)
        self.logger.new_record.connect(self.log_widget.appendHtml)
 


def main():


    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":

    main()

