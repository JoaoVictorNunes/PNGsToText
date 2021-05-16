import os
import pytesseract
import cv2
import PySimpleGUI as gui
import imageio as io
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
gui.theme('DarkTeal9')

def list_all_png(path):
    png_filenames = []
    for filepath in path:
        ini = filepath.rfind('/')
        nome = filepath[ini+1:]
        if ".png" in nome or ".PNG" in nome:
            png_filenames.append(filepath)
    return png_filenames


def image_to_text(filepath):
    img = io.imread(filepath)
    string = pytesseract.image_to_string(img, lang="por+eng")
    string = string.replace('\n', ' ')
    if string[0] == "-":
        string = ">" + string[1:]
    return string_slicer(string)


def string_slicer(string):
    atom = 250
    parts = 1 + int(len(string)/atom)
    sliced = ""
    for i in range(parts):
        if i == parts:
            sliced = string[(1+i)*atom:]
            break
        sliced += string[i*atom: (i+1) * atom] + '\t'
    return sliced


def main_function(paths_list):
    window['-STATUS-'].update(value='Lendo arquivos...')
    path_list = list_all_png(paths_list)
    file = open("CRFs - Razão da Mudança.txt", 'w')
    file2 = open("CRFs - Títulos.txt", 'w')
    for path in path_list:
        text = image_to_text(path)
        nome = path[path.rfind('/')+1:]

        if 't' in nome:
            file2.write('\n' + nome[:-5] + "\t" + "CRF - " + text[:-2].upper())
            
        else:
            file.write('\n' + nome[:-4] + "\t" + text[:-2])

    file.close()
    file2.close()

    window['-STATUS-'].update(value='Finalizado!')


layout = [[gui.FilesBrowse("Selecionar arquivos", key="Browse", size=(15,1))],
          [gui.Button('Ler arquivos', key='-LER-', size=(15,1)) ],
          [gui.Text('Selecione os arquivos e clique para lê-los', size=(40, 1), key='-STATUS-')]]

window = gui.Window('Converter para texto', layout, force_toplevel=True, size=(400,150))

while True:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        break
    elif event == '-LER-':
        paths = values['Browse'].split(';')

        if paths[0] == '':
            window['-STATUS-'].update(value='Selecione os arquivos!')
        else:
            main_function(paths)

window.close()
