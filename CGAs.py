import copy
import AL
import ortool as Or
import crossover as Cr
import mutation as Mu

#------------------------------[FUNCTION]------------------------------------

def Read_Data(filename='data.txt'):
    # Khởi tạo mảng để lưu dữ liệu
    data_rows = []
    # Đọc từng dòng của tệp và thêm vào mảng data_rows
    with open(filename, 'r') as file:
        for line in file:
            # Tách các giá trị trong dòng và chuyển thành số nguyên
            row = list(map(int, line.strip().split()))
            data_rows.append(row)
    # Chuyển mảng thành mảng NumPy
    structure = [[[0 for i in range(data_rows[0][2])] for j in range(data_rows[0][1])] for k in range(data_rows[0][0])]
    for i in range(len(data_rows)-1):
        no = 1
        for j in range(data_rows[i+1][0]):
            for k in range(no + 1,2*data_rows[i+1][no]+no,2):
                structure[i][j][data_rows[i+1][k]-1] = data_rows[i+1][k+1]
            no = no + 2*data_rows[i+1][no]+1
    for i in range(len(structure)):
        for j in range(len(structure[i])):
            for k in range(len(structure[i][j])):
                if structure[i][j][k] == 0:
                    structure[i][j][k] = 99
    return structure

def chromosome(Data_Input,loop):
    nE = []
    n = 0
    n2 = 0
    while n < loop:
        EE = []
        EE = AL.gen1(Data_Input,99)
        if EE not in nE :
            nE.append(EE)
            n = 0
        else:
            n += 1
    while n2 < loop:
        EE = []
        EE = AL.gen2(Data_Input,99)
        if EE not in nE :
            nE.append(EE)
            n2 = 0
        else:
            n2 += 1
    E_chromosome = [[0 for k in range(3)] for j in range(len(nE))]
    for i in range(len(nE)):
        E_chromosome[i][0] = nE[i]
        ec = Or.format_data(E_chromosome[i][0],Data_Input)
        a = Or.JSP_OR(ec)
        E_chromosome[i][1] = a.makespans()
        E_chromosome[i][2] = a.workloads()
    E_chromosome1 = sorted(E_chromosome, key=lambda sublist: (sublist[1], sublist[2]))
    return E_chromosome1

def Genetic_Algorithms(Data_in,population_size,generation,crossover_probability,mutation1_probability,mutation2_probability):
    D = Data_in    #Đưa dữ liệu vào mảng D
    E = chromosome(D,10)    #Xây dựng quần thể (bộ nhiễm sắc thể choromosome(dữ liệu vào, số lượng gen mong muốn, số vòng lặp random))
    
    c = int(population_size*crossover_probability)
    m1 = int(population_size*mutation1_probability)
    m2 = int(population_size*mutation2_probability)

    Q = E
    x = 1
    y = 0
    Cmax_find = 99999
    WL_find = 99999
    Assignment = [ 0 for i in range(100)]
    while x <= generation:
        QQ = copy.deepcopy(Q)

        #Lai ghép
        C1 = [0 for j in range(c)]
        for i in range(0,c,2):
            F = Cr.cross(D,Q)
            C1[i] = F[0]
            C1[i+1] = F[1]

        #Đột biến kiểu 1
        M1 = [0 for j in range(m1)]
        for i in range(m1):
            M1[i] = Mu.mutation1(C1,D)

        #Đột biến kiểu 2
        M2 = [0 for j in range(m2)]
        for i in range(m2):
            M2[i] = Mu.mutation2(C1,D)

        #Gộp các tổ hợp
        C1.extend(M1)
        C1.extend(M2)
        # Tạo mảng Q2 bao gồm cả chỉ số đánh giá Makespans
        Q2 = [[0 for j in range(3)] for k in range(population_size)]
        for i3 in range(len(Q2)):
            Q2[i3][0] = C1[i3]
            q2f = Or.format_data(Q2[i3][0],D)
            Q2[i3][1] = Or.JSP_OR(q2f).makespans()
            Q2[i3][2] = Or.JSP_OR(q2f).workloads()
        # Gộp G2 vào tập quần thể ban đầu
        Q2.extend(QQ)
        # Sắp xếp các phần tử trong Q2 theo thứ tự tăng dần Cmax
        QQ2 = sorted(Q2, key=lambda sublist: (sublist[1], sublist[2]))
        # Loại bỏ các phần tử giống nhau trong QQ2 lưu vào QQ3
        QQ3 = []
        for element in QQ2:
            if element not in QQ3:
                QQ3.append(element)
        # Lấy n phần tử đầu của QQ3 thay vào Q
        Q = QQ3[:population_size]
        if Q[0][1] <= Cmax_find or Q[0][2] <= WL_find:
            Cmax_find = Q[0][1]
            WL_find = Q[0][2]
            Assf = Or.format_data(Q[0][0],D)
            WL = Or.JSP_OR(Assf).workloads_per_machine()
            if WL not in Assignment:
                Assignment.append(WL)
                print(f"________________________BEST SOLUTION IN GENERATION {x}_______________________")
                for i in range(len(Assf)):
                    print(Assf[i])
                Or.JSP_OR(Assf).scheduling()
                print("Makespans : = ", Or.JSP_OR(Assf).makespans())
                print("Workloads : = ", Or.JSP_OR(Assf).workloads())
                print("Workloads per Machines : = ", Or.JSP_OR(Assf).workloads_per_machine())
                print("Time per Jobs : = ", Or.JSP_OR(Assf).processing_time())
                y += 1
        x += 1
#-----------------------------[MAIN]--------------------------------------------------------
values = Read_Data('kacem4.txt')
Genetic_Algorithms(values,1000,1000,1,0.5,0.5)
#-----------------------------[END]---------------------------------------------------------