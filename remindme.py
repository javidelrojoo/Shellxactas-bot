
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
        frmt='segundo/s'
        return show,wait,frmt
    show=tiempo[:-1]
    if tiempo.endswith('d'):
        wait=float(tiempo[:-1])*86400
        frmt='dia/s'
    elif tiempo.endswith('h'):
        wait=float(tiempo[:-1])*3600
        frmt='hora/s'
    elif tiempo.endswith('m'):
        wait=float(tiempo[:-1])*60
        frmt='minuto/s'
    elif tiempo.endswith('s'):
        wait=float(tiempo)
        frmt='segundo/s'
    elif tiempo[-1].isdigit():
        show=tiempo
        wait=float(tiempo)
        frmt='segundo/s'
    else:
        return
    return show,wait,frmt
