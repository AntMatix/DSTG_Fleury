class Stack:
   def __init__(self):
      self.items = []

   def isEmpty(self):
      return self.items == []

   def push(self, my_data):
      self.items.append(my_data)

   def pop(self):
      if (self.isEmpty()):
         return "Stack is empty."
      return self.items.pop()