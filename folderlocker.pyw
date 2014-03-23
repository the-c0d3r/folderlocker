import os
from Tkinter import *
import tkMessageBox

class Locker(Frame):
    
    def __init__(self,parent):
        Frame.__init__(self,parent, background="white")
        
        self.parent = parent
        self.initvariable()
        self.initUI()

    def initvariable(self):
        global user,pwd,locker#, fake_user, fake_pwd
        user = 'f8f87915dce091a5571941436df26619'   # My private Username
        pwd = '0192023a7bbd73250516f069df18b500'    # And this is my private Password
        locker = '9e96fc70cb53a94092a5d720647a5447' # This is the folder name, when it is locked!

    def makehash(self,data):  # Just a simple method to get md5 hash
        from hashlib import md5
        tmp = md5()
        tmp.update(data)
        return tmp.hexdigest() # to return the md5 hash sum
    
    def msg(self,title,message):                    # to show error message conveniently 
        tkMessageBox.showerror(title,message)
    def about(self):
        tkMessageBox.showinfo('About',
        'This script is written by Anubis from MSF forum\n\
        Folder locker will hide the folder named "locker" out of view.\n\
        I can\'t find a way to view the hidden folder under windows environment. This script is for windows ONLY!\n\n\t\t\tAnubis [MSF Moderator]')    

    def update_status(self):
        st = self.search_locker()

        lbl_new = Label(winloggedin,text="Status : [%s]" % st)
        lbl_new.pack()
        
    def create_locker(self): # To create locker folder, if hidden or revealed folder is not detected
        import os
        drive = os.path.abspath('')[0:3]
        os.mkdir('%slocker' % drive)                # Create locker folder
        tkMessageBox.showinfo('Created',('Locker has been created successfully at %s' % drive))
        tkMessageBox.showinfo('Info','You should put everything you want to hide into locker folder,\n\tWhen you\'re done, click lock')
                
    def search_locker(self):                  # Used to search if the folder called Locker exist
        import os
        drive = os.path.abspath('')[0:3]
        #current_dir = os.path.abspath("") # Tells computer that we'll be working on local directory
        for i in os.listdir(drive): # Iterate through all file names
            if self.makehash(i) == locker:     # Make hash of the file and if has the same value as locker variable
                return 'locked'           # It will return locked. Meaning there is the hidden control panel folder
                break                     # And will break free from for loop, meaning there is no need to continue through the rest files.
            
            if i == 'locker':             # Or, we need to check if the folder called [locker] is present in the directory
                return 'unlocked'         # If yes, it means, it is unlocked!
                break                     # And yes, break free of the loop.
                                          # I don't use elif because, I need to check for both of them. Not single one of them.
        self.create_locker()
    
    def unlock(self):                            # As you may have guessed, this is the part of the code, doing all those revel work
        from os import system
        import os
        status = self.search_locker()             # To see if the locker has been locked or not
        drive = os.path.abspath('')[0:3]     # Just to get the current drive letter
        if status == 'locked':               # When the locker is confirmed to be locked!, unlock it.
            system('attrib "%sControl Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}" -s -h' % drive)
            system('ren "%sControl Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}" locker' % drive)
            tkMessageBox.showinfo('Command Completed','Locker has been Unlocked successfully') # And shows that this has been unlocked!
            system(('explorer %s' % str(drive+'locker')))
            winloggedin.destroy()                    # Deletes the current GUI and 
            self.loggedin()                   # Shows the logged in GUI again
            
        elif status == 'unlocked':           # When locker is unlocked but the user commands to unlock, show that it is unlocked!
            tkMessageBox.showinfo('Information','Locker seem to be unlocked')

        elif not status:                     # Hmm.. This means that locker is not existent 
            tkMessageBox.showinfo('Errrr..','Locker hasn\'t been created!')

    def lock(self):
        from os import system
        import os
        global drive
        status = self.search_locker()
        drive = os.path.abspath('')[0:3]
        if status == 'unlocked': # If locker is unlocked, lock it.
            system('ren %slocker "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"' % drive)
            system('attrib "%sControl Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}" +s +h' % drive)
            now_status = self.search_locker() # To check the result
            
            if now_status == 'unlocked': # If the locker is still unlocked, it means that command is not successful.
                tkMessageBox.showinfo('Sorry, can\'t close it right now','Please close any opening files and folders from LOCKER and try again.')
            elif now_status == 'locked':
                tkMessageBox.showinfo('Command Completed','Locker has been locked successfully')
                winloggedin.destroy()        # we needed another window because, status has changed.
                self.loggedin()
            
        elif status == 'unlocked':
            tkMessageBox.showinfo('Information','Locker seem to be unlocked!')
            
        elif not status:                     # Hmm.. This means that locker is not existent 
            tkMessageBox.showinfo('Errrr..','Locker hasn\'t been created!')
            
    def initUI(self):
        self.notloggedin()

    def notloggedin(self):
        # UI Before Logging in
        # 300,200
        self.centerWindow(self.parent)
        self.parent.focus_force()
        self.parent.title('Please Login!')

        #$LOGIN LABELS
        global lbl_user,lbl_pass
        #=======================
        lbl_user = Label(self.parent,text="User : ")  
        lbl_user.place(x=10,y=13)
        lbl_pass = Label(self.parent,text="Pass : ")
        lbl_pass.place(x=10,y=40)

        #$LOGIN TEXT BOX
        global txt_user,txt_pass
        #=======================
        txt_user = Entry(self.parent,width='30')          # Username Entry box
        txt_user.place(x=48,y=15)
        txt_pass = Entry(self.parent,width='30',show='*') # Password Entry box, show='*' used to cover the password
        txt_pass.place(x=48,y=43)
        Entry.focus_set(txt_user)

        #$LOGIN BUTTONS
        global btn_quit,btn_login
        #========================
        btn_login = Button(self.parent,text="Login",command=self.get,width='7')
        btn_login.place(x=145,y=70)
        btn_quit = Button(self.parent,text="Quit",command=self.bye,width='7')
        btn_quit.place(x=204,y=70)

        
        self.parent.mainloop()

    def get(self):
        #============================================
        # check if usr and pwd are empty
        user = txt_user.get()   # Get username
        passwd = txt_pass.get() # Get password
        if user != '' and passwd != '': # If both username and passwords are not empty, proceed to check the login
            self.login()
        elif user == '': # If username is empty, shows error message, that username is missing.
            self.msg('Error','Plese Provide Username')
            Entry.focus_set(txt_user) # Set focus on username field
            
        elif user != '' and passwd == '': # or else, if username is there but, password is not filled in, show message
            self.msg('Error','Please Provide Password')
            Entry.focus_set(txt_pass)
            
    def login(self):
        # This method will take user input and test if the login names and passwords are correct
        global username,password # I need to use it in other places, so making them global is essential

        #=============================================
        username = txt_user.get().strip()   # To remove un-necessary white spaces
        password = txt_pass.get().strip()
        user_hash = self.makehash(username)      # convert user to hash
        password_hash = self.makehash(password)  # convert password to hash
        
        if user_hash != user: # when username is not equal to the hash stored in user variable, show error message
            self.msg('Error!','Username and password do not match')
            txt_user.delete(0,len(str(txt_user.get()))) # delete the filled in text, 
            txt_pass.delete(0,len(str(txt_pass.get()))) # if not, user will have to select them and delete them
            Entry.focus_set(txt_user)
            
        elif user_hash == user and password_hash != pwd or user_hash != user and password_hash == pwd: # when username is correct but the password is wrong, show error message
            self.msg('Error!','Username and password do not match')
            txt_user.delete(0,len(str(txt_user.get())))
            txt_pass.delete(0,len(str(txt_pass.get())))
            Entry.focus_set(txt_user)
            
        elif user_hash == user and password_hash == pwd: # Check if we got successful login attempt
            tkMessageBox.showinfo('Welcome','Welcome back [%s]' % username) # Greet the user
            self.parent.destroy()          # User login window is no longer need because, user has logged in
            self.loggedin()          # So move on to logged in window
            

    def loggedin(self):
        #$CONFIGURATIONS
        global winloggedin,lbl_status
        winloggedin = Tk()
        winloggedin.focus_force()
        winloggedin.title('Welcome Back [%s]' % username)
        self.centerWindow(winloggedin)
        winloggedin.minsize(300,120)
        winloggedin.maxsize(350,150)
        
        self.update_status()

        #$LABELS
        lbl_frame = Label(winloggedin,text='+==========================+')
        lbl_frame.pack()
        btn_label = LabelFrame(winloggedin)
        btn_label.pack()

        #$BUTTONS
        btn_open_locker = Button(btn_label,text="Unlock",command=self.unlock,width='10')#,state=DISABLED)
        btn_open_locker.pack(side=RIGHT)
        btn_close_locker = Button(btn_label,text="Lock",command=self.lock,width='10')
        btn_close_locker.pack(side=LEFT)
        btn_quit = Button(winloggedin,text="QUIT!",command=self.bye,width='10')
        btn_quit.pack()

        menubar = Menu(winloggedin) # Creates the menu bar
        help_menu = Menu(winloggedin,tearoff=0)
        help_menu.add_command(label="About",command=self.about)
        menubar.add_cascade(label="Help",menu=help_menu)
        winloggedin.config(menu=menubar)

        winloggedin.mainloop()

    def centerWindow(self,frame):
    # For making the window appear magically at the center of the screen

        if frame == self.parent: w=300;h=150;
        elif frame == winloggedin: w=270;h=150;
        #self.parent.maxsize(350,230)
        #self.parent.minsize(350,230)

        sw = frame.winfo_screenwidth()
        # sw is equal to screen width
        sh = frame.winfo_screenheight()
        # sh equal to screen height

        x = (sw-w)/2
        y = (sh-h)/2
        frame.geometry('%dx%d+%d+%d' % (w,h,x,y))
        # Set the geometry


    def bye(self): # In py2exe compiled exe file, command=exit is causing trouble, so I created this to do the same trick
        import sys,tkMessageBox
        status = self.search_locker()
        if status == 'unlocked':
            resp = tkMessageBox.askyesno('Are you Sure?','Are you sure to exit?\nLocker is still opened, want to lock it?')
            if resp == True:
                self.lock()
                
            elif resp == False:
                tkMessageBox.showinfo('','Ok then, but please make sure to lock it once you\'re done with it.')
                sys.exit()
                
        elif status == 'locked':
            sys.exit()
        else:
            sys.exit()


def main():
    root = Tk()
    app = Locker(root)


if __name__ == '__main__':
    main()
