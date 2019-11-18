
def add_logs(lines):
    '''add logs to file
    
    Args:
    * lines: the content will be recorded in process.txt
    '''
    with open('process.txt', 'a+') as f:
        f.write(lines)
    print(lines)
