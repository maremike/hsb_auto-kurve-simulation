from multiprocessing import Process

from view.wholeView import init_views, updateView


def view():
    init_views()
    #viewProcess = Process(target=updateView())
    #viewProcess.start()