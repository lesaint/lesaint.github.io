title: Fix warning "Unable to import Android Lint report file(s)" in SonarQube/SonarCloud
tags: Android

I used Android Studio Koala Feature Drop | 2024.1.2 to create a new Android Application project (I used the 
"Empty Activity" template) and set up the SonarCloud analysis using the scanner for Gradle.

I had the following warning in Gradle logs:

```
> Task :sonar
Unable to import Android Lint report file(s):
- /home/runner/work/PyLMS/PyLMS/android/app/build/reports/lint-results-debug.xml
```

and further down the following:

```
> Task :app:lintReportDebug
Wrote HTML report to file:///home/runner/work/PyLMS/PyLMS/android/app/build/reports/lint-results-debug.html
```

I concluded that the `sonar` task was executed to early.

I modified the `build.gradle.kts` of the root project (where I configure the sonar tasks) to create a dependency onto
the task `:app:lint` (`:app:lintReportDebug` is a child task):

```
// add a dependency of sonar task onto any task lint of any subproject
// use afterEvaluate otherwise the task set is empty
val sonarTask = tasks.getByName("sonar")
subprojects {
    afterEvaluate {
        project.tasks.filter { it.name == "lint" }.forEach{ sonarTask.dependsOn(it)}
    }
}
```

The warning is removed and Android Lint issues are now visible in SonarQube/SonarCloud.

!!! note " Resources"
    * [Configure SonarCloud scanner for Gradle](https://docs.sonarsource.com/sonarcloud/advanced-setup/ci-based-analysis/sonarscanner-for-gradle/)
    * [version of latest SonarCloud scanner for Gradle](https://plugins.gradle.org/plugin/org.sonarqube)