import keyboard
x_co = float(0.0)
y_co = float(0.0)
z_co = float(0.5)
while True:
    if keyboard.is_pressed('up'):
        print("loop broken")
        break
    elif keyboard.is_pressed('space'):
        x_co = float(input("enter new x coordinate"))
        y_co = float(input("enter new y coordinate"))
        z_co = float(input("enter new z coordinate"))
    else:
        print(x_co)
        print(y_co)
        print(z_co)

