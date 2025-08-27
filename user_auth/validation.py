def phone_number_validation(number):
    non = list(number)
    non.reverse()
    new_number = []
    
    for i in non:
        if i != ' ':
            if len(new_number) == 10:
                break
            else: new_number.append(i)
    

    new_number.reverse()
    new_number = ''.join([x for x in new_number])
    
    return new_number