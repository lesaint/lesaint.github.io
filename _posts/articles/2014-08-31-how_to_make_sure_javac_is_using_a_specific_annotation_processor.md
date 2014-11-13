---
layout: post
title: "How to make sure javac is using an annotation processor and troubleshoot when it is not"
tags: 
 - Annotation Processing
 - Javac
categories: articles
image:
 feature: feature_image_green.png
redirect_from:
  - /2014/08/31/how_to_make_sure_javac_is_using_a_specific_annotation_processor.html
comments: true
---

When developing an annotation processor, one can either declare it to ```javac``` using the ```-processorpath``` command line option or with the service provider-configuration file ```META-INF/services/javax.annotation.processing.Processor```.

In both cases, when our annotation processor seems not to be invoked by ```javac```, it is not easy to troubleshoot why ```javac``` is not using it, especially as we are not getting any error.

We will see in this article how to enable and interpret ```javac``` logs to make sure the annotation processor is run and if not, how to interpret them to get a few leads on where the problem is coming from.


## enable and interprete ```javac``` logs

Since I am using ```Maven``` to build my project, I am not writing ```javac``` command lines by hand, ```Maven``` does it for me.

Obviouly, one could configure the ```maven-compile``` plugin in the pom.xml file to enable the logs we need in ```javac``` but ```Maven``` has a tendancy in swallowing ```javac``` logs. In addition, running ```Maven``` will flood the terminal with logs we don't care about. So we would rather use the ```javac``` command directly. 

### retrieve the ```javac``` command line from ```Maven```

Run ```Maven``` with -X option on the module which uses the annotation processor and copy the log line after log ```[DEBUG] Command line options:```.

For example, run ```Maven``` with the following command line:

{% highlight sh %}
mvn clean compile -X -pl :moduleName
{% endhighlight %}

> ```-pl :moduleName``` is a way of specifying a specific module for ```Maven``` to build. It allows to run the ```mvn``` command from the root directory of the project. Obviously, in a single module project, this is useless. In a multi-module project however, its convenient. It saves you from changing the current directory to the module's directory and run the same ```mvn``` command without that option.

### customize the command line

1. prefix what you just copied with the ```javac``` command
2. remove ```-nowarn``` option, we need to see any information available, this option removes warnings
3. add options ```-verbose -XprintRounds -XprintProcessorInfo -Xlint -J-verbose```
    * ```-verbose```
        - (doc description) Verbose output. This includes information about each class loaded and each source file compiled.
    * ```-Xlint```
        - (doc description) Enable all recommended warnings. In this release, enabling all available warnings is recommended.
    * ```-XprintProcessorInfo```
        - (doc description) Print information about which annotations a processor is asked to process.
    * ```-XprintRounds```
        - (doc description) Print information about initial and subsequent annotation processing rounds
    * -J-verbose
        - (doc description) Sets the -verbose option of JVM run internally by javac
    * warning about ```-Xprint```
        - DO NOT USE this option when you want to investigage annotation processors
        - this option will use a Java runtime internal annotation processor to display source of compiled files and ```javac``` won't log the actual annotation processor(s) that will be run during the round. It seems that this internal annotation processor wraps the actually used annotation processor(s) and we don't see which in logs
        - (doc description) Print out textual representation of specified types for debugging purposes; perform neither annotation processing nor compilation. The format of the output may change.
    * (see http://docs.oracle.com/javase/7/docs/technotes/tools/windows/javac.html for details)

4. (optional) send all outputs to a file, add ```> /tmp/compile_clean.log 2>&1```

## make sure the annotation processor is run by ```javac```

To make sure there is no problem loading your Annotation Processor class, look for the next 4 log lines.

1. look for a log line stating that the .class file of your AnnotationProcessor class is being read.     
    * if the class is in a Jar:

        {% highlight sh %}
        [loading ZipFileIndexFileObject[/opt/maven/repository/fr/javatronic/damapping/annotation-processor/0.2.3-bundle-clean-SNAPSHOT/annotation-processor-0.2.3-bundle-clean-SNAPSHOT.jar(fr/javatronic/damapping/processor/DAAnnotationProcessor.class)]]
        {% endhighlight %}
    * if the class is on the file system

        {% highlight sh %}
        [loading RegularFileObject[/home/user/DEV/damapping/damapping-samples/spring-project/target/classes/fr/javatronic/damapping/processor/DAAnnotationProcessor.class]]
        {% endhighlight %}

2. look for at least one annotation processor round log
    * look for the ```Round``` string
    * a round log line looks like the following:

        {% highlight sh %}
        Round 1:
                input files: {fr.javatronic.damapping.demo.domain.repository.impl.CourseSlotRepositoryImpl, fr.javatronic.damapping.demo.domain.repository.impl.CourseRepositoryImpl, fr.javatronic.damapping.demo.domain.repository.CourseSlotRepository, fr.javatronic.damapping.demo.domain.model.Teacher, fr.javatronic.damapping.demo.view.service.impl.PeopleIndexServiceImpl, fr.javatronic.damapping.demo.view.model.Day, fr.javatronic.damapping.demo.view.model.TimedClass, fr.javatronic.damapping.demo.view.mapper.IntegerToString, fr.javatronic.damapping.demo.view.model.WeekPlanning, fr.javatronic.damapping.demo.view.model.EveningClasses, fr.javatronic.damapping.demo.MainClass, fr.javatronic.damapping.demo.view.service.impl.WeekPlanningServiceImpl, fr.javatronic.damapping.demo.spring.ApplicationConfig, fr.javatronic.damapping.demo.view.mapper.TeacherToPeople, fr.javatronic.damapping.demo.domain.repository.impl.TeacherRositoryImpl, fr.javatronic.damapping.demo.domain.model.Course, fr.javatronic.damapping.demo.view.model.AfternoonClasses, fr.javatronic.damapping.demo.view.model.Classes, fr.javatronic.damapping.demo.view.service.WeekPlanningService, fr.javatronic.damapping.demo.view.mapper.StudentToPeople, fr.javatronic.damapping.demo.view.model.PeopleIndex, fr.javatronic.damapping.demo.domain.model.CourseSlot, fr.javatronic.damapping.demo.domain.repository.impl.StudentRepositoryImpl, fr.javatronic.damapping.demo.domain.repository.StudentRepository, fr.javatronic.damapping.demo.view.service.PeopleIndexService, fr.javatronic.damapping.demo.view.model.MorningClasses, fr.javatronic.damapping.demo.view.model.People, fr.javatronic.damapping.demo.domain.repository.CourseRepository, fr.javatronic.damapping.demo.domain.model.Student, fr.javatronic.damapping.demo.domain.repository.TeacherRository}
                annotations: [java.lang.Override, fr.javatronic.damapping.annotation.Mapper, javax.annotation.Nullable, org.springframework.context.annotation.Configuration]
                last round: false
        {% endhighlight %}
    * make sure your annotation(s) are present in the list in the line before the last line
3. look for the log line indicating that your AnnotationProcessor has been identified to process one or more annotation

    {% highlight sh %}
    Processor [qualified name of your AnnotationProcessor class] matches [name(s) of the annotation(s) your AnnotationProcessor will be invoked for] and returns [true/false].
    {% endhighlight %}
4. look for a log line stating that your AnnotationProcessor class has been loaded, such as

    {% highlight sh %}
    [Loaded fr.javatronic.damapping.processor.DAAnnotationProcessor from file:/opt/maven/repository/fr/javatronic/damapping/annotation-processor/0.2.3-bundle-clean-SNAPSHOT/annotation-processor-0.2.3-bundle-clean-SNAPSHOT.jar]
    {% endhighlight %}

If you cannot find the first log line, your AnnotationProcessor is not in the classpath of the ```javac``` command.

If you cannot find the second log line, ```javac``` did not pick any annotation processor in the classpath at all (so, not yours nor any other) or annotation processing is disabled. Make sure you don't have the ```-proc:none``` on your command line.

If you cannot find your annotation(s) in the second log line, you are just not compiling any class with your annotation(s). Your Annotation Processor will never be run by ```javac```.

If you cannot find the third log line, your AnnotationProcessor might be incorrectly configured. Make sure the ```getSupportedOptions()``` method of your Annotation Processor returns correctly the canonical name of the annotation(s) you want to process.

If you cannot find the fourth log line, your Annotation Processor class or any class it depends on can not be loaded by ```javac```. There may be various reasons for that but I don't know how to get more details about that from ```javac```.

Obviously, if you can see all 4 log lines and don't get any error at all, your annotation processor is correctly beeing run by ```javac``` and your problem is most likely the code of your Annotation Processor.

You then need to debug your Annotation Processor and this is not trivial. I will likely post an article on how to debug an Annotation Processor soon.

Hope this helps.
