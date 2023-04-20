import cv2

cv2.namedWindow("preview")

vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

frameCounter = 0
leftHand = ""
rightHand = ""
pastLeftHand = ""
pastRightHand = ""
leftScore = 0
rightScore = 0

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

def matchLeftHand(img_gray):
    scissors = cv2.imread('assets/left_scissors.png', 0)
    matchScissors = cv2.matchTemplate(img_gray, scissors, cv2.TM_SQDIFF_NORMED).max()

    stone = cv2.imread('assets/left_rock.png', 0)
    matchStone = cv2.matchTemplate(img_gray, stone, cv2.TM_CCOEFF_NORMED).max()

    if(matchStone < 0.49):
        return "PEDRA"
    elif(matchScissors > 0.22):
        return "TESOURA"
    else:
        return "PAPEL"

def matchRightHand(img_gray):
    scissors = cv2.imread('assets/right_scissors.png', 0)
    matchScissors = cv2.matchTemplate(img_gray, scissors, cv2.TM_SQDIFF_NORMED).max()

    stone = cv2.imread('assets/right_rock.png', 0)
    matchStone = cv2.matchTemplate(img_gray, stone, cv2.TM_SQDIFF_NORMED).max()

    if(matchStone > 0.2 and matchStone < 0.21):
        return "PEDRA"
    if (matchScissors > 0.2194):
        return "TESOURA"
    else:
        return "PAPEL"

def calcResultado(leftHand, rightHand):
    if(rightHand == leftHand):
        printResultado("EMPATE", "EMPATE")
        return "EMPATE", "EMPATE"
    elif(rightHand == "PEDRA" and leftHand == "TESOURA"):
        printResultado("DERROTA", "VITORIA")
        return "DERROTA", "VITORIA"
    elif (rightHand == "PAPEL" and leftHand == "PEDRA"):
        printResultado("DERROTA", "VITORIA")
        return "DERROTA", "VITORIA"
    elif (rightHand == "TESOURA" and leftHand == "PAPEL"):
        printResultado("DERROTA", "VITORIA")
        return "DERROTA", "VITORIA"
    else:
        printResultado("VITORIA", "DERROTA")
        return "VITORIA", "DERROTA"

def printResultado(leftHandResult, rightHandResult):
    font = cv2.FONT_HERSHEY_SIMPLEX

    if leftHandResult == "VITORIA":
        cv2.putText(frame, str(leftHandResult), (350, 1000), font, 3, (0, 255, 0), 8, cv2.LINE_AA)
    elif leftHandResult == "EMPATE":
        cv2.putText(frame, str(leftHandResult), (725, 1000), font, 3, (144, 0, 145), 8, cv2.LINE_AA)
    else:
        cv2.putText(frame, str(rightHandResult), (1100, 1000), font, 3, (0, 255, 0), 8, cv2.LINE_AA)

def calcScore(resultLeftHand, resultRightHand):
    global leftHand
    global rightHand
    global leftScore
    global rightScore
    global pastLeftHand
    global pastRightHand
    if not leftHand == pastLeftHand or not rightHand == pastRightHand:
        if resultLeftHand == "VITORIA":
            leftScore += 1
        elif resultRightHand == "VITORIA":
            rightScore += 1
        pastLeftHand = leftHand
        pastRightHand = rightHand

def showTexts():
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, str(leftHand), (350, 200), font, 3, (200, 50, 0), 5, cv2.LINE_AA)
    cv2.putText(frame, str(rightHand), (1100, 200), font, 3, (200, 50, 0), 5, cv2.LINE_AA)

    resultLeftHand, resultRightHand = calcResultado(leftHand, rightHand)
    calcScore(resultLeftHand, resultRightHand)

    cv2.putText(frame, "Left score: " + str(leftScore), (1600, 900), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Right score: " + str(rightScore), (1600, 1000), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

def matchHands():
    global frameCounter
    global leftHand
    global rightHand

    frameCounter += 1
    img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    if (frameCounter == 10):
        frameCounter = 0
        leftHand = matchLeftHand(img_gray)
        rightHand = matchRightHand(img_gray)


while rval:
    matchHands()
    showTexts()

    cv2.imshow("game", frame)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

def higherScore():
    if leftHand == rightHand:
        return "O jogo resultou em empate"
    elif leftHand > rightHand:
        return "O vencedor foi o jogador da esquerda"
    else:
        return "O vencedor foi o jogador da direita"

print("===============================")
print("          Score final          ")
print("===============================")
print("Jogador da esquerda: " + str(leftScore))
print("Jogador da direita: " + str(rightScore))
print("===============================")
print(higherScore())

cv2.destroyWindow("preview")
vc.release()