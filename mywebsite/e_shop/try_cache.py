try:
    x= int(input("Enter the first number: "))
    y= int(input("Enter the second number: "))
    z=x/y

except ZeroDivisionError:
    print("Divison by zero not possible")
except ValueError:
    print("invalid datatype")
else:
    print("the value of z is", z)
    # print(f"value of z is {z}")
finally:
    print("this will always execute")