
import os
import datetime

def main():
    start = datetime.datetime.now()
    os.chdir('C:/Users/JIANGMI/Desktop/CANoe/SFTP16/180705_PK_Actros10/')
    acs = 'I:/VehicleLogs/Actros10/180705_PK_Actros10/Trace_Actros10_20180704_050357_20180704_085304_#01-1_CHA-CAN.asc'
    trigger_list = [['14FF00E8x', 'ABA', 22, 2],\
        ['10FF007Fx', 'LDWA', 24, 2]]
    n = len(trigger_list)

    for i in range(0, n):
        searchmessage(trigger_list[i], acs)

    end = datetime.datetime.now()
    print(end-start)

def searchmessage(trigger_list, acs):

    message = trigger_list[0]
    def_name = trigger_list[1]+'_1-1'
    start_bit = trigger_list[2]
    bit_len = trigger_list[3]
    slic = [[] for j in range(10)]
    j = 0
    n = 0
    status = 0
    ignition = 2
    with open(acs, 'r') as inputfile:
        for line in inputfile:
            uline = line.split()
            n += 1
            if n> 10:
                ignition = signal_val(ignition, uline, '10FF0021x', 0, 4)
                if ignition == 2:
                    old_status = status
                    status = signal_val(status, uline, message, start_bit, bit_len)
                    if old_status != status:
                        change_status = 1
                    else:
                        change_status = 0

                    if change_status == 1 and status == 0:
                        filename = def_name + str(j) + '.asc'
                        slic[j].extend([filename, float(uline[0])])

                    if change_status == 1 and status == 1:
                        if slic[j] == []:
                            filename = def_name + str(j) + '.asc'
                            slic[j].extend([filename, float(uline[0])])
                        slic[j].append(float(uline[0]))
                        j += 1
    del slic[(j):10]
    del slic[0]
    print(slic)
    writefile(acs, slic)






def signal_val(old_val, uline, message, start_bit, bit_len):
    n_byte = []
    if uline[2] == message:
        byte0 = start_bit // 8
        bit0 = start_bit % 8
        m_byte = '{:08b}'.format(int(uline[6 + byte0], 16))
        val0 = int(m_byte[(8-bit_len-bit0):(8-bit0)], 2)
        return val0   
    else:
        return old_val

def writefile(acs, slic):
    header = open('C:/Users/JIANGMI/Desktop/CANoe/SFTP18/191028_MB_V959/ASC_header.txt', 'r')
    line_header = header.readlines()
    n = len(slic)
    for f in range(0,n):
        slic[f][1] -= 5
        slic[f][2] += 5
        locals()[slic[f][0]] = open(slic[f][0], 'w')
        locals()[slic[f][0]].writelines(line_header)
        locals()[slic[f][0]].close()
        locals()[slic[f][0]] = open(slic[f][0], 'a')
    header.close()

    with open(acs, 'r') as inputfile:
        i = 0
        j = 0
        condition = 0
        for line in inputfile:
            uline = line.split()
            j +=1
            if i == n:
                break

            if j > 10:
                if float(uline[0]) > slic[i][1] and float(uline[0]) < slic[i][2]:
                    locals()[slic[i][0]].write(line)
                    condition = 1

                elif condition ==1 :
                    i += 1
                    condition =0


main()
