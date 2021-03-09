import PySimpleGUI as gui

import cv2

def video2Image(movie_path:str, image_path)->bool:
    cap = cv2.VideoCapture(movie_path)

    if cap.isOpened() != True:
        #Noting Moive
        return False
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #print("count:{}, fps:{}, the number of image:{}".format(count,fps, int(count)/fps))
    
    for num in range(1, count, fps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, num)
        pic_no = int((num-1)/fps)
        cv2.imwrite('{}\picture{:0=3}.jpg'.format(image_path ,pic_no), cap.read()[1])
        #print('save picture{:0=3}.jpg'.format(pic_no))
    cap.release()
    return True

gui.theme('DarkAmber')

layout = [
    [gui.Text('動画を約1秒ごとの複数の画像に変換します!')],
    [gui.Text('以下に動画のパスを指定してください')],
    [gui.InputText(key='movie'), gui.FileBrowse('動画を選択',key='movie')],
    [gui.Text('以下に画像の保存先ディレクトリを指定してください')],
    [gui.InputText(key='image'), gui.FolderBrowse('保存先を選択',key='image')],
    [gui.Button('変換')]
]
window = gui.Window('Movie2Image', layout)
#event loop
while True:
    event, value = window.read()
    if event == gui.WIN_CLOSED:
        break
    elif event == '変換':
        success = video2Image(value['movie'],value['image'])
        popup_text = '変換処理が終了しました' if success else '動画が正常に読み込めていません'
        gui.popup(popup_text)

window.close()

