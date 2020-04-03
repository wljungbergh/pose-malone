import os



class decision_maker:

    def __init__(self):
        pass

    def notify(self, title, text):
        os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(text, title))

d_maker = decision_maker()

d_maker.notify("Title", "Heres an alert")
