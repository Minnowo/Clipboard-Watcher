import tkinter
import re 
import os 


# will only write text that matches anything in here 
MATCHES = [ 
        
        # matches urls 
        re.compile(r"(https?://[^\s]+)") 
    ]

# the delay between clipboard checks 
DELAY_MS = 50

# the output file where the data is put (1 match from above per line)
OUTPUT_FILE = "clipboard-urls.txt"

# file write mode
# if you want to use 'w' then you probably want to chagne the class
# so that it doesn't call handle.close() after each write,
# otherwise it will overwrite all the content each time
# basically comment out the last 3 lines of 'set_value(self)'
WRITE_MODE = "a"

# if you don't want the program to remove whitespace (i.e call str.strip())
# see uwu.write_url and remove the url = url.strip() 


class uwu():

    def __init__(self, window, interval = 5, log_file = "clipboard-urls.txt", matches = MATCHES) -> None:

        self.window = window 
        self.window.withdraw() # hide the window

        self.interval = interval

        self.matches = matches

        self.log_file = log_file

        self.last_value = ""

        self.url_cach = set()

        self.handle = open(self.log_file, WRITE_MODE)  # create the file 

        self.set_value(self.window.clipboard_get())


    def write_url(self, url):
        
        url = url.strip()

        self.url_cach.add(url)

        if self.handle is None:

            self.handle = open(self.log_file, WRITE_MODE) 
        
        print(url)
        self.handle.write(url + "\n")
        

    def set_value(self, value):
        
        # run through the regex and check the cache
        for m in MATCHES:
            for mm in m.findall(value):
            
                if mm in self.url_cach:
                    continue
                
                self.write_url(mm)

        self.last_value = value 

        if self.handle is not None:
            self.handle.close()
            self.handle = None 


    def run_listener(self):
        
        # check clipboard for a new value 
        temp_value = self.window.clipboard_get()

        if self.last_value != temp_value:

            self.set_value(temp_value)

        # this is the main loop, this uses like 0 cpu for some reason idk but it's epic 
        self.window.after(self.interval, self.run_listener)


    def stop_listener(self):

        # change the method to an empty method to stop self.window.after
        self.run_listener = lambda x : None 
        
        # ensure the file handle is closed 
        if self.handle is None:
            return

        self.handle.close()


def main():
    os.system("") # console color on windows 
    YELLOW ="\033[93m"
    RED    ="\033[91m"
    ENDC   ="\033[0m"
    
    root = tkinter.Tk()

    print(YELLOW + "Listener Running. Clipboard Content Matching The Regex Will Be Shown Below:" + ENDC)

    clipboard_listener = uwu(root, DELAY_MS, OUTPUT_FILE)
    clipboard_listener.run_listener()

    try:
        root.mainloop()

    except Exception as e:
        print(RED)
        print(e)
        print(ENDC)

    except KeyboardInterrupt:
        print("Keyboard interrupt")

    finally:
        root.destroy()
        clipboard_listener.stop_listener()


if __name__ == "__main__":
    main()