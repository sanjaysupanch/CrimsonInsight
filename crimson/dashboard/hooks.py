
# app_label="crimson"
def app_label(app_label):
    f = open('app/crimson/src/main/res/values/strings.xml', 'w')
    
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:xliff="http://schemas.android.com/apk/res-auto">

    <string name="app_name"> %s </string>
    <string name="main_activity_title"> %s </string>

</resources>

"""%(app_label, app_label))

    f.close()