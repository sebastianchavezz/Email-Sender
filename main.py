from app import last

def main():
    
    appsjoen = last.Appsjoen()
    appsjoen.protocol("WM_DELETE_WINDOW", appsjoen.on_closing)
    appsjoen.mainloop() 

if __name__ == '__main__':
    main()