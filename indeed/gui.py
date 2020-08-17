import sys
from multiprocessing import Process, Manager

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QTextBrowser, QComboBox, QHBoxLayout, QVBoxLayout

from indeed.spiders.indeed_crawler import IndeedSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from indeed import settings as my_settings


def crawl(Q, ua, is_obey, start_url, var):
    # CrawlerProcess
    crawler_settings = Settings()
    my_settings.USER_AGENT = ua
    my_settings.ROBOTSTXT_OBEY = is_obey
    page = var//10
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(crawler_settings)
    process.crawl(IndeedSpider, Q=Q, start_url=start_url, page=page)
    process.start()


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.setWindowTitle('IndeedCrawler')

        self.url_line = QLineEdit(self)  # Get start url
        self.ua_line = QLineEdit(self)  # Input USER_AGENT
        self.obey_combo = QComboBox(self)  # Decide ROBOTSTXT_OBEY
        self.job_num = QLineEdit(self)
        self.obey_combo.addItems(['Yes', 'No'])
        self.log_browser = QTextBrowser(self)  # Log output
        self.crawl_btn = QPushButton('Start Crawling', self)  # Start Crawling
        self.crawl_btn.clicked.connect(self.crawl_slot)

        # 布局
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(QLabel('Input start url'))
        self.v_layout.addWidget(self.url_line)
        self.v_layout.addWidget(QLabel('Iinput total job numbers to be crawled'))
        self.v_layout.addWidget(self.job_num)
        self.h_layout.addWidget(QLabel('Input User-Agent'))
        self.h_layout.addWidget(self.ua_line)
        self.h_layout.addWidget(QLabel('Obey Robot.txt'))
        self.h_layout.addWidget(self.obey_combo)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(QLabel('Output'))
        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addWidget(self.crawl_btn)
        self.setLayout(self.v_layout)

        self.Q = Manager().Queue()
        self.log_thread = LogThread(self)

    def crawl_slot(self):
        if self.crawl_btn.text() == 'Start Crawling':
            self.log_browser.clear()
            self.crawl_btn.setText('Stop Crawling')
            start_url = self.url_line.text()
            ua = self.ua_line.text().strip()
            try:
                job_num = int(self.var.text())
            except:
                print('Jobs number must be a integer')
            is_obey = True if self.obey_combo.currentText() == 'Yes' else False
            self.p = Process(target=crawl, args=(self.Q, ua, is_obey, start_url, var))
            self.p.start()
            self.log_thread.start()
        else:
            self.crawl_btn.setText('Start Crawling')
            self.p.terminate()
            self.log_thread.terminate()

    def closeEvent(self, event):
        self.p.terminate()
        self.log_thread.terminate()


class LogThread(QThread):
    def __init__(self, gui):
        super(LogThread, self).__init__()
        self.gui = gui

    def run(self):
        while True:
            if not self.gui.Q.empty():
                self.gui.log_browser.append(self.gui.Q.get())

                # Make sure slider can move to the bottom
                cursor = self.gui.log_browser.textCursor()
                pos = len(self.gui.log_browser.toPlainText())
                cursor.setPosition(pos)
                self.gui.log_browser.setTextCursor(cursor)

                if 'Crawling Finished' in self.gui.log_browser.toPlainText():
                    self.gui.crawl_btn.setText('Start Crawling')
                    break

                # Sleep 1000ms to avoid crash
                self.msleep(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
