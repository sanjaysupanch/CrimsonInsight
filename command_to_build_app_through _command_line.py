<p> First you need to download sdk tools</p>

android create project -a MainActivity -n naino -k com.example.naino -t android-29 -g -v 5.4.1 -p naino

./gradlew assembleDebug

adb devices
./gradlew installDebug


//./gradlew assembleRelease
//./gradlew assembleRelease --no-daemon

keytool -genkey -v -keystore signing.keystore -alias signing -keyalg RSA -keysize 2048 -validity 10000

keytool -genkeypair -v  -keystore signing.keystore -storepass qwerty -keyalg RSA -keysize 2048 -validity 10000  -alias crimson -dname "CN=CrimsonInsight, OU=SoftwareDeveloper, O=CrimsonInsight, L=Deo, S=Haryana, C=IN"

./gradlew build
./gradlew assembleDebug
./gradlew assembleRelease


#####################(__Modify in Code__build.gradle)########################################


buildscript {
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.5.2'
    }
}
apply plugin: 'android'

// gradle.taskGraph.whenReady{ taskGraph -> 
//     if(taskGraph.hasTask(':assembleRelease')){
//         android.signingConfigs.release.storePassword = "qwerty" // new String(System.console().readPassword("\n Enter keystore password:"))
//         android.signingConfigs.release.keyPassword = "qwerty"//new String(System.console().readPassword("\n Enter key password:"))
//     }
// }



android {
    compileSdkVersion 'android-22'
    buildToolsVersion '29.0.2'//'29.0.2'

    signingConfigs {
        
        release {
            storeFile file("signing.keystore")
            storePassword 'qwerty'
            keyAlias "signing"
            keyPassword 'qwerty'
        }
    }
    



    buildTypes {
        release {
            
            minifyEnabled false
            proguardFile getDefaultProguardFile('proguard-android.txt')
            signingConfig signingConfigs.release
        }
    }
}

allprojects {
    repositories {
        google()
        jcenter()
        
    }
}



#####################(__Modify in Code__ /gradle-wrapper.properties)#############################

#Wed Apr 10 15:27:10 PDT 2013
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
distributionUrl=https://services.gradle.org/distributions/gradle-5.4.1-all.zip
