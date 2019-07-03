#So I have this 128 bit input in form of 32 hexagonal digits. Now I need to
#work with them.
from KeyExpansion import SubWord

def SubBytes(state):                    #Verified
  for row in range(4):
    word = ""
    for column in range(4):
      word += state[row][column]
    temp = SubWord(word)
    for column in range(4):
      state[row][column] = temp[2*column:2*column+2]  
  return state

def hextoint2dig(param):
  temp = int('{0:04b}'.format(int(param[0], base = 16))+'{0:04b}'.format(int(param[1], base = 16)), base = 2)
  return temp


def AddRoundKey(state, key):           #Verified
  for i in range (4):
    for j in range(4):
        temp = ""
        temp = '{0:0x}'.format(int(state[i][j][0], base = 16)^int(key[j][2*i], base = 16)) + '{0:0x}'.format(int(state[i][j][1], base = 16)^ int(key[j][2*i+1], base = 16))
        state[i][j] = temp
  return state

def digtohex2dig(tempint): 
  temp = ""
  tempbin = '{0:08b}'.format(tempint)
  temp = '{0:0x}'.format(int(tempbin[0:4], base = 2))+'{0:0x}'.format(int(tempbin[4:8], base =2))
  return temp

def MixColumn(state):                                                               #Verified
  state_new = [['xy' for x in range(4)] for y in range(4)]
  multConst = [["02","03","01","01"],["01","02","03","01"],["01","01","02","03"],["03","01","01","02"]]
  for index in range(4):
    for row in range(4):
      tempint = 0
      for column in range(4):
        numbertoxor = hextoint2dig(state[column][index])
        if multConst[row][column] is "02":
            if numbertoxor <2**7:
                tempint = tempint ^ numbertoxor<<1
            else:
                tempint = tempint ^  (numbertoxor<<1)%(2**8) ^ 27
        elif multConst[row][column] is "01":
          tempint = tempint ^ numbertoxor
        elif multConst[row][column] is "03":
            if numbertoxor < 2**7:
                tempint = tempint ^ (numbertoxor<<1) ^ numbertoxor
            else:
                tempint = tempint ^ ((numbertoxor<<1)%(2**8) ^ 27) ^ numbertoxor
      
      state_new[row][index] = digtohex2dig(tempint)        
  return state_new

def ShiftRow(state): 
  state_new = [['xy' for x in range(4)] for y in range(4)]                          #Verified
  for row in range(4):
    for row in range(4):
      for column in range(4):
        if row == 0:
          state_new[row][column] = state[row][column]
        elif row == 1:
          state_new[row][column] = state[row][(column+1)%4]
        elif row == 2:
          state_new[row][column] = state[row][(column+2)%4]
        elif row == 3:
          state_new[row][column] = state[row][(column+3)%4]
  return state_new


def encrypt(input, key, Nr):
  state = list()
  for i in range(4):
    temp = list()
    for j in range(4):
      temp.append(input[8*j+2*i:8*j+2*(i+1)])
    state.append(temp)

  state = AddRoundKey(state, key[0:4])

  for round in range(Nr-1):
    state = SubBytes(state)
    state = ShiftRow(state)
    state = MixColumn(state)
    state = AddRoundKey(state, key[4*(round+1):4*(round+2)])

  state = SubBytes(state)
  state = ShiftRow(state)
  state = AddRoundKey(state, key[40:44])
  out = ""
  for i in range(4):
    for j in range(4):
      out += state[j][i]
  return out
