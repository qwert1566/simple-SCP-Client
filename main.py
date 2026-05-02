import PySide6.QtWidgets
import os
from PySide6.QtCore import Qt
import paramiko


NetworkAdpater = "이더넷 어댑터 이더넷 2"
passwd = "123456"
oriDirectory = "/data/data/com.termux/files/home/video/"
downloadDirectory = "D:/ChzzkVideo/모방리"

executeCommand = ""
escape = ["&&", "|"]

def changeDir(a=False):
    global oriDirectory, executeCommand
    if a:
        oriDirectory = getVideoLink.text()
    executeCommand = f'find {oriDirectory} -maxdepth 1 -printf "%y\\t%s\\t%f\\n"'

changeDir()

def size_fmt(size):
    if (size == ""):
        size = "0"
    size = int(size)
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0

    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1

    return f"{size:.2f}{units[i]}"

def get_ip():
    output = os.popen("ipconfig").read()
    output = output.split("\n")
    find = 0
    for i in range(len(output)):
        if NetworkAdpater + ":" == output[i]:
            find = 1
        if find == 2 and len(output) > i and output[i+1] == "":
            getIpOutput.setText(output[i].split(":")[1].strip())
            break
        if find == 1:
            find = 2
        if i+1 == len(output):
            getIpOutput.setText("127.0.0.1")
            break

def get_video():
    if getIpOutput.text() == "":
        getVideoOutput.setPlainText("IP address is wrong.")
        return
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(getIpOutput.text(), port=8022, username="user", password=passwd, timeout=1)
    except Exception as e:
        getVideoOutput.setPlainText(str(e))
        return
    try:
        if (oriDirectory == "" or any(k in oriDirectory for k in escape)):
            getVideoOutput.setPlainText("Remote server directory is not expected.")
            return
        _, stdout, _ = client.exec_command(executeCommand)
        stdout.channel.settimeout(3)
        video_list = []
        oriVideoList = list(reversed(stdout.read().decode("utf-8").strip().split("\n")))
        for i, x in enumerate(oriVideoList):
            if (i == len(oriVideoList)-1):
                continue
            type = ""
            if x.split("\t")[0] == "d":
                type = "[📁]"
            else:
                type = "[📄]"
            video_list.append(f"{size_fmt(x.split("\t")[1])}\t{type} {x.split("\t", 2)[2]}")
        getVideoOutput.setPlainText(("\n".join(video_list)).strip())
    except Exception as e:
        getVideoOutput.setPlainText(str(e))
        return
    client.close()

def get_download():
    global oriDirectory
    if (getIpOutput.text() == ""):
        os.system("start cmd /c " + '"echo IP address is wrong. && pause"')
        return
    if any(t == "" or any(k in t for k in escape) for t in [getIpOutput.text(), oriDirectory, getDownloadCode.text(), downloadDirectory]):
        os.system("start cmd /c " + '"echo Found injection attempt. so you cannot proceed. && pause"')
        return
    if (oriDirectory == ""):
        oriDirectory = "."
    if (oriDirectory[-1] != "/"):
        oriDirectory += "/"
    os.system('start cmd /k ' + f'scp -P 8022 "user@{getIpOutput.text()}":"{oriDirectory}{getDownloadCode.text()}" "{downloadDirectory}"')

def open_download_folder():
    os.startfile(downloadDirectory)

def input_download_folder():
    global downloadDirectory
    downloadDirectory = getDownloadFolder.text()

def changePasswd():
    global passwd
    passwd = getVideoPassword.text()

def changeNAN():
    global NetworkAdpater
    NetworkAdpater = AutoIpValue.text()

QtWidget = PySide6.QtWidgets
app = QtWidget.QApplication([])

if os.name != "nt":
    QtWidget.QMessageBox.critical(None, "Error", "Can running only Windows")
    exit()

content = QtWidget.QWidget()
content.setProperty("class", "content")
layout = QtWidget.QVBoxLayout(content)
window = QtWidget.QWidget()
window.setProperty("class", "content")

app.setStyleSheet("""
[class="content"] {
    background-color: #202020;
}

QPushButton {
    background-color: #61CCFF;
    color: #000000;
    border-radius: 4px;
    padding: 12px 16px;
    margin-bottom: 2px;
    text-align: left;
}
QPushButton:hover {
    background-color: #5CBCEA;
}
QPushButton:pressed {
    background-color: #57ADD6;
    color: #2B566B;
}
[class="frame"] {
    background-color: #2B2B2B;
    padding: 24px 32px;
    border-radius: 8px;
}
QLineEdit, QPlainTextEdit {
    background-color: #272727;
    margin-top: 2px;
    padding-left: 12px;
    color: #ffffff;
                  
}
QPlainTextEdit {
    padding: 12px;
}
[class*="canEdit"] {
    background-color: #373737;
}
[class*="btmMr"] {
    margin-top: 0;
    margin-bottom: 2px;}
[class="topMr"] {
    margin-top: 2px;
    margin-bottom: 0;
}
""")

######################################

getIp = QtWidget.QWidget()
getIp.setProperty("class", "frame")
getIp.setSizePolicy(
    QtWidget.QSizePolicy.Policy.Preferred,
    QtWidget.QSizePolicy.Policy.Fixed
)
getIpLayout = QtWidget.QVBoxLayout(getIp)
getIpLayout.setSpacing(5)

AutoIpValue = QtWidget.QLineEdit()
AutoIpValue.setProperty("class", "canEdit btmMr")
AutoIpValue.setCursor(Qt.CursorShape.IBeamCursor)
AutoIpValue.textChanged.connect(changeNAN)
AutoIpValue.setText(NetworkAdpater)
AutoIpValue.setPlaceholderText("Input Network Adapter (optional)")
getIpLayout.addWidget(AutoIpValue)

getIpInput = QtWidget.QPushButton()
getIpInput.setText("Get IP for Network Adpater (ifconfig standard)")
getIpInput.setProperty("class", "topMr")
getIpInput.setCursor(Qt.CursorShape.PointingHandCursor)
getIpInput.clicked.connect(get_ip)
getIpLayout.addWidget(getIpInput)

AutoIpValue.setFixedHeight(getIpInput.sizeHint().height())

getIpOutput = QtWidget.QLineEdit()
getIpOutput.setProperty("class", "canEdit")
getIpOutput.setFixedHeight(getIpInput.sizeHint().height())
getIpOutput.setCursor(Qt.CursorShape.IBeamCursor)
getIpOutput.setPlaceholderText("Input IP")
getIpLayout.addWidget(getIpOutput)

layout.addWidget(getIp)

######################################

getVideo = QtWidget.QWidget()
getVideo.setProperty("class", "frame")
getVideo.setSizePolicy(
    QtWidget.QSizePolicy.Policy.Preferred,
    QtWidget.QSizePolicy.Policy.Fixed
)
getVideoLayout = QtWidget.QVBoxLayout(getVideo)
getVideoLayout.setSpacing(5)


getVideoLink = QtWidget.QLineEdit()
getVideoLink.setProperty("class", "canEdit")
getVideoLink.setFixedHeight(getIpInput.sizeHint().height())
getVideoLink.setCursor(Qt.CursorShape.IBeamCursor)
getVideoLink.setPlaceholderText("Input remote server folder path...")
getVideoLink.setText(oriDirectory)
getVideoLink.textChanged.connect(changeDir)
getVideoLayout.addWidget(getVideoLink)

getVideoPassword = QtWidget.QLineEdit()
getVideoPassword.setProperty("class", "canEdit")
getVideoPassword.setEchoMode(QtWidget.QLineEdit.EchoMode.Password)
getVideoPassword.setFixedHeight(getIpInput.sizeHint().height())
getVideoPassword.setCursor(Qt.CursorShape.IBeamCursor)
getVideoPassword.setPlaceholderText("Input SSH Password")
getVideoPassword.setText(passwd)
getVideoPassword.textChanged.connect(changePasswd)
getVideoLayout.addWidget(getVideoPassword)

getVideoInput = QtWidget.QPushButton()
getVideoInput.setText("Load file list")
getVideoInput.setCursor(Qt.CursorShape.PointingHandCursor)
getVideoInput.clicked.connect(get_video)
getVideoLayout.addWidget(getVideoInput)

getVideoOutput = QtWidget.QPlainTextEdit()
getVideoOutput.setReadOnly(True)
getVideoOutput.setFixedHeight(getIpInput.sizeHint().height() * 5)
getVideoLayout.addWidget(getVideoOutput)

layout.addWidget(getVideo)

######################################

getDownload = QtWidget.QWidget()
getDownload.setProperty("class", "frame")
getDownload.setSizePolicy(
    QtWidget.QSizePolicy.Policy.Preferred,
    QtWidget.QSizePolicy.Policy.Fixed
)
getDownloadLayout = QtWidget.QVBoxLayout(getDownload)
getDownloadLayout.setSpacing(5)

getDownloadCode = QtWidget.QLineEdit()
getDownloadCode.setFixedHeight(getIpInput.sizeHint().height())
getDownloadCode.setPlaceholderText("Input file name to download...")
getDownloadCode.setProperty("class", "canEdit btmMr")
getDownloadLayout.addWidget(getDownloadCode)

getDownloadFolder = QtWidget.QLineEdit()
getDownloadFolder.setFixedHeight(getIpInput.sizeHint().height())
getDownloadFolder.setPlaceholderText("Input download location or file name...")
getDownloadFolder.setText(downloadDirectory)
getDownloadFolder.setProperty("class", "canEdit btmMr")
getDownloadFolder.textChanged.connect(input_download_folder)
getDownloadLayout.addWidget(getDownloadFolder)

getDownloadInput = QtWidget.QPushButton()
getDownloadInput.setText("File Download")
getDownloadInput.setCursor(Qt.CursorShape.PointingHandCursor)
getDownloadInput.clicked.connect(get_download)
getDownloadInput.setProperty("class", "topMr")
getDownloadLayout.addWidget(getDownloadInput)

layout.addWidget(getDownload)

######################################

openFolder = QtWidget.QWidget()
openFolder.setProperty("class", "frame")
openFolder.setSizePolicy(
    QtWidget.QSizePolicy.Policy.Preferred,
    QtWidget.QSizePolicy.Policy.Fixed
)
openFolderLayout = QtWidget.QVBoxLayout(openFolder)
openFolderLayout.setSpacing(5)

openFolderInput = QtWidget.QPushButton()
openFolderInput.setText("Open Download Folder (injection warning)")
openFolderInput.setCursor(Qt.CursorShape.PointingHandCursor)
openFolderInput.clicked.connect(open_download_folder)
openFolderLayout.addWidget(openFolderInput)


layout.addWidget(openFolder)

######################################

scroll = QtWidget.QScrollArea()
scroll.setWidgetResizable(True)
scroll.setFrameShape(QtWidget.QFrame.Shape.NoFrame)
scroll.setWidget(content)
content.setSizePolicy(
    QtWidget.QSizePolicy.Policy.Expanding,
    QtWidget.QSizePolicy.Policy.Expanding
)

layout.addStretch()
main_layout = QtWidget.QVBoxLayout(window)
main_layout.addWidget(scroll)
window.resize(700, 800)
window.setWindowTitle("file import script V1")
window.show()

app.exec()