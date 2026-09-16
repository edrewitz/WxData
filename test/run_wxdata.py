from wxdata import gfs_0p25

def main():
    
    gfs_0p25(variables=['geopotential height'],
            levels=[500],
            process_data=False)

if __name__ == "__main__":
    main()