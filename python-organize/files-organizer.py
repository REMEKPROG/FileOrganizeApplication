import os
import shutil
import pathlib
import datetime
import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.simpledialog import askstring

#creating root(window) for aplication
root = Tk()
img = None
root.title('Files Organizer Program - FOP')
root.geometry('1000x500')
root.config(background='light gray')

#global dict to remove buttons between functions
Plik = {}
activeButtons = {}

#init function - making widget for application
def initFunction():
    file = open('log.log', 'a')
    file.close()

    ProgramMainTitle = Label(root, text = "File Organizer")
    ProgramMainTitle.config(font='Arial, 25', padx=10, pady=10, fg='red')
    ProgramMainTitle.pack(expand=False, fill=BOTH, side=TOP)

    directoryButton = Button(root, text='Wybierz Folder', command=openDirectory)
    directoryButton.config(font='Arial, 15', padx=10, pady=10)
    directoryButton.pack(expand=False, side=BOTTOM, fill=X)

    logLabel = Label(root, text='Kliknij tutaj aby \n wyświetlić pliki zmian')
    logLabel.config(font='Arial, 10')
    logLabel.pack(side=LEFT,ipadx=5, ipady=5)

    logFileBtn = Button(root, text='LOG', command=openLogFile)
    logFileBtn.config(font='Arial, 10')
    logFileBtn.pack(side=LEFT, ipadx=5, ipady=5)
    activeButtons['directoryBtn'] = directoryButton

#function to open log file from button
def openLogFile():
    logFile = os.startfile('log.log')

#function to creating widgets for starting main function
def openDirectory():
    try:
        elements = [activeButtons['folder'], activeButtons['actionBtn']]
        for label in elements:
            if not label == None:
                label.destroy()
    except KeyError:
        print('error')

    #opening directory to organize
    try:
        folderName = filedialog.askdirectory()
        if folderName == '':
            return
        Plik['folderName'] = folderName
    except:
        messageBox = messagebox.showerror(title='Error', message='Nie udało się otworzyć pliku! Sprawdź swoje uprawnienia!')
    folderLabel = Label(root, text=f'Wybrany folder:{folderName}')
    folderLabel.config(font='Arial, 10', padx=5, pady= 5, fg='red')
    folderLabel.pack(expand=True)

    actionButton = Button(root, text=f'Kliknij aby rozpocząć organizować', command=organizeFiles)
    actionButton.config(font='Arial, 15', padx=10, pady=10)
    actionButton.pack(expand=False, fill=X, side=BOTTOM)

    activeButtons['folder'] = folderLabel
    activeButtons['actionBtn'] = actionButton

initFunction()

#function to make new file if file is already exists(new file name), 
def makeNewFile(File, Path):
    fileName, fileExtension = os.path.splitext(File)
    regex = '[0-9]'
    newFileName = File
    i = 1
    while os.path.exists(os.path.join(Path, newFileName)):
        i += 1
        newFileName = re.split(regex,fileName)[0] + str(i) + fileExtension
    return newFileName

#function to create necessary widgets for validating file, program is saving file with new name or removing it from system
def ValidateFile(File, filePath):
    wybor_var = StringVar()

    def HandleChoice(event):
        wybor_var.set(choiceLabel.get())

    choiceLabel = Entry(root, width=50)
    choiceLabel.pack(expand=False, side=BOTTOM)

    fileProblemLabel = Label(root, text=f'plik {File} Już istnieje. Co chcesz z nim zrobić? \n 1.Usuń \n 2.Zapisz z automatyczną nazwą')
    fileProblemLabel.config(font='Arial, 10', pady=10)
    fileProblemLabel.pack(expand=False, side=BOTTOM, fill=X)

    choiceLabel.bind('<Return>', HandleChoice)
    choiceLabel.focus_set()

    activeButtons['fileProblem'] = fileProblemLabel
    activeButtons['choice'] = choiceLabel

    #a part when program is waiting for user input, its based on wait_variable method which waiting when variable will change
    root.wait_variable(wybor_var)
    wybor = int(wybor_var.get())

    choiceLabel.destroy()
    fileProblemLabel.destroy()
    
    #making choice and saving information to log file
    if wybor == 1:
        os.remove(os.path.join(filePath, File))
        try:
            with open ('log.log', 'a', encoding='utf-8') as log:
                logMessage = rf'Plik {File} został usunięty z {filePath}'
                currentDate = datetime.datetime.now()
                log.write(str(currentDate.strftime('%Y') + '-' + currentDate.strftime('%m') + '-' + currentDate.strftime('%d') + ' ' + currentDate.strftime('%X')) + ' - ' + logMessage + '\n')
        except:
            print('Nastąpił błąd związany z otwarciem pliku!')
        return True
    elif wybor == 2:
        return False
    
#list for collecting needed subfolders basing on which file is organizing now
subfolders = []

#function that moves filles to special subfolders basing on their extensions
def moveFileToDirectory(currentPath, DestinationPath, originalFile):
    folder = os.path.dirname(DestinationPath)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    #making subfolders
    for subfolder in subfolders:
        subFolderPath = os.path.join(folder, subfolder)
        if not os.path.exists(subFolderPath):
            os.makedirs(subFolderPath)

    #checking if file already exists
    if os.path.exists(os.path.join(DestinationPath, originalFile)):
        if ValidateFile(originalFile, currentPath):
            return
        File = makeNewFile(originalFile, DestinationPath)
    else:
        File = originalFile

    #moving file
    fileCurrentPath = os.path.join(currentPath, originalFile)
    fileDestinationPath = os.path.join(DestinationPath, File)
    shutil.move(fileCurrentPath, fileDestinationPath)
    return rf'Plik: {File}, został przeniesiony z {fileCurrentPath} do {fileDestinationPath}' + '\n'


#this function is main function that active others function
def organizeFiles():
    #disable button to avoid bugs
    activeButtons['actionBtn']['state'] = 'disabled'

    #checking if folder is empty or not
    path = Plik['folderName']
    while len(os.listdir(path)) == 0:
        allert = messagebox.askretrycancel(title='Ostrzeżenie', message='Twój folder jest pusty, co uniemożliwia segregację!')
        if not allert:
            return
    
    #warn user before organize
    listOfFiles = os.listdir(path)
    alertBox = messagebox.askyesno(title='Ostrzeżenie', message='Proces segregacji folderu jest nieodrwacalny, czy chcesz wykonać?')
    if not alertBox:
        activeButtons['actionBtn']['state'] = 'normal'
        return
    
    #its main part of function, there files are being checked and moving, then information about file is saved in log file
    with open('log.log', 'a', encoding='utf-8') as log:
        for plik in listOfFiles:
            if os.path.isdir(os.path.join(path, plik)):
                continue
            else:
                if plik.lower().endswith('.txt'):
                    subfolders.append('dokumenty')
                    logMessage = moveFileToDirectory(path , rf'{path}\dokumenty', plik)
                elif plik.lower().endswith(('.png', '.jpg', '.jpeg')):
                    subfolders.append('obrazy')
                    logMessage = moveFileToDirectory(path , rf'{path}\obrazy', plik)
                elif plik.lower().endswith(('.mp3', '.mp4')):
                    subfolders.append('muzyka')
                    logMessage = moveFileToDirectory(path , rf'{path}\muzyka', plik)
            try:
                currentDate = datetime.datetime.now()
                log.write(str(currentDate.strftime('%Y') + '-' + currentDate.strftime('%m') + '-' + currentDate.strftime('%d') + ' ' + currentDate.strftime('%X')) + ' - ' + logMessage)
            except:
                print(f'Nie udało się zapisac do logów!, plik {plik} został usunięty')
    for element in activeButtons.values():
        if element == activeButtons['directoryBtn']:
            continue
        element.destroy()
root.mainloop()