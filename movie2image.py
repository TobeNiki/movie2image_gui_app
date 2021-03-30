import PySimpleGUI as gui
import os
import cv2

def video2Image(movie_path:str, image_path:str)->bool:
    cap = cv2.VideoCapture(movie_path)

    if cap.isOpened() != True:
        #Noting Moive
        return False
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    #１秒ごとに動画から画像を切り出す処理
    for num in range(1, count, fps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, num)
        pic_no = int((num-1)/fps)
        cv2.imwrite('{}\picture{:0=3}.jpg'.format(image_path ,pic_no), cap.read()[1])
        
    cap.release()
    return True

#レイアウトの定義
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
        #画面が閉じるとうの終了処理
        break
    elif event == '変換':
        #保存フォルダ作成(既存のものがある場合はパス)
        saveFolder = '{}/m2p_save'.format(value['image'])
        if not os.path.exists(saveFolder):
            os.mkdir(saveFolder)
        #変換を実行する処理
        success = video2Image(value['movie'],saveFolder)
        #変換処理の結果(bool値)に応じてメッセージを表示
        popup_text = '変換処理が終了しました' if success else '動画が正常に読み込めていません'
        gui.popup(popup_text)

window.close()