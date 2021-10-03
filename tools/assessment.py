def assessment_RandomN(self, number = 8):
    coefficient = side_length/2
    self._targets = []
    text = 'Center'
    self._targets.append((0,0,text))

    while (len(self._targets) != number):
        xgame = np.random.random_integers(-coefficient, coefficient)
        ygame = np.random.random_integers(-coefficient, coefficient)
        text = '('+ str(xgame) + str(ygame) + ')'
        print(xgame,ygame)
        
        doubled = False
        ##### hey work on this wth is this forloop doing
        for i in range(len(self._targets)):
            if (xgame == self._targets[i][0]) and (ygame == self._targets[i][1]):
                    doubled = True
            if doubled == False:
                text = '(' + str(xgame) + ',' + str(ygame) +')'
                self._targets.append((xgame,ygame,text))

    # print (self._targets)
    # self._target_circle = plt.Circle((x,y), 1.5 , color='r',fill=False)
    # #adding circle around the marker.
    # ax.add_patch(cir)

        
def assessment_FivePoint(self, number = 5):
    coefficient = side_length/2
    self._targets = []
    center = 'Center'
    self._targets.append((0,0,center))

    for i in range(number):
        rand = np.random.random_integers(1, 4)
        if rand == 1:
            xgame = -coefficient
            ygame = coefficient
            text = 'Top - Left'
        if rand == 2:
            xgame = coefficient
            ygame = coefficient
            text = 'Top - Right'
        if rand == 3:
            xgame = -coefficient
            ygame = -coefficient
            text = 'Bottom - Left'
        if rand == 4:
            xgame = coefficient
            ygame = -coefficient
            text = 'Bottom - Right'
        self._targets.append((xgame,ygame,text))
        
        self._targets.append((0,0,center))