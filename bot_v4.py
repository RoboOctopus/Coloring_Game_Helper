import cv2
import numpy as np
import pyautogui
import time
import keyboard
import os
import mouse



dir_path = os.path.dirname(os.path.realpath(__file__))

const = 10 # alle Center coordinates are 20 pixels appart

#area = (147,62,1682,1324)

color = (0,0,1000,500)


#clicks left on the coodinate tuple given
def l_click(xy):
    x, y = xy
    mouse.move(x, y, absolute= True)
    mouse.click(button='left')
    time.sleep(0.01)

#clicks right on the coodinate tuple given
def r_click(xy):
    x, y = xy
    mouse.move(x, y, absolute= True)
    mouse.click(button='right')
    time.sleep(0.01)


#checks stuff 
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
def looker(start_list: list, size_x, size_y)-> list:
    return_list = []
    while len(start_list) != 0:
        #initializes an array set to zero

        void_left, void_top = start_list[0]
        coords = np.zeros((void_left + size_x,void_top + size_y))
        #coords = np.zeros((168, 132))

        #puts a 1 in the 2d array for the coordinates in a liste

              
        for i in range(len(start_list)):
            #print(start_list[i])
            x_,y_ = start_list[i]
            #print(coords[x_ ,y_ ])
            coords[x_,y_] = 1
            #print(coords[x_ ,y_ ])

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
        for _y_ in range(size_y+ void_top):
            for _x_ in range(size_x+ void_left):
                if coords[_x_,_y_] == 2:
                    #temp_r.append((_x_ * const + 147 +5 ,_y_ * const + 63 + 5))
                    temp_r.append((_x_ ,_y_ ))

   
        

        xx ,yy = temp_r[0]
        return_list.append((xx * const + 100 +5 ,yy * const + 62 + 5))

        for i in range(len(temp_r)):
            start_list.remove(temp_r[i])

        
    #print(return_list)
    return return_list

#gets the width and height
def size(liste:list,area)-> tuple:
    #looks for the biggest x and sub smollest x and the same for y. dont know how to make is smaller :/
    temp = min(liste,key=lambda tup: tup[0])
    min_x = temp[0]
    temp = max(liste,key=lambda tup: tup[0])
    max_x = temp[0]
    temp = min(liste,key=lambda tup: tup[1])
    min_y = temp[1]
    temp = max(liste,key=lambda tup: tup[1])
    max_y = temp[1]
    len_x,len_y=  max_x- min_x +1,max_y - min_y +1

    return((len_x,len_y))


def bot(dir_path, res_x,res_y):
    start = 0
    finish = 0
    start = time.perf_counter()
    Ö = 0

    

    area = (100,62,res_x-100, res_y-62)
    #area = (147,62,2560-147,1440-62)

    #gets the area of the curren color
    checkmark = pyautogui.locateCenterOnScreen((f'{dir_path}\images\checkmark.png'),region=(color),confidence= 0.95)
    color_x, color_y = checkmark
    color_area = (color_x+15, color_y -15, 35, 35)
    pyautogui.screenshot(region=(color_area)).save(f'{dir_path}\images\current_color.png')

    current_color = f'{dir_path}\images\current_color.png'

    check_colorchange = pyautogui.locateCenterOnScreen(current_color,region=(color), confidence= 0.99)


    #main loop of the script
    while keyboard.is_pressed('v') == False and Ö == 0:
        clicks = []
        pyautogui.screenshot(region=(area)).save(f'{dir_path}\images\savedimage.png')

        game_img = cv2.imread(f'{dir_path}/images/savedimage.png' , cv2.IMREAD_UNCHANGED)
        green_img = cv2.imread(f'{dir_path}/images/green.png' , cv2.IMREAD_UNCHANGED)
        
        green = f'{dir_path}\images\green.png'
        grey = f'{dir_path}\images\grey.png'

        result = cv2.matchTemplate(game_img, green_img, cv2.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.99

        yloc, xloc = np.where(result >= threshold)
        x, y = max_loc

        #list of block coordiantes that contains a block that has yet to be clicked
        liste_green = []
        for (x,y) in zip(xloc, yloc):
            liste_green.append((round((x/const)),round(y/const)))


        game_img = cv2.imread(f'{dir_path}/images/savedimage.png' , cv2.IMREAD_UNCHANGED)
        green_img = cv2.imread(f'{dir_path}/images/grey.png' , cv2.IMREAD_UNCHANGED)

        result = cv2.matchTemplate(game_img, green_img, cv2.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.99

        yloc, xloc = np.where(result >= threshold)
        x, y = max_loc

        liste_grey = []
        for (x,y) in zip(xloc, yloc):
            liste_grey.append((round(x/const),round(y/const)))

        liste_all = liste_grey + liste_green
        liste_all.sort(key=lambda tup: tup[0])
        liste_all.sort(key=lambda tup: tup[1])


        #c_start = time.perf_counter()
        size_x, size_y =size(liste_all, area)


        #calls looker function 
        clicks = looker(liste_green,size_x, size_y)


        #refreshes current_color
        pyautogui.screenshot(region=(color_area)).save(f'{dir_path}\images\current_color.png')


        #clicks all coordiantes in list "clicks"
        for num in range(len(clicks)):
            l_click(clicks[num])
            if keyboard.is_pressed('v') == True:
                finish = time.perf_counter()
                return {round(finish-start,2)}
        

        check_colorchange = pyautogui.locateCenterOnScreen(current_color,region=(color), confidence= 0.99)
        locate_green = pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.90)

        #waiting for the game to update
        while locate_green != None and check_colorchange != None:
            check_colorchange = pyautogui.locateCenterOnScreen(current_color,region=(color_area), confidence= 0.99)
            locate_green = pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.99)
            #exit
            if keyboard.is_pressed('v') == True:
                finish = time.perf_counter()
                return {round(finish-start,2)}
            pass

        #refreshes current_color
        pyautogui.screenshot(region=(color_area)).save(f'{dir_path}\images\current_color.png')


        #finds a grey box and clicks it
        locate_grey = pyautogui.locateCenterOnScreen(grey,region=(area),confidence= 0.99)
        if locate_grey  != None and check_colorchange != None:
            r_click(locate_grey)
            while pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.99) == None and pyautogui.locateCenterOnScreen(grey,region=(area),confidence= 0.99) != None:
                pass


        locate_green = pyautogui.locateCenterOnScreen(green,region=(area), confidence= 0.99)        
        #if no grey boxes are found it will exit the loop
        if  locate_grey == None and locate_green == None:
            Ö =  Ö + 1


    finish = time.perf_counter()
    

    return {round(finish-start,2)}
