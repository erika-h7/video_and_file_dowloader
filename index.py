from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import os
from PyQt5.uic import loadUiType
import urllib.request

import pafy
from pytube import YouTube
import humanize

ui, _ = loadUiType("main.ui")


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUi()
        self.Handle_Buttons()

    def InitUi(self):
        ## contain all ui changes in loading
        pass

    def Handle_Buttons(self):
        ## handle all buttons in the app

        ## File Downloader
        self.pushButton.clicked.connect(
            self.Download
        )  ## this connects the ui download button page1(file downloader)
        self.pushButton_2.clicked.connect(
            self.Handle_Browse
        )  ## this connects the ui browse button page1(file downloader)

        ## Youtube Video Downloader
        self.pushButton_9.clicked.connect(self.Get_Video_Data)
        self.pushButton_8.clicked.connect(self.Download_Video)
        self.pushButton_7.clicked.connect(self.Save_Browse)


    def Handle_Progress(self, blocknum, blocksize, totalsize):
        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()


    def Handle_Browse(self):
        ## enable browsing to our os, pick save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)"
        )

        print(save_location)

        self.lineEdit_2.setText(str(save_location[0]))


    def Download(self):
        ## download any file
        print("Starting Download")

        ## getting info from ui
        download_url = (
            self.lineEdit.text()
        )  ## this gets the url text from the first line edit in the ui
        save_location = (
            self.lineEdit_2.text()
        )  ## this gets the save location text from the second line edit in the ui

        if download_url == " " or save_location == " ":
            QMessageBox.warning(
                self, "Data error", "Please provide a valid URL or save location"
            )
        else:
            ## this is to start downloading
            try:
                urllib.request.urlretrieve(
                    download_url, save_location, self.Handle_Progress
                )  ## this passes our info to our Handle_Progress method
            except Exception:
                QMessageBox.warning(
                    self,
                    "Download Error",
                    "Please provide a valid URL or save location",
                )
                return

        QMessageBox.information(
            self, "Download Completed", "The Download Completed Successfully"
        )

        self.lineEdit.setText(" ")
        self.lineEdit_2.setText(" ")
        self.progressBar.setValue(0)


    def Save_Browse(self):
        ## save location in the line edit
        pass


    # ██╗   ██╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗    ███████╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
    # ╚██╗ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝    ██╔════╝██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
    #  ╚████╔╝ ██║   ██║██║   ██║   ██║   ██║   ██║██████╔╝█████╗      ███████╗█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
    #   ╚██╔╝  ██║   ██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝      ╚════██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
    #    ██║   ╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝██████╔╝███████╗    ███████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
    #    ╚═╝    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝    ╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

    ################################################################
    ## DOWNLOAD SINGLE YOUTUBE VIDEO
    def Save_Browse(self):
        ## save location in the line edit
        ## enable browsing to our os, pick save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)"
        )

        self.lineEdit_8.setText(str(save_location[0]))



    def Get_Video_Data(self):
        video_url = self.lineEdit_7.text()
        print("video url button clicked")
        print(video_url)

        if video_url == "":
            QMessageBox.warning(self, "Data Error", "Please provide a valid video URL")
        else:

            # pytube3
            video = YouTube(video_url)
            print(video.title)
            print(video.length / 60)
            print(video.author)
            print(video.views)
            print(video.rating)

            # video_streams = video.streams.first()
            # data = "{} {} {}".format(video_streams.mime_type, video_streams.type, video_streams.filesize / 1000000)
            # self.comboBox.addItem(data)


            # experimenting for quality
            video_streams = video.streams.filter(file_extension='mp4')

            print(video_streams)

            for stream in video_streams:
                data = "{} {} {} {}".format(stream.mime_type, stream.type, stream.resolution, str(round(stream.filesize/1000000, 2))+ "Mb")
                self.comboBox.addItem(data)


            # pafy
            # video = pafy.new(video_url)
            # print(video.title)
            # print(video.duration)


    def Download_Video(self):
        video_url = self.lineEdit_7.text()
        save_location = self.lineEdit_8.text()

        if video_url == " " or save_location == " ":
            QMessageBox.warning(
                self, "Data error", "Please provide a valid Video URL or save location"
            )
        else:
            video = YouTube(video_url)
            video_stream = video.streams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(output_path=save_location)

        QMessageBox.information(
            self, "Download Completed", "The Download Completed Successfully"
        )




    def Video_Progress(self, total, received, ratio, rate, time):
        pass


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

