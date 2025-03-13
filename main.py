import math

def calculate_belt_length(C1, C2, D):
    r1 = C1 / (2 * math.pi)
    r2 = C2 / (2 * math.pi)
    delta = abs(r1 - r2)
    
    if D < delta:
        raise ValueError("错误：圆心距D不能小于两轮半径之差的绝对值。")
    
    try:
        theta = math.asin(delta / D)
    except:
        raise ValueError("无法计算带包角，请检查输入参数是否合理。")
    
    # 计算带包角
    if r1 > r2:
        angle1 = math.pi + 2 * theta
        angle2 = math.pi - 2 * theta
    else:
        angle1 = math.pi - 2 * theta
        angle2 = math.pi + 2 * theta
    
    dbj1 = (angle1 / math.pi) * 180
    dbj2 = (angle2 / math.pi) * 180
    print(f"带包角1 = {dbj1:.2f}°")
    print(f"带包角2 = {dbj2:.2f}°")
    
    # 计算弧长和切线长
    arc_length1 = angle1 * r1
    arc_length2 = angle2 * r2
    tangent_length = 2 * math.sqrt(D**2 - delta**2)
    
    L = arc_length1 + arc_length2 + tangent_length
    return L

def calculate_circle_center_distance(C1, C2, L):
    r1 = C1 / (2 * math.pi)
    r2 = C2 / (2 * math.pi)
    delta = abs(r1 - r2)
    
    # 牛顿迭代法求解D
    def f(D):
        if D <= delta:
            return float('inf')
        try:
            theta = math.asin(delta / D)
        except:
            return float('inf')
        angle1 = math.pi + 2*theta if r1 > r2 else math.pi - 2*theta
        angle2 = math.pi - 2*theta if r1 > r2 else math.pi + 2*theta
        tangent = 2 * math.sqrt(D**2 - delta**2)
        return angle1*r1 + angle2*r2 + tangent - L
    
    # 初始猜测值
    D_guess = max(delta + 1, (r1 + r2))
    tolerance = 1e-6
    max_iter = 1000
    
    for _ in range(max_iter):
        f_val = f(D_guess)
        if abs(f_val) < tolerance:
            break
        h = 1e-6
        f_derivative = (f(D_guess + h) - f_val) / h
        if f_derivative == 0:
            break
        D_guess -= f_val / f_derivative
        D_guess = max(D_guess, delta + 1e-6)
    
    # 角度重计算
    theta = math.asin(delta / D_guess)
    if r1 > r2:
        angle1 = math.pi + 2 * theta
        angle2 = math.pi - 2 * theta
    else:
        angle1 = math.pi - 2 * theta
        angle2 = math.pi + 2 * theta
    
    dbj1 = (angle1 / math.pi) * 180
    dbj2 = (angle2 / math.pi) * 180
    print(f"带包角1 = {dbj1:.2f}°")
    print(f"带包角2 = {dbj2:.2f}°")
    
    return D_guess

def calculate_unknown_C(C_known, L, D, is_C1_unknown):
    r_known = C_known / (2 * math.pi)
    
    def f(r_unknown):
        if is_C1_unknown:
            r1, r2 = r_unknown, r_known
        else:
            r1, r2 = r_known, r_unknown
        
        delta = abs(r1 - r2)
        if D < delta:
            return float('inf')
        try:
            theta = math.asin(delta / D)
        except:
            return float('inf')
        
        if r1 > r2:
            angle1 = math.pi + 2 * theta
            angle2 = math.pi - 2 * theta
        else:
            angle1 = math.pi - 2 * theta
            angle2 = math.pi + 2 * theta
        
        arc1 = angle1 * r1
        arc2 = angle2 * r2
        tangent = 2 * math.sqrt(D**2 - delta**2)
        return arc1 + arc2 + tangent - L
    
    # 初始猜测与迭代
    r_guess = r_known + 1  # 初始偏移
    tolerance = 1e-6
    max_iter = 1000
    
    for _ in range(max_iter):
        f_val = f(r_guess)
        if abs(f_val) < tolerance:
            break
        h = 1e-6
        f_derivative = (f(r_guess + h) - f_val) / h
        if f_derivative == 0:
            break
        r_guess -= f_val / f_derivative
        r_guess = max(r_guess, 0.1)  # 防止负半径
    
    if abs(f(r_guess)) > tolerance:
        raise ValueError("无法收敛，请检查参数合理性。")
    
    # 计算最终角度
    if is_C1_unknown:
        r1, r2 = r_guess, r_known
    else:
        r1, r2 = r_known, r_guess
    
    delta = abs(r1 - r2)
    theta = math.asin(delta / D)
    if r1 > r2:
        angle1 = math.pi + 2 * theta
        angle2 = math.pi - 2 * theta
    else:
        angle1 = math.pi - 2 * theta
        angle2 = math.pi + 2 * theta
    
    dbj1 = (angle1 / math.pi) * 180
    dbj2 = (angle2 / math.pi) * 180
    print(f"带包角1 = {dbj1:.2f}°")
    print(f"带包角2 = {dbj2:.2f}°")
    
    return 2 * math.pi * r_guess

def Chinese_menu():
    print("选择需要输入的参数:")
    print("1.已知传动轮周长 C1, C2, 和传动轮圆心距 D (计算皮带长度 L)")
    print("2.已知传动轮周长 C1, C2, 和传动皮带长度 L (计算圆心距 D)")
    print("3.已知其中一轮周长 C, 皮带长度 L, 和传动轮圆心距 D (计算另一轮周长)")
    
    choice = input("请输入选项 (1/2/3): ")
    
    try:
        if choice == '1':
            C1 = float(input("请输入传动轮1周长 C1: "))
            C2 = float(input("请输入传动轮2周长 C2: "))
            D = float(input("请输入圆心距 D: "))
            length = calculate_belt_length(C1, C2, D)
            print(f"皮带长度 L = {length:.2f}")
        
        elif choice == '2':
            C1 = float(input("请输入轮1周长 C1: "))
            C2 = float(input("请输入轮2周长 C2: "))
            L = float(input("请输入皮带长度 L: "))
            D = calculate_circle_center_distance(C1, C2, L)
            print(f"圆心距 D = {D:.2f}")
        
        elif choice == '3':
            C1 = float(input("请输入轮周长 C: "))
            L = float(input("请输入皮带长度 L: "))
            D = float(input("请输入圆心距 D: "))
            C2 = calculate_unknown_C(C1, L, D, is_C1_unknown=False)
            print(f"另一轮周长 C2 = {C2:.2f}")
        
        else:
            print("无效的选项。")
    
    except ValueError as e:
        print(f"错误：{e}")


def English_menu():
    print("Please select the parameter to input:")
    print("1. Given the belt length, C1, C2, and the center distance D, calculate the belt length L.")
    print("2. Given the belt length, C1, C2, and the belt length L, calculate the center distance D.")
    print("3. Given the length of one wheel, C, the belt length L, and the center distance D, calculate the length of the other wheel")
    
    choice = input("Please enter the option (1/2/3): ")
    
    try:
        if choice == '1':
            C1 = float(input("Please enter the length of wheel 1, C1: "))
            C2 = float(input("Please enter the length of wheel 2, C2: "))
            D = float(input("Please enter the center distance, D: "))
            length = calculate_belt_length(C1, C2, D)
            print(f"The belt length is {length:.2f}.")
        
        elif choice == '2':
            C1 = float(input("Please enter the length of wheel 1, C1: "))
            C2 = float(input("Please enter the length of wheel 2, C2: "))
            L = float(input("Please enter the belt length, L: "))
            D = calculate_circle_center_distance(C1, C2, L)
            print(f"The center distance is {D:.2f}.")
        
        elif choice == '3':
            C1 = float(input("Please enter the length of one wheel, C: "))
            L = float(input("Please enter the belt length, L: "))
            D = float(input("Please enter the center distance, D: "))
            C2 = calculate_unknown_C(C1, L, D, is_C1_unknown=False)
            print(f"The length of the other wheel is {C2:.2f}.")
        
        else:
            print("Invalid option.")
    
    except ValueError as e:
        print(f"Error: {e}")

def Russian_menu():
    print("Выберите параметр для ввода:")
    print("1. Принимая длину троса C1, C2, и дистанцию между центрами D, вычислить длину троса L.")
    print("2. Принимая длину троса C1, C2, и длину троса L, вычислить дистанцию между центрами D.")
    print("3. Принимая длину одного колеса C, длину троса L, и дистанцию между центрами D, вычислить длину другого колеса.")
    
    choice = input("Введите вариант (1/2/3): ")
    
    try:
        if choice == '1':
            C1 = float(input("Введите длину колеса 1, C1: "))
            C2 = float(input("Введите длину колеса 2, C2: "))
            D = float(input("Введите дистанцию между центрами, D: "))
            length = calculate_belt_length(C1, C2, D)
            print(f"Длина троса L = {length:.2f}.")
        
        elif choice == '2':
            C1 = float(input("Введите длину колеса 1, C1: "))
            C2 = float(input("Введите длину колеса 2, C2: "))
            L = float(input("Введите длину троса, L: "))
            D = calculate_circle_center_distance(C1, C2, L)
            print(f"Дистанция между центрами D = {D:.2f}.")
        
        elif choice == '3':
            C1 = float(input("Введите длину одного колеса, C: "))
            L = float(input("Введите длину троса, L: "))
            D = float(input("Введите дистанцию между центрами, D: "))
            C2 = calculate_unknown_C(C1, L, D, is_C1_unknown=False)
            print(f"Длина другого колеса C2 = {C2:.2f}.")
        
        else:
            print("Неверный вариант.")
    
    except ValueError as e:
        print(f"Ошибка: {e}")
    
if __name__ == '__main__':
    while True:
        print("1.-------中文 (Chinese)-----")
        print("2.-------English-----------")
        print("3.-------Русский (Russian)-")
        language = input("请选择语言 (please select language):")
        if language == '1':
            Chinese_menu()
        elif language == '2':
            English_menu()
        elif language == '3':
            Russian_menu()
        else:
            print("无效的选项(Invalid option)")
            print("是否继续？continue?(y/n)",end='')
            if input() == 'n':
                break

