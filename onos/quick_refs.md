

mvn archetype:generate -DarchetypeGroupId=org.onosproject -DarchetypeArtifactId=onos-bundle-archetype

* onos-create-app : 
```

Define value for property 'groupId': : org.foo    
Define value for property 'artifactId': : foo-app
Define value for property 'version':  1.0-SNAPSHOT: :
Define value for property 'package':  org.foo: : org.foo.app
Confirm properties configuration:
groupId: org.foo
artifactId: foo-app
version: 1.0-SNAPSHOT
package: org.foo.app
 Y: :
```

kauri@kdev:~/test$ tree
.
└── 3
    ├── pom.xml
    └── src
        ├── main
        │   └── java
        │       └── ktst
        │           └── AppComponent.java
        └── test
            └── java
                └── ktst
                    └── AppComponentTest.java

8 directories, 3 files
kauri@kdev:~/test$

kauri@kdev:~/onos-app-samples$ tree ifwd/
ifwd/
├── pom.xml
├── src
│   └── main
│       └── java
│           └── org
│               └── onosproject
│                   └── ifwd
│                       ├── IntentReactiveForwarding.java
│                       └── package-info.java


21 directories, 17 files
kauri@kdev:~/onos-app-samples$
