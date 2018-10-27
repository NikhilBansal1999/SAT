import sys
import time
import copy

num_literals=0
start_time=0

def read_from_file(infile):
    global num_literals
    inhand=open(infile,"r")
    line_num=0
    cons=list()
    cons.append(list())
    for line in inhand:
        line_num=line_num+1
        if line_num==1:
            inp=line.strip().split()
            num_literals=int(inp[2])
            continue
        else:
            inp=line.strip().split()
            inp2=[int(k) for k in inp]
            cons[0].append(inp2[:len(inp)-1])

    return cons

def check_validity(con_list):#returns 1 for consistent list else return 0
    length_list=len(con_list)
    for i in range(length_list):
        if type(con_list[i]) is list:
            continue
        else:
            for j in range(i+1,length_list):
                if type(con_list[j]) is list:
                    continue
                else:
                    elem1=int(con_list[i])
                    elem2=int(con_list[j])
                    if (elem1+elem2) == 0: #inconsistencies found
                        return 0

    return 1 # if no inconsistencies are found, the code will reach here

def remove_redundant_lists(con_list):
    for i in range(len(con_list)):
        if type(con_list[i]) is list:
            if len(con_list[i])==1:
                con_list[i]=con_list[i][0]

    return con_list

def remove_redundancy(con_list):
    i=0
    while i<len(con_list):
        if type(con_list[i]) is list:
            i=i+1
            continue
        else:
            j=0
            while j<len(con_list):
                if i==j:
                    j=j+1
                    continue
                if type(con_list[j]) is list:
                    for elem in con_list[j]:
                        if elem == con_list[i]:#this condition is redundant
                            del con_list[j]
                            if j<i:
                                i=i-1
                            j=j-1
                            break
                        elif (elem + con_list[i])==0:#this literal is not satisfiable
                            con_list[j].remove(elem)
                            #if removal leads to an empty literal con_list is unsatisfiable
                            if len(con_list[j])==0:
                                return 0
                    j=j+1
                else:
                    if con_list[j]==con_list[i]:
                        del con_list[j]
                        if j<i:
                            i=i-1
                        continue
                    if (con_list[j]+con_list[i])==0:#inconsistencies found
                        return 0
                    #nothing special continue to next element
                    j=j+1
            i=i+1

    return con_list

def list_free(con_list):#returns 1 if the list has no nested list else returns 0
    for elem in con_list:
        if type(elem) is list:
            return 0

    return 1

def solve(conditions):
    global num_literals
    global start_time
    num_break=0

    while len(conditions) > 0:
        print(len(conditions))
        #check if there is a satisfying assignment
        num_break=num_break+1
        n=0
        while n<len(conditions):
            if list_free(conditions[n])==1:#no nested list, it will either be SAT or UNSAT with no branching needed
                #check if it is satisfiable
                if check_validity(conditions[n])==1:#we got a satisfying assignment
                    sat_list=[0]*num_literals
                    for j in conditions[n]:
                        if j>0:
                            sat_list[j-1]=1
                    print("SAT")
                    for i in range(len(sat_list)):
                        if sat_list[i]==0:
                            print(-1*(i+1),end=" ")
                        else:
                            print((i+1),end=" ")
                    print()
                    end_time=time.time()
                    print(end_time-start_time)
                    print("Broke: ",num_break)
                    sys.exit()
                else:#this is an UNSAT clause
                    del conditions[n]
            else:
                n=n+1
        #if no assignment found this time break some more lists
        for i in range(len(conditions)):
            to_break=0
            for j in range(len(conditions[i])):
                if type(conditions[i][j]) is list:
                    con=conditions.pop(i)
                    list_in_con=con.pop(j)
                    for elem in list_in_con:
                        con_app=copy.deepcopy(con)+[elem]
                        con_app=remove_redundant_lists(con_app)
                        consistency=check_validity(con_app)
                        if consistency==1:
                            con_app=remove_redundancy(con_app)
                            if con_app==0:
                                continue
                            else:
                                con_app=remove_redundant_lists(con_app)
                                conditions.insert(0,con_app)
                    to_break=1
                    break
            if to_break==1:
                break

    end_time=time.time()
    print(end_time-start_time)
    print("Broke: ",num_break)
    print("UNSAT")

if __name__=="__main__":
    start_time=time.time()
    infile=sys.argv[1]
    condition=read_from_file(infile)
    condition[0]=remove_redundant_lists(condition[0])
    condition[0]=remove_redundancy(condition[0])
    condition[0]=remove_redundant_lists(condition[0])
    solve(condition)
