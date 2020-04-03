import os
import random


class MacOSNotifier:
    def __init__(self):
        self.mild_notifications = [
            "Straighten your back soldier",
            "Your pose is off", 
            "Hey, think about about your back"
            "Why dont you sit up straight"
        ]

        self.medium_notifications = [
            "Seriously, your back is going to break",
            "Come on now, think about your posture",
            "Do you love pain or why are you sitting like this?"
        ]

        self.harsh_notifications = [
            "EY YOU LITTLE BITCH LISTEN HERE. SIT UP STRAIGHT",
            "How many times do I have to tell you?",
            "This is as annoying for me as it is for you"
        ]

        self.notifications = {1:self.mild_notifications, 2: self.medium_notifications, 3:self.harsh_notifications}
    
    def send_notification(self, message_level, title):
        notification = random.choice(self.notifications[message_level])
        os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(notification, title))
            



if __name__ == "__main__":
    no = MacOSNotifier()
    no.send_notification(1, "pose malone says")