
def tiempo(tiempo):
    try:
        if len(tiempo)==1:
            float(tiempo)    
        else:
            float(tiempo[:-1])
    except:
        return
    if len(tiempo)==1:
        show=tiempo
        wait=float(tiempo)
        frmt='segundos'
        return show,wait,frmt
    show=tiempo[:-1]
    if tiempo.endswith('d'):
        wait=float(tiempo[:-1])*86400
        frmt='dias'
    elif tiempo.endswith('h'):
        wait=float(tiempo[:-1])*3600
        frmt='horas'
    elif tiempo.endswith('m'):
        wait=float(tiempo[:-1])*60
        frmt='minutos'
    elif tiempo.endswith('s'):
        wait=float(tiempo)
        frmt='segundos'
    elif tiempo[-1].isdigit():
        show=tiempo
        wait=float(tiempo)
        frmt='segundos'
    else:
        return
    return show,wait,frmt
