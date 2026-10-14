# Python Fundamentals
> Django + Data Manipulations

1. How to define and manipulate data values. For example:
    1. 

    > In the group of MIS department, how to add a new Employee?
    >
    > mis = ['Ian', 'Marod', 'Dustin', 'Greg', 'Joey']
    >
    > Add 'Rene' in mis
    >
    > mis.append('Rene')

    2.

     In the list `attendance`, how to get all the students that are late (late == time >= 7:00 AM)
     ``` py
     attendance = [
         {
             'student_id': 1,
             'time_in': '7:15 AM'
         },
         {
             'student_id': 2,
             'time_in': '6:50 AM'
         },
         {
             'student_id': 3,
             'time_in': '6:20 AM'
         },
     ]

     # const {getter, setter} = useState(val)
     # ustState return an object of 2 items: {getter, setter}

    def get_lates():
        # Looped
        time, unit = attendance[0]['time_in'].split(' ')

        # [6, 20]   Destructure == Deconstruct
        hour, min = time.split(':')

        lates = []

        if time >= '7:00':
            lates.append(i)
    
        return lates

     ```