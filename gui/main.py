import logging
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
app = QtWidgets.QApplication(sys.argv)

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
    log_html_format =  \
            "<span style=\" font-size:10pt; font-weight:400; color:{};\" ><pre>{}<\pre></span>"
    levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


    def __init__(self):
        super().__init__()

        self.setWindowTitle('Logging window')

        self.log_widget = QtWidgets.QPlainTextEdit(self)
        self.log_widget.setReadOnly(True)

        self._log_view = QtWidgets.QWidget(self)

        self.set_logging()
       
        vertical_layout =  QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.log_widget)

        self.set_check_boxes()
        vertical_layout.addLayout(self.check_boxes_layout)

        self._log_view.setLayout(vertical_layout)
        i = 1
        N = 1000
        while i < N:
            log.debug('Debug')
            log.info('Info')
            log.warning('Warning')
            log.error('Error')
            log.critical('Critical')
            i += 1

        self.log_file_to_gui('log.log')

        self.setCentralWidget(self._log_view)

    def set_check_boxes(self):

        horizontal_layout = QtWidgets.QHBoxLayout()

        self.DebugC = QtWidgets.QCheckBox('Debug')
        self.DebugC.setChecked(True)
        self.DebugC.stateChanged.connect(lambda: \
                self.add_log_level('DEBUG') if self.DebugC.isChecked()\
                else self.remove_log_level('DEBUG'))
        horizontal_layout.addWidget(self.DebugC)

        self.InfoC = QtWidgets.QCheckBox('Info')
        self.InfoC.setChecked(True)
        self.InfoC.stateChanged.connect(lambda: \
                self.add_log_level('INFO') if self.InfoC.isChecked()\
                else self.remove_log_level('INFO'))
        horizontal_layout.addWidget(self.InfoC)


        self.WarningC = QtWidgets.QCheckBox('Warning')
        self.WarningC.setChecked(True)
        self.WarningC.stateChanged.connect(lambda: \
                self.add_log_level('WARNING') if self.WarningC.isChecked()\
                else self.remove_log_level('WARNING'))
        horizontal_layout.addWidget(self.WarningC)

        self.ErrorC = QtWidgets.QCheckBox('Error')
        self.ErrorC.setChecked(True)
        self.ErrorC.stateChanged.connect(lambda: \
                self.add_log_level('ERROR') if self.ErrorC.isChecked()\
                else self.remove_log_level('ERROR'))
        horizontal_layout.addWidget(self.ErrorC)

        self.check_boxes_layout = horizontal_layout



    def add_log_level(self, level = None):
        start_time = time.time()
        self.levels.append(level)
        self.refresh_log()
        deltat = start_time - time.time()
        print(deltat)

    def remove_log_level(self, level = None):
        self.levels.remove(level)
        self.refresh_log()

    def refresh_log(self):
        self.log_widget.clear()
        self.log_file_to_gui('log.log')

    def set_logging(self):
        log_format = '''%(asctime)s %(name)s %(levelname)s: %(message)s'''
        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")

        self.file_handler = logging.FileHandler('log.log')
        self.file_handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(self.file_handler)

    def log_file_to_gui(self, filep):
        with open(filep, 'r') as f:
            line = f.readline()
            while line:
                line = f.readline()
                _log = self.plain_to_html(line[0:-1])
                if not(_log is None):
                    self.log_widget.appendHtml(_log)

    def plain_to_html(self, logline):
        log_level = ''
        html_log = None

        for level in self.levels:
            log_level_found = level in logline
            if log_level_found:
                log_level = level
                break

        match log_level:
           case 'DEBUG':
               html_log = self.log_html_format.format('gray', logline)
           case 'INFO':
               html_log = self.log_html_format.format('black', logline)
           case 'WARNING':
               html_log = self.log_html_format.format('orange', logline)
           case 'ERROR':
               html_log = self.log_html_format.format('red', logline)
           case 'CRITICAL':
               html_log = self.log_html_format.format('violet', logline)

        return  html_log

       

def main():


    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":

    main()

