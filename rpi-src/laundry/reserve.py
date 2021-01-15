import firebase_module

def main():
    fb = firebase_module.firebase("store")
    fb.get_reserve_time()

if __name__ == "__main__":
    main()