from source.InfoClass import Assistant_Info

assistant_info = Assistant_Info()



def assistant_start(global_signal):
    assistant = assistant_info.pickle_get()
    global_signal.log_print.emit(str(assistant['drug']))


