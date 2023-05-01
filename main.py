import pygame
import os
from process import process

pygame.display.set_caption("State Processing Simulation")
pygame.font.init()

# Program Constants
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
MAX_PROCESSES = 8
MAX_TIME = 50
INIT, READY, RUNNING, BLOCKED, DONE, ADMIT = 'Uninitialized', 'Ready', 'Running', 'Blocked', 'Done', 'Arrived'
TIMER_FONT = pygame.font.SysFont("Arial", 30, 1)
SUBHEADING_FONT = pygame.font.SysFont("Arial", 20, 1)
TEXT_FONT = pygame.font.SysFont("Arial", 13)
BUTTON_ONE_POS = (10, 10)
BUTTON_TWO_POS = (120, 10)
RUN_BUTTON_POS = (300, 10)
TEXTBOX_POS = (190, 130)
TOP_PROCESS_POS = (10, 100)
BOTTOM_PROCESS_POS = (10, 300)
PROCESS_OFFSET = 180

# Images
BUTTON_IMAGE = pygame.image.load(os.path.join("Images" ,"Button.png"))
SMALL_BUTTON_IMAGE = pygame.image.load(os.path.join("Images" ,"Small_Button.png"))
CPU_IMAGE = pygame.image.load(os.path.join("Images", "CPU_Pos.png"))
PROCESS_BLOCKED_IMAGE = pygame.image.load(os.path.join("Images", "Process_Blocked.png"))
PROCESS_DONE_IMAGE = pygame.image.load(os.path.join("Images", "Process_Done.png"))
PROCESS_INIT_IMAGE = pygame.image.load(os.path.join("Images", "Process_Init.png"))
PROCESS_READY_IMAGE = pygame.image.load(os.path.join("Images", "Process_Ready.png"))
PROCESS_RUNNING_IMAGE = pygame.image.load(os.path.join("Images", "Process_Running.png"))
TEXTBOX_IMAGE = pygame.image.load(os.path.join("Images", "Textbox.png"))
INCREMENT_BUTTON_IMAGE = pygame.image.load(os.path.join("Images", "Increment_Button.png"))
DECREMENT_BUTTON_IMAGE = pygame.image.load(os.path.join("Images", "Decrement_Button.png"))

# Sprites
BUTTON = pygame.transform.scale(BUTTON_IMAGE, (81, 51))
SMALL_BUTTON = pygame.transform.scale(SMALL_BUTTON_IMAGE, (51, 31))
CPU = pygame.transform.scale(CPU_IMAGE, (81, 61))
PROCESS_BLOCKED = pygame.transform.scale(PROCESS_BLOCKED_IMAGE, (121, 61))
PROCESS_DONE = pygame.transform.scale(PROCESS_DONE_IMAGE, (121, 61))
PROCESS_INIT = pygame.transform.scale(PROCESS_INIT_IMAGE, (121, 61))
PROCESS_READY = pygame.transform.scale(PROCESS_READY_IMAGE, (121, 61))
PROCESS_RUNNING = pygame.transform.scale(PROCESS_RUNNING_IMAGE, (121, 61))
TEXTBOX = pygame.transform.scale(TEXTBOX_IMAGE, (301, 251))
INCREMENT_BUTTON = pygame.transform.scale(INCREMENT_BUTTON_IMAGE, (31, 36))
DECREMENT_BUTTON = pygame.transform.scale(DECREMENT_BUTTON_IMAGE, (31, 36))

# Global Variables
processes = [0] * MAX_PROCESSES
currentNumProcesses = 4
simulating = False
currentTime = 0
processSettings = -1
readyList = []
admitList = []
interruptList = []
runningNum = -1
cpuNum = -1

# Main function
def main():
    run = True
    clock = pygame.time.Clock()
    create_process()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked()
        draw_window()
    
    pygame.quit()

# Draw images on the window
def draw_window():
    WIN.fill(WHITE)
    WIN.blit(BUTTON, BUTTON_ONE_POS)
    if simulating == False:
        WIN.blit(BUTTON, BUTTON_TWO_POS)
        WIN.blit(BUTTON, RUN_BUTTON_POS)
        draw_processes()
        draw_menu_text()
        draw_settings()
    else:
        global runningNum, cpuNum
        draw_processes()
        draw_sim_text()
        if not cpuNum == -1:
            draw_cpu(cpuNum)
    pygame.display.update()

# Draw text on the window
def draw_menu_text():
    # Button 1 Text
    topText = TEXT_FONT.render("Add", 1, BLACK)
    bottomText = TEXT_FONT.render("Process", 1, BLACK)
    WIN.blit(topText, (BUTTON_ONE_POS[0] + 28, BUTTON_ONE_POS[1] + 10))
    WIN.blit(bottomText, (BUTTON_ONE_POS[0] + 17, BUTTON_ONE_POS[1] + 30))\
    # Button 2 Text
    topText = TEXT_FONT.render("Remove", 1, BLACK)
    bottomText = TEXT_FONT.render("Process", 1, BLACK)
    WIN.blit(topText, (BUTTON_TWO_POS[0] + 17, BUTTON_TWO_POS[1] + 10))
    WIN.blit(bottomText, (BUTTON_TWO_POS[0] + 17, BUTTON_TWO_POS[1] + 30))
    # Run Button Text
    topText = TEXT_FONT.render("Run", 1, BLACK)
    bottomText = TEXT_FONT.render("Simulation", 1, BLACK)
    WIN.blit(topText, (RUN_BUTTON_POS[0] + 29, RUN_BUTTON_POS[1] + 10))
    WIN.blit(bottomText, (RUN_BUTTON_POS[0] + 10, RUN_BUTTON_POS[1] + 30))
    # Process Text
    x = 0
    while x < currentNumProcesses:
        topText = TEXT_FONT.render("Process " + str(x + 1), 1, BLACK)
        atText = TEXT_FONT.render("Arrival Time: " + str(processes[x].arrivalTime), 1, BLACK)
        ctText = TEXT_FONT.render("CPU Time: " + str(processes[x].cpuTime), 1, BLACK)
        itText = TEXT_FONT.render("I/O Time: " + str(processes[x].ioTime), 1, BLACK)
        idText = TEXT_FONT.render("I/O Duration: " + str(processes[x].ioDuration), 1, BLACK)
        if x < 4:
            WIN.blit(topText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 30, TOP_PROCESS_POS[1] + 24))
            WIN.blit(atText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 5, TOP_PROCESS_POS[1] + 70))
            WIN.blit(ctText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 5, TOP_PROCESS_POS[1] + 90))
            WIN.blit(itText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 5, TOP_PROCESS_POS[1] + 110))
            if not processes[x].ioTime == -1:
                WIN.blit(idText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 5, TOP_PROCESS_POS[1] + 130))
        else:
            WIN.blit(topText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 30, BOTTOM_PROCESS_POS[1] + 24))
            WIN.blit(atText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 5, BOTTOM_PROCESS_POS[1] + 70))
            WIN.blit(ctText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 5, BOTTOM_PROCESS_POS[1] + 90))
            WIN.blit(itText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 5, BOTTOM_PROCESS_POS[1] + 110))
            if not processes[x].ioTime == -1:
                WIN.blit(idText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 5, BOTTOM_PROCESS_POS[1] + 130))
        x += 1

#Draw text during the simulation
def draw_sim_text():
    #Button 1 Text
    topText = TEXT_FONT.render("Go", 1, BLACK)
    bottomText = TEXT_FONT.render("Back", 1, BLACK)
    WIN.blit(topText, (BUTTON_ONE_POS[0] + 32, BUTTON_ONE_POS[1] + 10))
    WIN.blit(bottomText, (BUTTON_ONE_POS[0] + 25, BUTTON_ONE_POS[1] + 30))
    # Time Text
    topText = TIMER_FONT.render("Time: " + str(currentTime), 1, BLACK)
    WIN.blit(topText, (RUN_BUTTON_POS[0] - 10, RUN_BUTTON_POS[1] + 10))
    # Process Text
    x = 0
    while x < currentNumProcesses:
        topText = TEXT_FONT.render("Process " + str(x + 1), 1, BLACK)
        bottomText = TEXT_FONT.render(processes[x].currentState, 1, BLACK)
        if x < 4:
            WIN.blit(topText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 30, TOP_PROCESS_POS[1] + 4))
            WIN.blit(bottomText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 30, TOP_PROCESS_POS[1] + 24))
        else:
            WIN.blit(topText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 30, BOTTOM_PROCESS_POS[1] + 4))
            WIN.blit(bottomText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 30, BOTTOM_PROCESS_POS[1] + 24))
        x += 1

# Draw the processes and their state
def draw_processes():
    x = 0
    while x < currentNumProcesses:
        if x < 4:
            if processes[x].currentState == INIT or processes[x].currentState == ADMIT:
                WIN.blit(PROCESS_INIT, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET), TOP_PROCESS_POS[1]))
            elif processes[x].currentState == READY:
                WIN.blit(PROCESS_READY, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET), TOP_PROCESS_POS[1]))
            elif processes[x].currentState == RUNNING:
                WIN.blit(PROCESS_RUNNING, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET), TOP_PROCESS_POS[1]))
                stateText = TEXT_FONT.render("Time left: " + str(processes[x].cpuTime - processes[x].tempCPUTime), 1, BLACK)
                WIN.blit(stateText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 30, TOP_PROCESS_POS[1] + 44))
            elif processes[x].currentState == BLOCKED:
                WIN.blit(PROCESS_BLOCKED, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET), TOP_PROCESS_POS[1]))
                stateText = TEXT_FONT.render("I/O Time: " + str(processes[x].ioDuration - processes[x].tempIODuration), 1, BLACK)
                WIN.blit(stateText, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 30, TOP_PROCESS_POS[1] + 44))
            elif processes[x].currentState == DONE:
                WIN.blit(PROCESS_DONE, (TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET), TOP_PROCESS_POS[1]))
        else:
            if processes[x].currentState == INIT or processes[x].currentState == ADMIT:
                WIN.blit(PROCESS_INIT, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET), BOTTOM_PROCESS_POS[1]))
            elif processes[x].currentState == READY:
                WIN.blit(PROCESS_READY, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET), BOTTOM_PROCESS_POS[1]))
            elif processes[x].currentState == RUNNING:
                WIN.blit(PROCESS_RUNNING, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET), BOTTOM_PROCESS_POS[1]))
                stateText = TEXT_FONT.render("Time left: " + str(processes[x].cpuTime - processes[x].tempCPUTime), 1, BLACK)
                WIN.blit(stateText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 30, BOTTOM_PROCESS_POS[1] + 44))
            elif processes[x].currentState == BLOCKED:
                WIN.blit(PROCESS_BLOCKED, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET), BOTTOM_PROCESS_POS[1]))
                stateText = TEXT_FONT.render("I/O Time: " + str(processes[x].ioDuration - processes[x].tempIODuration), 1, BLACK)
                WIN.blit(stateText, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 30, BOTTOM_PROCESS_POS[1] + 44))
            elif processes[x].currentState == DONE:
                WIN.blit(PROCESS_DONE, (BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET), BOTTOM_PROCESS_POS[1]))
        x += 1

# Draw the settings textbox
def draw_settings():
    global processSettings
    if not processSettings == -1:
        WIN.blit(TEXTBOX, TEXTBOX_POS)
        headingText = SUBHEADING_FONT.render("Process " + str(processSettings + 1), 1, BLACK)
        atText = TEXT_FONT.render("Arrival Time: " + str(processes[processSettings].tempArrivalTime), 1, BLACK)
        ctText = TEXT_FONT.render("CPU Time: " + str(processes[processSettings].tempCPUTime), 1, BLACK)
        itText = TEXT_FONT.render("I/O Time: " + str(processes[processSettings].tempIOTime), 1, BLACK)
        idText = TEXT_FONT.render("I/O Duration: " + str(processes[processSettings].tempIODuration), 1, BLACK)
        WIN.blit(headingText, (TEXTBOX_POS[0] + 105, TEXTBOX_POS[1] + 10))
        # Arrival Time
        WIN.blit(atText, (TEXTBOX_POS[0] + 10, TEXTBOX_POS[1] + 50))
        WIN.blit(INCREMENT_BUTTON, (TEXTBOX_POS[0] + 200, TEXTBOX_POS[1] + 35))
        WIN.blit(DECREMENT_BUTTON, (TEXTBOX_POS[0] + 250, TEXTBOX_POS[1] + 35))
        # CPU Time
        WIN.blit(ctText, (TEXTBOX_POS[0] + 10, TEXTBOX_POS[1] + 90))
        WIN.blit(INCREMENT_BUTTON, (TEXTBOX_POS[0] + 200, TEXTBOX_POS[1] + 75))
        WIN.blit(DECREMENT_BUTTON, (TEXTBOX_POS[0] + 250, TEXTBOX_POS[1] + 75))
        # I/O Time
        WIN.blit(itText, (TEXTBOX_POS[0] + 10, TEXTBOX_POS[1] + 130))
        WIN.blit(INCREMENT_BUTTON, (TEXTBOX_POS[0] + 200, TEXTBOX_POS[1] + 115))
        WIN.blit(DECREMENT_BUTTON, (TEXTBOX_POS[0] + 250, TEXTBOX_POS[1] + 115))
        # I/O Duration
        WIN.blit(idText, (TEXTBOX_POS[0] + 10, TEXTBOX_POS[1] + 170))
        WIN.blit(INCREMENT_BUTTON, (TEXTBOX_POS[0] + 200, TEXTBOX_POS[1] + 155))
        WIN.blit(DECREMENT_BUTTON, (TEXTBOX_POS[0] + 250, TEXTBOX_POS[1] + 155))
        # Save Button
        WIN.blit(SMALL_BUTTON, (TEXTBOX_POS[0] + 75, TEXTBOX_POS[1]+ 210))
        saveText = TEXT_FONT.render("Save", 1, BLACK)
        WIN.blit(saveText, (TEXTBOX_POS[0] + 85, TEXTBOX_POS[1] + 219))
        # Cancel Button
        WIN.blit(SMALL_BUTTON, (TEXTBOX_POS[0] + 175, TEXTBOX_POS[1]+ 210))
        cancelText = TEXT_FONT.render("Cancel", 1, BLACK)
        WIN.blit(cancelText, (TEXTBOX_POS[0] + 180, TEXTBOX_POS[1] + 219))

# Initialize the process list
def create_process():
    x = 0
    while x < MAX_PROCESSES:
        processes[x] = process(x + 1, x + 1, -1, 1)
        processes[x].tempArrivalTime = processes[x].arrivalTime
        processes[x].tempCPUTime = processes[x].cpuTime
        processes[x].tempIOTime = processes[x].ioTime
        processes[x].tempIODuration = processes[x].ioDuration
        x += 1

def reset_processes():
    if simulating:
        for i in processes:
            i.currentState = INIT
            i.tempIODuration = 0
            i.tempCPUTime = 0
    else:
        global currentTime, admitList, readyList, runningNum, interruptList, cpuNum
        for i in processes:
            i.currentState = READY
            i.tempIODuration = i.ioDuration
            i.tempCPUTime = i.cpuTime
        currentTime = 0
        runningNum = -1
        cpuNum = -1
        readyList.clear()
        admitList.clear()
        interruptList.clear()

def clicked():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global simulating, currentNumProcesses, currentTime, processSettings
    # Menu clicks
    if not simulating:
        if mouse_x > RUN_BUTTON_POS[0] and mouse_x < RUN_BUTTON_POS[0] + 81 and mouse_y > RUN_BUTTON_POS[1] and mouse_y < RUN_BUTTON_POS[1] + 51:
            simulating = True
            reset_processes()
            process_arrival()
            process_io()
        elif mouse_x > BUTTON_ONE_POS[0] and mouse_x < BUTTON_ONE_POS[0] + 81 and mouse_y > BUTTON_ONE_POS[1] and mouse_y < BUTTON_ONE_POS[1] + 51 and currentNumProcesses < MAX_PROCESSES:
            currentNumProcesses += 1
        elif mouse_x > BUTTON_TWO_POS[0] and mouse_x < BUTTON_TWO_POS[0] + 81 and mouse_y > BUTTON_TWO_POS[1] and mouse_y < BUTTON_TWO_POS[1] + 51 and currentNumProcesses > 1:
            currentNumProcesses -= 1

        if processSettings == -1:
            x = 0
            while x < currentNumProcesses:
                if mouse_x > TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) and mouse_x < TOP_PROCESS_POS[0] + (x * PROCESS_OFFSET) + 121 and mouse_y > TOP_PROCESS_POS[1] and mouse_y < TOP_PROCESS_POS[1] + 61:
                    processSettings = x
                elif mouse_x > BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) and mouse_x < BOTTOM_PROCESS_POS[0] + ((x - 4) * PROCESS_OFFSET) + 121 and mouse_y > BOTTOM_PROCESS_POS[1] and mouse_y < BOTTOM_PROCESS_POS[1] + 61:
                    processSettings = x
                x += 1
        else:
            # Save Button
            if mouse_x > TEXTBOX_POS[0] + 75 and mouse_x < TEXTBOX_POS[0] + 126 and mouse_y > TEXTBOX_POS[1] + 210 and mouse_y < TEXTBOX_POS[1] + 241:
                processes[processSettings].arrivalTime = processes[processSettings].tempArrivalTime
                processes[processSettings].cpuTime = processes[processSettings].tempCPUTime
                processes[processSettings].ioTime = processes[processSettings].tempIOTime
                processes[processSettings].ioDuration = processes[processSettings].tempIODuration
                processSettings = -1
            # Cancel Button
            elif mouse_x > TEXTBOX_POS[0] + 175 and mouse_x < TEXTBOX_POS[0] + 226 and mouse_y > TEXTBOX_POS[1] + 210 and mouse_y < TEXTBOX_POS[1] + 241:
                processes[processSettings].tempArrivalTime = processes[processSettings].arrivalTime
                processes[processSettings].tempCPUTime = processes[processSettings].cpuTime
                processes[processSettings].tempIOTime = processes[processSettings].ioTime
                processes[processSettings].tempIODuration = processes[processSettings].ioDuration
                processSettings = -1
            # Increment Button
            elif mouse_x > TEXTBOX_POS[0] + 200 and mouse_x < TEXTBOX_POS[0] + 231:
                if mouse_y > TEXTBOX_POS[1] + 35 and mouse_y < TEXTBOX_POS[1] + 71 and processes[processSettings].tempArrivalTime < MAX_TIME:
                    processes[processSettings].tempArrivalTime += 1
                elif mouse_y > TEXTBOX_POS[1] + 75 and mouse_y < TEXTBOX_POS[1] + 111 and processes[processSettings].tempCPUTime < MAX_TIME:
                    processes[processSettings].tempCPUTime += 1
                elif mouse_y > TEXTBOX_POS[1] + 115 and mouse_y < TEXTBOX_POS[1] + 151 and processes[processSettings].tempIOTime < processes[processSettings].tempCPUTime - 1:
                    if not processes[processSettings].tempIOTime == -1:
                        processes[processSettings].tempIOTime += 1
                    else:
                        processes[processSettings].tempIOTime = 1
                elif mouse_y > TEXTBOX_POS[1] + 155 and mouse_y < TEXTBOX_POS[1] + 191 and processes[processSettings].tempIODuration < MAX_TIME:
                    processes[processSettings].tempIODuration += 1
            # Decrement Button
            elif mouse_x > TEXTBOX_POS[0] + 250 and mouse_x < TEXTBOX_POS[0] + 281:
                if mouse_y > TEXTBOX_POS[1] + 35 and mouse_y < TEXTBOX_POS[1] + 71 and processes[processSettings].tempArrivalTime > 0:
                    processes[processSettings].tempArrivalTime -= 1
                elif mouse_y > TEXTBOX_POS[1] + 75 and mouse_y < TEXTBOX_POS[1] + 111 and processes[processSettings].tempCPUTime > 1 and processes[processSettings].tempCPUTime > processes[processSettings].tempIOTime + 1:
                    processes[processSettings].tempCPUTime -= 1
                elif mouse_y > TEXTBOX_POS[1] + 115 and mouse_y < TEXTBOX_POS[1] + 151:
                    if not processes[processSettings].tempIOTime == 1:
                        processes[processSettings].tempIOTime -= 1
                    else:
                        processes[processSettings].tempIOTime = -1
                elif mouse_y > TEXTBOX_POS[1] + 155 and mouse_y < TEXTBOX_POS[1] + 191 and processes[processSettings].tempIODuration > 1:
                    processes[processSettings].tempIODuration -= 1
                
    # Simulation clicks
    else:
        if mouse_x > BUTTON_ONE_POS[0] and mouse_x < BUTTON_ONE_POS[0] + 81 and mouse_y > BUTTON_ONE_POS[1] and mouse_y < BUTTON_ONE_POS[1] + 51:
            simulating = False
            reset_processes()
        else:
            currentTime += 1
            process_arrival()
            process_io()
            cpu()

def process_arrival():
    global currentTime, admitList
    x = 0
    while x < currentNumProcesses:
        if currentTime == processes[x].arrivalTime:
            processes[x].currentState = ADMIT
            admitList.append(x)
        x += 1

def process_io():
    global interruptList
    x = 0
    while x < currentNumProcesses:
        if processes[x].currentState == BLOCKED and processes[x].tempIODuration < processes[x].ioDuration:
            processes[x].tempIODuration += 1
            if processes[x].tempIODuration == processes[x].ioDuration:
                interruptList.append(x)
                processes[x].ioTime = -1
        x += 1

# Simulates the cpu
def cpu():
    global readyList, admitList, runningNum, currentTime, interruptList, cpuNum
    # Process is currently running
    if not runningNum == -1:
        # Process gets interrupted by an io device
        if processes[runningNum].tempCPUTime == processes[runningNum].ioTime:
            processes[runningNum].currentState = BLOCKED
            cpuNum = runningNum
            runningNum = -1
        # Process is finished running
        elif processes[runningNum].tempCPUTime >= processes[runningNum].cpuTime:
            processes[runningNum].currentState = DONE
            cpuNum = runningNum
            runningNum = -1
        # Process keeps running
        else:
            processes[runningNum].tempCPUTime += 1
            cpuNum = runningNum
    # No process is currently running
    else:
        # Admit arrived process to ready list
        if len(admitList) > 0:
            readyList.append(admitList[0])
            processes[admitList[0]].currentState = READY
            cpuNum = admitList[0]
            admitList.pop(0)
        # Add blocked process back to ready list
        elif len(interruptList) > 0:
            readyList.append(interruptList[0])
            processes[interruptList[0]].currentState = READY
            cpuNum = interruptList[0]
            interruptList.pop(0)
        # Assign a process to the cpu
        else:
            if len(readyList) > 0:
                runningNum = readyList[0]
                processes[runningNum].currentState = RUNNING
                cpuNum = runningNum
                readyList.pop(0)

def draw_cpu(num):
    if num < 4:
        WIN.blit(CPU, (TOP_PROCESS_POS[0] + (num * PROCESS_OFFSET) + 25, TOP_PROCESS_POS[1] + 65))
    else:
        WIN.blit(CPU, (BOTTOM_PROCESS_POS[0] + ((num - 4) * PROCESS_OFFSET) + 25, BOTTOM_PROCESS_POS[1] + 65))

if __name__ == "__main__":
    main()