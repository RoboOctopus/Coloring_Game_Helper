import cv2 
import numpy as np
import pyautogui
import time
import keyboard
import mouse

const = 10 # alle Center coordinates are 20 pixels appart (only in 1440p) 

area = (147,63,1682,1322)

done_area = (60,36,56,56)


def l_click(xy):
    x, y = xy
    mouse.move(x, y, absolute= True)
    mouse.click(button='left')
    time.sleep(0.01)


def r_click(xy):
    x, y = xy
    mouse.move(x, y, absolute= True)
    mouse.click(button='right')
    time.sleep(0.01)




def isValid(screen, m, n, x, y, prevC, newC):
    if x<0 or x>= m\
       or y<0 or y>= n or\
       screen[x][y]!= prevC\
       or screen[x][y]== newC:
        return False
    return True

# FloodFill function
def floodFill(screen, m, n, x, y, prevC, newC):
    queue = []
     
    # Append the position of starting
    # pixel of the component
    queue.append([x, y])
 
    # Color the pixel with the new color
    screen[x][y] = newC
 
    # While the queue is not empty i.e. the
    # whole component having prevC color
    # is not colored with newC color
    while queue:
         
        # Dequeue the front node
        currPixel = queue.pop()
         
        posX = currPixel[0]
        posY = currPixel[1]
         
        # Check if the adjacent
        # pixels are valid
        if isValid(screen, m, n, 
                posX + 1, posY, 
                        prevC, newC):
             
            # Color with newC
            # if valid and enqueue
            screen[posX + 1][posY] = newC
            queue.append([posX + 1, posY])
         
        if isValid(screen, m, n, 
                    posX-1, posY, 
                        prevC, newC):
            screen[posX-1][posY]= newC
            queue.append([posX-1, posY])
         
        if isValid(screen, m, n, 
                posX, posY + 1, 
                        prevC, newC):
            screen[posX][posY + 1]= newC
            queue.append([posX, posY + 1])

        if isValid(screen, m, n, 
                    posX, posY-1, 
                        prevC, newC):
            screen[posX][posY-1]= newC
            queue.append([posX, posY-1])

# look for big groups of boxes and returns the first coordinate of a group
def looker(start_list: list)-> list:  
    return_list = []
    
    while len(start_list) != 0:
    #for _ in range(1):
        #initializes an array with the width of 167 and height if 131 all set to zero
        coords = np.zeros((168, 132))

        #puts a 1 in the 2d array for the coordinates in a liste
        for i in range(len(start_list)):
            x_,y_ = start_list[i]
            coords[x_ ,y_ ] = 1

        # Co-ordinate provided by the user
        _x, _y = start_list[0]

        # Row of the display
        m = len(coords)

        # Column of the display
        n = len(coords[0])

        # Current color at that co-ordinate
        prevC = coords[_x][_y]

        # New color that has to be filled
        newC = 2

        floodFill(coords, m, n, _x, _y, prevC, newC)

        #now we create a new list "temp_r" and remove all filled coordinates from the original list
        temp_r =[]
        for _y_ in range(132):
            for _x_ in range(168):
                if coords[_x_,_y_] == 2:
                    #temp_r.append((_x_ * const + 147 +5 ,_y_ * const + 63 + 5))
                    temp_r.append((_x_ ,_y_ ))
        #print(temp_r)
        xx ,yy = temp_r[0]
        return_list.append((xx * const + 147 +5 ,yy * const + 63 + 5))

        for i in range(len(temp_r)):
            start_list.remove(temp_r[i])


    return return_list


def bot(dir_path):
    start = 0
    finish = 0
    start = time.perf_counter()
    Ö = 0

    while keyboard.is_pressed('v') == False and Ö == 0:
        clicks = []
        pyautogui.screenshot(region=(area)).save(f'{dir_path}\images\savedimage.png')

        game_img = cv2.imread(f'{dir_path}/images/savedimage.png' , cv2.IMREAD_UNCHANGED)
        green_img = cv2.imread(f'{dir_path}/images/green.png' , cv2.IMREAD_UNCHANGED)
        
        green = f'{dir_path}\images\green.png'
        grey = f'{dir_path}\images\grey.png'
        # i dont know what is happening here
        a = 'area.png'
        done_area_pic =  f'{dir_path}\images\{a}'


        result = cv2.matchTemplate(game_img, green_img, cv2.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #print(max_val ,max_loc)
        threshold = 0.99

        yloc, xloc = np.where(result >= threshold)
        #print(len(xloc),len(xloc))
        x, y = max_loc

        #list of block coordiantes that contains a block that has yet to be clicked
        liste = []
        for (x,y) in zip(xloc, yloc):
            #real_liste.append((x + 147 +5,y + 63 + 5))
            liste.append((round(x/const),round(y/const)))

        c_start = time.perf_counter()

        #calls lokker function 
        clicks = looker(liste)

        math_finish = time.perf_counter()
        #print(f'math: {round(math_finish-c_start,2)} s')

        #clicks all coordiantes in list "clicks"
        for num in range(len(clicks)):
            l_click(clicks[num])

        #Scanns the screen area for matches and clicks them
        color_finished = pyautogui.locateCenterOnScreen(done_area_pic,region=(done_area), confidence= 0.3)
        locate_green = pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.99)
        time.sleep(0.001)
        while keyboard.is_pressed('c') == False and locate_green != None and color_finished == None:
            color_finished = pyautogui.locateCenterOnScreen(done_area_pic,region=(done_area), confidence= 0.05)
            locate_green = pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.99)    
            if locate_green and color_finished == None:
                l_click(locate_green)
                #print(color_finished)

        #finds a grey box and clicks it
        locate_grey = pyautogui.locateCenterOnScreen(grey,region=(area),confidence= 0.99)
        if locate_grey  != None and locate_green == None:
            r_click(locate_grey)

            while pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.99) == None and pyautogui.locateCenterOnScreen(grey,region=(area),confidence= 0.99) != None:
                pass

        #if no grey boxes are found it will exit the loop
        if  locate_grey == None and color_finished == None and locate_green == None:
            Ö =  Ö + 1


    finish = time.perf_counter()
    

    return {round(finish-start,2)}
