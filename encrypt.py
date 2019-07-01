#So I have this 128 bit input in form of 32 hexagonal digits. Now I need to
#work with them.

def hextoint2dig(param):
  temp = int('{0:04b}'.format(int(param[0], base = 16))+'{0:04b}'.format(int(param[1], base = 16)), base = 2)
  return temp


def AddRoundKey(state, key):
  for i in range (4):
    for j in range(4):
        temp = ""
        temp = '{0:0x}'.format(int(state[i][j][0], base = 16)^int(key[2*i][j], base = 16)) + '{0:0x}'.format(int(state[i][j][1], base = 16)^ int(key[2*i+1][j])
        state[i][j] = temp
  return state

def digtohex2dig(tempint):
  temp = ""
  tempbin = '{0:08b}'.format(tempint)
  temp = '{0:0x}'.format(int(tempbin[0:4], base = 2))+'{0:0x}'.format(int(tempbin[4:8], base =2))
  return temp

def MixColumn(state):
  state_new = state
  multConst = [["02","03","01","01"],["01","02","03","01"],["01","01","02","03"],["03","01","01","02"]]
  for index in range(4);
    for row in range(4):
      tempint = 0

      for column in range(4):
        if multConst is "02":
          tempint = tempint ^  (hextoint2dig(state[column][index])<<1) ^ 27
        elif multiConst is "01":
          tempint = tempint ^ hextoint2dig(state[column][index])
        elif multiConsr is "03":
          tempint = tempint ^ (hextoint2dig(state[column][index])<<1) ^ 27 ^ hextoint2dig(state[column][index])

      state_new[row][index] = digtohex2dig(tempint)        #Function to be defined
  return state_new

def ShiftRows(state):
  for row in range(4):
    if row == 1:
      temp = state[1][0]
      for column in range(2):
        state[row][column] = state[row][column+2]
      state[1][3] = temp
    elif row == 2:
      temp1 = state[2][0]
      temp2 = state[2][1]
      for column in range(2):
        state[row][column] = state[row][column+2]
      state[2][2] = temp1
      state[2][3] = temp2
    elif row == 3:
      temp1 = state[3][0]
      temp2 = state[3][1]
      temp3 = state[3][2]
      for column in range(1):
        state[row][column] = state[row][column+3]
      state[3][1] = temp1
      state[3][2] = temp2
      state[3][3] = temp3



def encrypt(input, key, Nr):
  state = list()
  for i in range(4):
    temp = list()
    for j in range(4):
      temp.append(input[8*j+2*i:8*j+2*(i+1)])
    state.append(temp)
  #State generated

#We can use sub bytes from keyexpansion file and finally writing part is done!!!

  state = AddRoundKey(state, key[0:4])

  for round in range(Nr-1):
    state = AddRoundKey(MixColumn(ShiftRow(SubBytes(state))),key[4*(i+1):4*(i+2)] )

  state = AddRoundKey(ShiftRow(SubByte(state)), key[40:44])

  #Rounds done Now we have to get back output
  out = ""
  for i in range(4):
    for j in range(4):
      out += state[j][i]
  return out


