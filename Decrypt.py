import Encrypt

def xtime(numbertoxor):
     if numbertoxor <2**7:
        return numbertoxor<<1
     else:
        return (numbertoxor<<1)%(2**8) ^ 27

def InvSubWord(a):
    invSBOX = [
    ["52","09","6a","d5","30","36","a5","38","bf","40","a3","9e","81","f3","d7","fb"],
    ["7c","e3","39","82","9b","2f","ff","87","34","8e","43","44","c4","de","e9","cb"],
    ["54","7b","94","32","a6","c2","23","3d","ee","4c","95","0b","42","fa","c3","4e"],
    ["08","2e","a1","66","28","d9","24","b2","76","5b","a2","49","6d","8b","d1","25"],
    ["72","f8","f6","64","86","68","98","16","d4","a4","5c","cc","5d","65","b6","92"],
    ["6c","70","48","50","fd","ed","b9","da","5e","15","46","57","a7","8d","9d","84"],
    ["90","d8","ab","00","8c","bc","d3","0a","f7","e4","58","05","b8","b3","45","06"],
    ["d0","2c","1e","8f","ca","3f","0f","02","c1","af","bd","03","01","13","8a","6b"],
    ["3a","91","11","41","4f","67","dc","ea","97","f2","cf","ce","f0","b4","e6","73"],
    ["96","ac","74","22","e7","ad","35","85","e2","f9","37","e8","1c","75","df","6e"],
    ["47","f1","1a","71","1d","29","c5","89","6f","b7","62","0e","aa","18","be","1b"],
    ["fc","56","3e","4b","c6","d2","79","20","9a","db","c0","fe","78","cd","5a","f4"],
    ["1f","dd","a8","33","88","07","c7","31","b1","12","10","59","27","80","ec","5f"],
    ["60","51","7f","a9","19","b5","4a","0d","2d","e5","7a","9f","93","c9","9c","ef"],
    ["a0","e0","3b","4d","ae","2a","f5","b0","c8","eb","bb","3c","83","53","99","61"],
    ["17","2b","04","7e","ba","77","d6","26","e1","69","14","63","55","21","0c","7d"]
    ]
    
    final = ""

    for x in range(4):
        final += invSBOX[int(a[2*x], base = 16)][int(a[2*x+1], base=16)]
    
    return final

def InvShiftRow(state):
  state_new = [['xy' for x in range(4)] for y in range(4)]                          #Verified

  for row in range(4):
      for column in range(4):
        if row == 0:
          state_new[row][column] = state[row][column]
        elif row == 1:
          state_new[row][column] = state[row][(column+3)%4]
        elif row == 2:
          state_new[row][column] = state[row][(column+2)%4]
        elif row == 3:
          state_new[row][column] = state[row][(column+1)%4]
  return state_new


def InvSubBytes(state):
    for row in range(4):
        word = ""
        for column in range(4):
            word += state[row][column]
        temp = InvSubWord(word)
        for column in range(4):
            state[row][column] = temp[2*column:2*column+2]  
    return state

def InvMixColumn(state):
    inv_special_matrix = [
    ["0E", "0B", "0D", "09"],
    ["09", "0E", "0B", "0D"],
    ["0D", "09", "0E", "0B"],
    ["0B", "0D", "09", "0E"],
    ]

    state_new = [['xy' for x in range(4)] for y in range(4)]

    for index in range(4):
        for row in range(4):
            tempint = 0
            for column in range(4):
                numbertoxor = Encrypt.hextoint2dig(state[column][index])
                ansx = xtime(numbertoxor)
                ansx2 = xtime(ansx)
                ansx3 = xtime(ansx2)
                if inv_special_matrix[row][column] is "0E":
                   tempint = tempint ^ ansx ^ ansx2 ^ ansx3

                elif inv_special_matrix[row][column] is "0B":
                    tempint = tempint ^ numbertoxor ^ ansx ^ ansx3

                elif inv_special_matrix[row][column] is "0D":
                    tempint = tempint ^ numbertoxor ^ ansx3 ^ ansx2 

                else:
                    tempint = tempint ^ numbertoxor ^ ansx3
      
            state_new[row][index] = Encrypt.digtohex2dig(tempint)        
    return state_new

def decrypt(input, key, Nr):
    state = list()
    for i in range(4):
        temp = list()
        for j in range(4):
            temp.append(input[8*j+2*i:8*j+2*(i+1)])
        state.append(temp)
    
    state = Encrypt.AddRoundKey(state,key[4*Nr:4*(Nr+1)])
    
    for i in range(Nr-1):
        state = InvShiftRow(state)
        state = InvSubBytes(state)
        state = Encrypt.AddRoundKey(state, key[4*(Nr-i-1):4*(Nr-i)])
        state = InvMixColumn(state)
    
    state = InvShiftRow(state)
    state = InvSubBytes(state)
    state = Encrypt.AddRoundKey(state, key [0:4])
    

    out = ""
    for i in range(4):
        for j in range(4):
         out += state[j][i]
    return out