import IPython.ipapi	
ip = IPython.ipapi.get()


def creation_readme(self, arg):
    ip = self.api 
    #ip.ex("import %s; reload(%s); from %s import *" % (arg,arg,arg) )
    text = open('../README', 'r')
    print text.read()
    text.close()

ip.expose_magic('readme', creation_readme)



