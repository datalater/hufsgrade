# default_size

full_size = [660, 500]

label_size          = [200, 20, 90, 20]
lineEdit_size       = [300, 20, 150, 20]
label_2_size        = [200, 50, 90, 20]
lineEdit_2_size     = [300, 50, 150, 20]
pushButton_size     = [200, 80, 250, 28]
progress_size       = [430, 475, 220, 20]
pushButton_2_size   = [552, 440, 80, 28]
label_3_size        = [10, 10, 280, 20]
label_5_size        = [370, 10, 280, 20]
line_size           = [0, 95, 660, 60]
line_2_size         = [0, 25, 660, 20]
label_6_size        = [20, 65, 240, 20]
label_7_size        = [535, 65, 120, 20]
label_4_size        = [5, 475, 500, 20]
tableWidget_size    = [20, 90, 615, 130]

widget_size_list = [label_size, lineEdit_size, label_2_size, lineEdit_2_size, pushButton_size, progress_size, pushButton_2_size, label_3_size, label_5_size, line_size, line_2_size, label_6_size, label_7_size, label_4_size, tableWidget_size]

# size auto
size_plus = [0, 20]

full_size[0] = full_size[0] + size_plus[0]
full_size[1] = full_size[1] + size_plus[1]

for widget_size in widget_size_list:
    widget_size[2] = widget_size[2] + size_plus[0]
    widget_size[3] = widget_size[3] + size_plus[1]

label_size          = widget_size_list[0]
lineEdit_size       = widget_size_list[1]
label_2_size        = widget_size_list[2]
lineEdit_2_size     = widget_size_list[3]
pushButton_size     = widget_size_list[4]
progress_size       = widget_size_list[5]
pushButton_2_size   = widget_size_list[6]
label_3_size        = widget_size_list[7]
label_5_size        = widget_size_list[8]
line_size           = widget_size_list[9]
line_2_size         = widget_size_list[10]
label_6_size        = widget_size_list[11]
label_7_size        = widget_size_list[12]
label_4_size        = widget_size_list[13]
tableWidget_size    = widget_size_list[14]



print(label_size[0], label_size[1], label_size[2], label_size[3])

#self.label.setGeometry(200, 20, 90, 20)
#self.widget.setGeometry(widget_size)
