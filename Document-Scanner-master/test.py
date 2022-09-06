import os
import tkinter.filedialog as fd
# создаем объект этого класса, применяем метод .upload()
def fil():
    filetypes = (("Изображение", "*.jpg *.gif *.png"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                  filetypes=filetypes)
    if filename:
        return filename.split('/')[-1]

#запускаем оббученную YOLO4 для оределения границ областей

put='photo/'+'10007.jpg'#fil()
out = 'test.txt'
os.system(f'./darknet detector test data/obj.data cfg/yolov4-obj.cfg yolov4-obj_last.weights {put} -thresh 0.5 -ext_output -dont_show -out result.txt > {out}')
# oblasty(out,put) #запускаем вырезание областей с последующим распознанием